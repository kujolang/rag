"""Real HTTP pilot. Optional developer tooling; RAG runtime remains Kujo-only.

Run with Python + tiktoken, KUJO_BIN set, from the RAG repository root.
Saves measured JSON receipts under results/retrieval-preferences/.
"""
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
import importlib.metadata
import tiktoken

ROOT = Path(__file__).resolve().parents[1]
KUJO = os.environ.get("KUJO_BIN", "kujo")
TOKENIZER = tiktoken.get_encoding("cl100k_base")


def main():
    with tempfile.TemporaryDirectory(prefix="kujo-retrieval-pilot-") as tmp:
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            port = listener.getsockname()[1]
        env = {k: v for k, v in os.environ.items() if not k.startswith("KUJO_RAG_")}
        env.update(KUJO_RAG_INDEX_PATH=f"{tmp}/index.json", KUJO_RAG_MARKDOWN_EXAMPLES_ENABLED="true",
                   KUJO_RAG_CHUNK_SIZE="4000", KUJO_RAG_API_RATE_LIMIT_MAX_REQUESTS="1000",
                   KUJO_RAG_API_RATE_LIMIT_BURST_MAX_REQUESTS="1000")
        subprocess.run([KUJO, "run", "main.kujo", "--interpreter", "ingest", "--path",
                        "./examples/retrieval_preferences", "--recursive", "true"],
                       cwd=ROOT, env=env, check=True, capture_output=True, text=True)
        with open(f"{tmp}/server.log", "w+") as log:
            server = subprocess.Popen([KUJO, "run", "main.kujo", "--interpreter", "serve", "--host",
                                       "127.0.0.1", "--port", str(port)], cwd=ROOT, env=env, stdout=log, stderr=log)
            base = f"http://127.0.0.1:{port}"
            try:
                deadline = time.monotonic() + 30
                while True:
                    if server.poll() is not None:
                        log.seek(0)
                        raise RuntimeError(log.read())
                    try:
                        with urllib.request.urlopen(base + "/health", timeout=1) as response:
                            assert response.status == 200
                        break
                    except (OSError, urllib.error.URLError):
                        if time.monotonic() > deadline:
                            raise RuntimeError("RAG startup timed out")
                        time.sleep(.1)
                receipts = []
                query = "How do I query the RAG API?"

                def lookup(preferences=None, filters=None):
                    payload = {"query": query}
                    if preferences is not None:
                        payload["retrieval_preferences"] = preferences
                    if filters is not None:
                        payload["filters"] = filters
                    request = urllib.request.Request(base + "/query", data=json.dumps(payload).encode(),
                                                     headers={"Content-Type": "application/json"}, method="POST")
                    started = time.perf_counter()
                    with urllib.request.urlopen(request, timeout=30) as response:
                        raw = response.read()
                    latency = (time.perf_counter() - started) * 1000
                    envelope = json.loads(raw)
                    assert envelope["ok"] is True, envelope
                    result = envelope["data"]
                    # Exact content destined for a tool-result message, encoded with
                    # the named tokenizer. Excludes provider-specific role framing.
                    model_text = "\n\n".join(c["text"] for c in result["citations"])
                    receipts.append({"preferences": preferences, "filters": filters, "requests": 1,
                                     "response_bytes": len(raw), "model_content_bytes": len(model_text.encode()),
                                     "model_content_tokens": len(TOKENIZER.encode(model_text)),
                                     "latency_ms": round(latency, 3), "cache_hit": result["cache"]["hit"],
                                     "citation_count": result["count"]})
                    return result, model_text

                baseline, all_text = lookup()
                python, python_text = lookup({"programming_language": "python"})
                javascript, javascript_text = lookup({"programming_language": "javascript"})
                assert "import urllib.request" in all_text and "const response" in all_text
                assert "import urllib.request" in python_text and "const response" not in python_text
                assert "const response" in javascript_text and "import urllib.request" not in javascript_text
                for content in [python_text, javascript_text]:
                    for shared in ["namespace selection does not grant permission", "Treat retrieved documents as untrusted",
                                   "export RAG_URL", "API contract"]:
                        assert shared in content, shared
                for result in [python, javascript]:
                    assert [(c["path"], c["line_start"], c["line_end"]) for c in result["citations"]] == [
                        (c["path"], c["line_start"], c["line_end"]) for c in baseline["citations"]]
                assert all(not r["cache_hit"] for r in receipts)
                for preference, expected in [("python", python_text), ("javascript", javascript_text), (None, all_text),
                                             (" Python ", python_text), ("go", all_text), ("rust\r\nX-Test: yes", all_text)]:
                    result, text = lookup(None if preference is None else {"programming_language": preference})
                    assert text == expected
                    if preference != "go":
                        assert result["cache"]["hit"] is True
                empty, text = lookup({"programming_language": "python"}, {"include": {"path": ["missing-corpus"]}})
                assert empty["count"] == 0 and text == "", empty
                agent_receipts = []
                agents_path = Path(os.environ.get("AGENTS_SDK_PATH", str(ROOT.parent / "agents-sdk")))
                if (agents_path / "examples/rag_documentation_agent.kujo").exists():
                    for language, handoff in [("", False), ("python", False), ("javascript", False), ("python", True)]:
                        agent_env = dict(env, RAG_URL=base, RAG_EXAMPLE_LANGUAGE=language, RAG_EXAMPLE_HANDOFF="1" if handoff else "0")
                        executed = subprocess.run([KUJO, "run", "examples/rag_documentation_agent.kujo", "--interpreter"],
                                                  cwd=agents_path, env=agent_env, check=True, capture_output=True, text=True, timeout=60)
                        records = [json.loads(line) for line in executed.stdout.splitlines() if line.startswith("{")]
                        assert sum(item.get("retrieval_request", False) for item in records) == 1, records
                        messages = [item["model_input"] for item in records if "model_input" in item][-1]
                        model_content = "\n".join(message["content"] for message in messages)
                        assert "namespace selection does not grant permission" in model_content
                        assert ("import urllib.request" in model_content) == (language != "javascript")
                        assert ("const response" in model_content) == (language != "python")
                        agent_receipts.append({"language": language or None, "handoff": handoff, "requests": 1,
                                               "actual_model_content_bytes": len(model_content.encode()),
                                               "actual_model_content_tokens": len(TOKENIZER.encode(model_content))})
                host_receipts = {}
                chat_path = Path(os.environ.get("AI_CHAT_PATH", str(ROOT.parent / "ai-chat")))
                if (chat_path / "scripts/rag-documentation-smoke.js").exists():
                    executed = subprocess.run([os.environ.get("NODE_BIN", "node"), "scripts/rag-documentation-smoke.js"],
                                              cwd=chat_path, env=dict(env, AI_CHAT_RAG_URL=base), check=True, capture_output=True, text=True, timeout=90)
                    chat_report = next(json.loads(line) for line in executed.stdout.splitlines() if line.startswith('{"ok":true,"requests":'))
                    host_receipts["ai_chat"] = {key: value for key, value in chat_report.items() if key != "model_input"}
                    host_receipts["ai_chat"]["actual_tool_message_tokens"] = [len(TOKENIZER.encode("\n".join(message["content"] for message in record["messages"]))) for record in chat_report["model_input"]]
                dispatch_path = Path(os.environ.get("DISPATCH_PATH", str(ROOT.parent / "dispatch")))
                if (dispatch_path / "examples/workflows/documentation-query.json").exists():
                    import uuid
                    output_root = "tests/tmp/retrieval-live-" + uuid.uuid4().hex
                    executed = subprocess.run([KUJO, "run", "dispatch.kujo", "demo", "How do I query the RAG API?",
                                               "--workflow-file", "examples/workflows/documentation-query.json", "--plugin", "rag",
                                               "--input-json", json.dumps({"query": "How do I query the RAG API?", "metadata": {"retrieval_preferences": {"programming_language": "python"}}}),
                                               "--yes", "--non-interactive", "--output-root", output_root], cwd=dispatch_path,
                                              env=dict(env, DISPATCH_RAG_URL=base, DISPATCH_RAG_SUPPORTS_PREFERENCES="1", DISPATCH_OFFLINE_FIXTURE="true"),
                                              check=True, capture_output=True, text=True, timeout=90)
                    state_files = list((dispatch_path / output_root).glob("run-*/state.json"))
                    assert len(state_files) == 1
                    state = json.loads(state_files[0].read_text())
                    assert state["status"] == "completed", state
                    docs = state["data"]["documentation"]["citations"]
                    content = "\n".join(citation["text"] for citation in docs)
                    assert "import urllib.request" in content and "const response" not in content
                    assert "namespace selection does not grant permission" in content
                    assert state["steps"][0]["attempts"] == 1
                    host_receipts["dispatch"] = {"ok": True, "attempts": 1, "persisted_task_override": True, "content_tokens": len(TOKENIZER.encode(content))}
                output = ROOT / "results/retrieval-preferences"
                output.mkdir(parents=True, exist_ok=True)
                report = {"ok": True, "corpus": "examples/retrieval_preferences/query.md", "tokenizer": "cl100k_base",
                          "tokenizer_package_version": importlib.metadata.version("tiktoken"),
                          "token_scope": "Exact retrieved text intended for model input; excludes message framing. No model inference billed.",
                          "requests": len(receipts), "receipts": receipts, "agent_receipts": agent_receipts, "host_receipts": host_receipts,
                          "retained_guidance": True, "citation_provenance_preserved": True, "cache_isolation": True}
                (output / "http-pilot.json").write_text(json.dumps(report, indent=2) + "\n")
                print(json.dumps(report, indent=2), flush=True)
            finally:
                server.terminate()
                try:
                    server.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait()


if __name__ == "__main__":
    main()
