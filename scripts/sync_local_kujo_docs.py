"""Snapshot the public Kujo docs into Markdown for local RAG dogfooding.

Python standard library + curl only. Does not execute downloaded content.
Run from the RAG root, then ingest data/local-kujo-docs/corpus.
"""
import concurrent.futures
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET

ORIGIN = 'https://docs.kujolang.ai'
ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'data/local-kujo-docs'


def fetch(url):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.netloc != 'docs.kujolang.ai':
        raise ValueError('Only the configured public docs origin may be fetched')
    # No redirects: sitemap entries must resolve directly on this origin.
    with tempfile.NamedTemporaryFile() as body:
        result = subprocess.run(['curl', '--fail', '--silent', '--show-error',
            '--proto', '=https', '--max-time', '30', '--max-filesize', '5000000',
            '-H', 'Accept: text/markdown, text/html;q=0.9, text/plain;q=0.8',
            '--write-out', '%{http_code}\n%{content_type}', '-o', body.name, url],
            check=True, capture_output=True, text=True, timeout=35)
        status, mime = result.stdout.split('\n', 1)
        if status != '200':
            raise ValueError(f'Document returned HTTP {status}: {url}')
        return Path(body.name).read_bytes(), mime.split(';')[0].lower()


class Markdown(HTMLParser):
    def __init__(self, url):
        super().__init__(convert_charrefs=True)
        self.url, self.parts, self.links = url, [], []
        self.skip, self.pre, self.code, self.fence = 0, False, False, '```'

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style', 'nav', 'aside', 'button', 'svg'):
            self.skip += 1
        if self.skip:
            return
        if tag == 'pre':
            self.pre = True
        elif tag == 'code':
            self.code = True
            if self.pre:
                language = next((c[9:] for c in attrs.get('class', '').split() if c.startswith('language-')), '')
                self.parts.append('\n\n' + self.fence + language + '\n')
            else:
                self.parts.append('`')
        elif re.fullmatch('h[1-6]', tag):
            self.parts.append('\n\n' + '#' * int(tag[1]) + ' ')
        elif tag in ('p', 'div', 'section', 'ul', 'ol', 'table', 'tr', 'blockquote'):
            self.parts.append('\n\n')
        elif tag == 'li':
            self.parts.append('\n- ')
        elif tag == 'br':
            self.parts.append('\n')
        elif tag in ('td', 'th'):
            self.parts.append(' | ')
        elif tag == 'a':
            target = urljoin(self.url, attrs.get('href', ''))
            self.links.append(target if urlsplit(target).scheme in ('https', 'http') else '')
            self.parts.append('[')

    def handle_endtag(self, tag):
        if self.skip:
            if tag in ('script', 'style', 'nav', 'aside', 'button', 'svg'):
                self.skip -= 1
            return
        if tag == 'code':
            self.parts.append('\n' + self.fence + '\n\n' if self.pre else '`')
            self.code = False
        elif tag == 'pre':
            self.pre = False
        elif tag == 'a' and self.links:
            self.parts.append('](' + self.links.pop() + ')')
        elif tag in ('p', 'li') or re.fullmatch('h[1-6]', tag):
            self.parts.append('\n\n')

    def handle_data(self, text):
        if not self.skip:
            self.parts.append(text if self.pre else re.sub(r'\s+', ' ', text))


def extract(raw, mime, url):
    text = raw.decode('utf-8')
    if mime == 'text/html':
        match = re.search(r'<article\b[^>]*>([\s\S]*?)</article>', text, re.I)
        if not match:
            match = re.search(r'<main\b[^>]*>([\s\S]*?)</main>', text, re.I)
        if not match:
            raise ValueError(f'No document content found: {url}')
        parser = Markdown(url)
        # Fence length exceeds any backtick run in the source.
        parser.fence = '`' * max(3, max((len(m) + 1 for m in re.findall(r'`+', match[1])), default=3))
        parser.feed(match[1])
        text = ''.join(parser.parts).strip()
    elif mime not in ('text/markdown', 'text/plain'):
        raise ValueError(f'Unsupported document type: {mime}')
    if len(text.strip()) < 40:
        raise ValueError(f'Empty document: {url}')
    return f'Source: {url}\n\n{text}\n'


def main():
    sitemap, _ = fetch(ORIGIN + '/sitemap.xml')
    urls = sorted(set(n.text for n in ET.fromstring(sitemap).findall('.//{*}loc')))
    if not 1 <= len(urls) <= 500:
        raise ValueError('Unexpected sitemap size')
    DEST.mkdir(parents=True, exist_ok=True)
    snapshot = []
    # Fetch the complete snapshot before replacing any existing corpus file.
    def document(url):
        raw, mime = fetch(url)
        return url, raw, mime, extract(raw, mime, url)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for item in pool.map(document, urls):
            snapshot.append(item)
    corpus = DEST / 'corpus'
    corpus.mkdir(exist_ok=True)
    records, names = [], set()
    for url, raw, mime, text in snapshot:
        route = urlsplit(url).path.strip('/') or 'index'
        name = re.sub('[^a-zA-Z0-9_-]', '-', route) + '-' + hashlib.sha256(url.encode()).hexdigest()[:8] + '.md'
        names.add(name)
        (corpus / name).write_text(text)
        records.append({'url': url, 'file': name, 'media_type': mime, 'source_sha256': hashlib.sha256(raw).hexdigest(), 'markdown_bytes': len(text.encode())})
    # Only remove files owned by the previous snapshot manifest.
    prior = DEST / 'manifest.json'
    if prior.exists():
        for record in json.loads(prior.read_text())['documents']:
            name = record['file']
            if name not in names and Path(name).name == name:
                (corpus / name).unlink(missing_ok=True)
    report = {'source': ORIGIN, 'fetched_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'count': len(records), 'documents': records}
    prior.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'ok': True, 'documents': len(records), 'corpus': str(corpus), 'manifest': str(prior)}))


if __name__ == '__main__':
    main()
