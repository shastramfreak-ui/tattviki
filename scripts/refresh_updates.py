#!/usr/bin/env python3
"""Refresh official GitHub project releases. Standard library only.

This is a transparent *metadata* feed, not generated journalism.
The W3C baseline references are curated and retained even if GitHub is down.
"""
import datetime as dt
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'data' / 'updates.json'
REPOSITORIES = {
    'rdfjs/N3.js': 'RDF JavaScript',
    'comunica/comunica': 'SPARQL engine',
    'RDFLib/pySHACL': 'SHACL validation',
    'microsoft/graphrag': 'GraphRAG',
    'apache/jena': 'RDF framework',
    'oxigraph/oxigraph': 'RDF database',
}

def fetch_latest(repo):
    api = f'https://api.github.com/repos/{repo}/releases/latest'
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Tāttvikī-learning-updates'}
    token = os.getenv('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = 'Bearer ' + token
    req = Request(api, headers=headers)
    with urlopen(req, timeout=14) as response:
        info = json.load(response)
    if info.get('draft') or info.get('prerelease'):
        return None
    date = (info.get('published_at') or '')[:10]
    if not date or not info.get('html_url'):
        return None
    return {
        'id': 'release-' + repo.replace('/', '-'),
        'title': f"{repo} — {info.get('tag_name') or info.get('name') or 'latest release'}",
        'category': 'Tool releases',
        'date': date,
        'source': 'GitHub / ' + repo,
        'url': info['html_url'],
        'summary': f"Official release metadata for {repo} ({REPOSITORIES[repo]}). Open the changelog for changes and compatibility notes.",
        'status': 'Published release'
    }


def main():
    data = json.loads(DEST.read_text(encoding='utf-8'))
    standards = [v for v in data.get('items', []) if v.get('category') == 'Standards']
    releases = []
    for repo in REPOSITORIES:
        try:
            release = fetch_latest(repo)
            if release:
                releases.append(release)
                print('OK', repo, release['date'])
        except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as exc:
            print('SKIP', repo, str(exc))
    # Do not pretend a successful feed refresh if every remote source failed.
    if not releases:
        print('No release metadata fetched; keeping the existing updates file.')
        return
    items = sorted(standards + releases, key=lambda x: x.get('date',''), reverse=True)
    output = {'generatedAt': dt.datetime.now(dt.timezone.utc).isoformat(),
              'note': 'Standards cards are curated references. Tool release entries are refreshed from official public GitHub release metadata.',
              'items': items}
    DEST.write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print('Wrote', len(items), 'entries.')

if __name__ == '__main__':
    main()
