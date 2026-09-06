import importlib.util
from pathlib import Path
import unittest
spec = importlib.util.spec_from_file_location('docs_snapshot', Path(__file__).resolve().parents[1] / 'scripts/sync_local_kujo_docs.py')
docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docs)

class SnapshotTests(unittest.TestCase):
    def test_article_code_warning_and_link_survive_without_navigation(self):
        raw = b'<nav>Discard navigation</nav><main><aside>Side menu</aside><article><h1>Imports</h1><p>Warning: use approved packages.</p><pre><code class="language-kujo">if ready {\n    print("yes")\n}</code></pre><a href="/learn/packages/">Packages</a><script>discard_script()</script></article></main>'
        text = docs.extract(raw, 'text/html', docs.ORIGIN + '/imports/')
        self.assertIn('```kujo\nif ready {\n    print("yes")\n}', text)
        self.assertIn('Warning: use approved packages.', text)
        self.assertIn('[Packages](https://docs.kujolang.ai/learn/packages/)', text)
        self.assertNotIn('discard_script', text)
        self.assertNotIn('Side menu', text)
        self.assertNotIn('Discard navigation', text)
        self.assertTrue(text.startswith('Source: https://docs.kujolang.ai/imports/'))
    def test_unrecognized_html_does_not_become_a_document(self):
        with self.assertRaises(ValueError):
            docs.extract(b'<html>Service unavailable</html>', 'text/html', docs.ORIGIN)

if __name__ == '__main__':
    unittest.main()
