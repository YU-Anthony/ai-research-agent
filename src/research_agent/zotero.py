"""Synchronize ranked, verified arXiv metadata to Zotero; no model calls or PDFs."""
import argparse
import hashlib
import json
import os
from pathlib import Path

import httpx
from .monitor import read_state, stable_id, atomic_json


class ZoteroError(ValueError):
    pass


def categories(paper):
    text = (paper['title'] + ' ' + paper.get('abstract', '')).lower()
    rules = {
        '多模态学习与推理': ('multimodal', 'vision-language'),
        '驾驶员行为与意图预测': ('driver behavior', 'driving behavior', 'intention', 'takeover'),
        '驾驶员状态与情绪': ('emotion', 'fatigue', 'drowsiness', 'driver state'),
        '生成式车内助手': ('in-vehicle assistant', 'in-car assistant', 'conversational'),
        '可解释与可信 AI': ('explainab', 'uncertainty', 'interpretab', 'trustworthy'),
        '数据集与评测基准': ('dataset', 'benchmark'),
    }
    return [name for name, words in rules.items() if any(w in text for w in words)] or ['待筛选']


class Zotero:
    def __init__(self, client, library, kind, key):
        if not library.isdigit() or kind not in ('user', 'group') or not key:
            raise ZoteroError('Configure ZOTERO_API_KEY, numeric ZOTERO_LIBRARY_ID and user/group library type')
        self.client = client
        self.base = f'https://api.zotero.org/{"users" if kind == "user" else "groups"}/{library}'
        self.headers = {'Zotero-API-Key': key, 'Zotero-API-Version': '3'}

    def request(self, path, data=None, params=None):
        headers = dict(self.headers)
        if data is not None:
            headers['Zotero-Write-Token'] = hashlib.sha256(
                (self.base + path + json.dumps(data, sort_keys=True)).encode()).hexdigest()[:32]
        response = self.client.request('POST' if data is not None else 'GET', self.base + path,
                                       headers=headers, json=data, params=params)
        if response.status_code >= 300:
            raise ZoteroError(f'Zotero HTTP {response.status_code}; no automatic retry')
        result = response.json()
        if data is not None and (result.get('failed') or not result.get('successful')):
            raise ZoteroError('Zotero rejected write; inspect permissions and metadata')
        return result

    def collections(self):
        result = {}
        start = 0
        while True:
            rows = self.request('/collections', params={'limit': 100, 'start': start})
            for row in rows:
                if not row['data'].get('parentCollection'):
                    result[row['data']['name']] = row['key']
            if len(rows) < 100:
                return result
            start += 100

    def save(self, paper, collections):
        identifier = stable_id(paper['id'])
        rows = self.request('/items', params={'q': identifier, 'qmode': 'everything', 'limit': 100})
        for row in rows:
            data = row['data']
            if any(identifier in data.get(k, '') for k in ('url', 'extra')):
                return 'existing'
        keys = []
        for name in categories(paper):
            if name not in collections:
                result = self.request('/collections', [{'name': name, 'parentCollection': False}])
                collections[name] = next(iter(result['successful'].values()))['key']
            keys.append(collections[name])
        item = {'itemType': 'preprint', 'title': paper['title'],
                'creators': [{'creatorType': 'author', 'name': name} for name in paper['authors']],
                'abstractNote': paper.get('abstract', ''), 'date': paper['published'][:10],
                'url': f'https://arxiv.org/abs/{identifier}', 'archive': 'arXiv',
                'archiveID': identifier, 'extra': f'arXiv: {identifier}',
                'tags': [{'tag': '待阅读'}, {'tag': '自动分类待复核'}], 'collections': keys}
        self.request('/items', [item])
        return 'created'


def synchronize(state_path, output, client=None):
    state = read_state(state_path)
    # Replay all selected history, so a failed sync is retried despite monitor seen-state.
    ids = {stable_id(row['id']) for run in state['history'].values() for row in run['papers']}
    result = {'status': 'success', 'created': 0, 'existing': 0}
    with httpx.Client(timeout=30, follow_redirects=False) if client is None else client as transport:
        api = Zotero(transport, os.environ.get('ZOTERO_LIBRARY_ID', '').strip(),
                     os.environ.get('ZOTERO_LIBRARY_TYPE', 'user').strip(), os.environ.get('ZOTERO_API_KEY', ''))
        collections = api.collections()
        for identifier in sorted(ids):
            paper = state['papers'].get(identifier)
            if not paper:
                raise ZoteroError('Selected paper metadata missing from persistent state')
            result[api.save(paper, collections)] += 1
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', type=Path, default=Path('monitor-state/state.json'))
    parser.add_argument('--output', type=Path, default=Path('reports/daily/zotero-status.json'))
    args = parser.parse_args()
    try:
        print(json.dumps(synchronize(args.state, args.output)))
    except Exception as exc:
        result = {'status': 'failed', 'error_type': type(exc).__name__,
                  'reason': str(exc) if isinstance(exc, ZoteroError) else 'External failure; details suppressed to protect credentials'}
        atomic_json(args.output, result)
        print(json.dumps(result))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
