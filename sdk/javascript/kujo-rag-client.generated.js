// Generated from ./openapi/kujo-rag-openapi.json by scripts/run_openapi_contract_review.kujo
// DO NOT EDIT MANUALLY.

class KujoRagClient {
	constructor(options = {}) {
		this.baseUrl = options.baseUrl || "http://127.0.0.1:8787";
		this.defaultHeaders = options.defaultHeaders || {};
	}

	async request(method, path, body = null, extraHeaders = {}) {
		const headers = Object.assign({}, this.defaultHeaders, extraHeaders);
		if (body !== null && headers['Content-Type'] === undefined) {
			headers['Content-Type'] = 'application/json';
		}
		const response = await fetch(this.baseUrl + path, {
			method,
			headers,
			body: body === null ? undefined : JSON.stringify(body)
		});
		const text = await response.text();
		let parsed = null;
		if (text !== '') {
			try {
				parsed = JSON.parse(text);
			} catch (_err) {
				parsed = text;
			}
		}
		if (!response.ok) {
			const err = new Error('Kujo RAG API request failed: ' + response.status);
			err.status = response.status;
			err.body = parsed;
			throw err;
		}
		return parsed;
	}

	async getRoot(extraHeaders = {}) {
		return this.request("GET", "/", null, extraHeaders);
	}

	async getHealth(extraHeaders = {}) {
		return this.request("GET", "/health", null, extraHeaders);
	}

	async getLive(extraHeaders = {}) {
		return this.request("GET", "/live", null, extraHeaders);
	}

	async getReady(extraHeaders = {}) {
		return this.request("GET", "/ready", null, extraHeaders);
	}

	async getStartup(extraHeaders = {}) {
		return this.request("GET", "/startup", null, extraHeaders);
	}

	async postIngest(payload = {}, extraHeaders = {}) {
		return this.request("POST", "/ingest", payload, extraHeaders);
	}

	async postIngestJobs(payload = {}, extraHeaders = {}) {
		return this.request("POST", "/ingest/jobs", payload, extraHeaders);
	}

	async postIngestJobsStatus(payload = {}, extraHeaders = {}) {
		return this.request("POST", "/ingest/jobs/status", payload, extraHeaders);
	}

	async postIngestJobsWorkerTick(extraHeaders = {}) {
		return this.request("POST", "/ingest/jobs/worker/tick", null, extraHeaders);
	}

	async postQuery(payload = {}, extraHeaders = {}) {
		return this.request("POST", "/query", payload, extraHeaders);
	}

	async getMetrics(extraHeaders = {}) {
		return this.request("GET", "/metrics", null, extraHeaders);
	}

	async getRetention(extraHeaders = {}) {
		return this.request("GET", "/retention", null, extraHeaders);
	}

	async postRetentionPolicy(payload = {}, extraHeaders = {}) {
		return this.request("POST", "/retention/policy", payload, extraHeaders);
	}

	async postRetentionPurge(payload = {}, extraHeaders = {}) {
		return this.request("POST", "/retention/purge", payload, extraHeaders);
	}

	async postRetentionLegalHoldStart(payload = {}, extraHeaders = {}) {
		return this.request("POST", "/retention/legal-hold/start", payload, extraHeaders);
	}

	async postRetentionLegalHoldStop(payload = {}, extraHeaders = {}) {
		return this.request("POST", "/retention/legal-hold/stop", payload, extraHeaders);
	}

	async postPrivacyExport(payload = {}, extraHeaders = {}) {
		return this.request("POST", "/privacy/export", payload, extraHeaders);
	}

	async postPrivacyDelete(payload = {}, extraHeaders = {}) {
		return this.request("POST", "/privacy/delete", payload, extraHeaders);
	}

	async getDrain(extraHeaders = {}) {
		return this.request("GET", "/drain", null, extraHeaders);
	}

	async postDrainStart(payload = {}, extraHeaders = {}) {
		return this.request("POST", "/drain/start", payload, extraHeaders);
	}

	async postDrainStop(extraHeaders = {}) {
		return this.request("POST", "/drain/stop", null, extraHeaders);
	}
}

module.exports = { KujoRagClient };
