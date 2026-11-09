"""Synchronize ranked, verified arXiv metadata to Zotero; no model calls or PDFs."""
import argparse
from contextlib import nullcontext
import secrets
import json
import os
import math
import time
from email.utils import parsedate_to_datetime
from pathlib import Path

import httpx
from .monitor import read_state, stable_id, atomic_json


class ZoteroError(ValueError):
    pass


class ZoteroPreconditionError(ZoteroError):
    """A rejected write must be reconciled before another write is attempted."""
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
    def __init__(self, client, library, kind, key, *, clock=time.time, sleep=time.sleep,
                 interval=1.0, max_wait=60, max_retries=2):
        if not library.isdigit() or kind not in ('user', 'group') or not key:
            raise ZoteroError('Configure ZOTERO_API_KEY, numeric ZOTERO_LIBRARY_ID and user/group library type')
        self.clock, self.sleep = clock, sleep
        self.interval, self.max_wait, self.max_retries = interval, max_wait, max_retries
        self.not_before = 0.0
        self.waited = 0.0
        self.client = client
        self.base = f'https://api.zotero.org/{"users" if kind == "user" else "groups"}/{library}'
        self.headers = {'Zotero-API-Key': key, 'Zotero-API-Version': '3'}

    def request(self, path, data=None, params=None):
        headers = dict(self.headers)
        if data is not None:
            # Tokens identify one operation, not content across separate runs.
            # Keep this token unchanged only for the 429 retries below.
            headers['Zotero-Write-Token'] = secrets.token_hex(16)
        for attempt in range(self.max_retries + 1):
            delay = max(0, self.not_before - self.clock())
            if self.waited + delay > self.max_wait:
                raise ZoteroError('Zotero cooldown exceeds run wait budget; pending papers retained for next sync')
            while delay > 0:
                chunk = min(delay, 30)
                self.sleep(chunk)
                self.waited += chunk
                delay = max(0, self.not_before - self.clock())
            response = self.client.request('POST' if data is not None else 'GET', self.base + path,
                                           headers=headers, json=data, params=params)
            now = self.clock()
            delays = [self.interval]
            for name in ('Backoff', 'Retry-After'):
                raw = response.headers.get(name)
                if raw is None:
                    continue
                try:
                    seconds = float(raw)
                except ValueError:
                    try:
                        seconds = parsedate_to_datetime(raw).timestamp() - now
                    except (ValueError, TypeError, OverflowError):
                        continue
                if math.isfinite(seconds):
                    delays.append(max(0, seconds))
            if response.status_code == 429:
                delays.append(5 * 2 ** attempt)
            self.not_before = now + max(delays)
            if response.status_code != 429:
                break
            if attempt == self.max_retries:
                raise ZoteroError('Zotero HTTP 429 after bounded retries; pending papers retained for next sync')
        if response.status_code == 412 and data is not None:
            raise ZoteroPreconditionError(f'Zotero HTTP 412 on POST {path}; verify remote state before retrying')
        if response.status_code >= 300:
            raise ZoteroError(f'Zotero HTTP {response.status_code} on {"POST" if data is not None else "GET"} {path}; no automatic retry')
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
        def exists():
            rows = self.request('/items', params={'q': identifier, 'qmode': 'everything', 'limit': 100})
            for row in rows:
                data = row['data']
                if any(identifier in data.get(k, '') for k in ('url', 'extra')):
                    return True
            return False

        if exists():
            return 'existing'
        keys = []
        for name in categories(paper):
            if name not in collections:
                try:
                    result = self.request('/collections', [{'name': name, 'parentCollection': False}])
                    collections[name] = next(iter(result['successful'].values()))['key']
                except ZoteroPreconditionError:
                    # Reconcile a possible prior creation; never assume 412 means success.
                    collections.update(self.collections())
                    if name not in collections:
                        raise
            keys.append(collections[name])
        item = {'itemType': 'preprint', 'title': paper['title'],
                'creators': [{'creatorType': 'author', 'name': name} for name in paper['authors']],
                'abstractNote': paper.get('abstract', ''), 'date': paper['published'][:10],
                'url': f'https://arxiv.org/abs/{identifier}', 'archive': 'arXiv',
                'archiveID': identifier, 'extra': f'arXiv: {identifier}',
                'tags': [{'tag': '待阅读'}, {'tag': '自动分类待复核'}], 'collections': keys}
        try:
            self.request('/items', [item])
        except ZoteroPreconditionError:
            if exists():
                return 'existing'
            raise
        return 'created'


def synchronize(state_path, output, client=None):
    state = read_state(state_path)
    # Replay all selected history, so a failed sync is retried despite monitor seen-state.
    ids = {stable_id(row['id']) for run in state['history'].values() for row in run['papers']}
    result = {'status': 'success', 'created': 0, 'existing': 0, 'cached': 0, 'pending': len(ids)}
    with (httpx.Client(timeout=30, follow_redirects=False) if client is None else nullcontext(client)) as transport:
        api = Zotero(transport, os.environ.get('ZOTERO_LIBRARY_ID', '').strip(),
                     os.environ.get('ZOTERO_LIBRARY_TYPE', 'user').strip(), os.environ.get('ZOTERO_API_KEY', ''))
        # Namespace by destination, so changing libraries does not suppress uploads.
        destinations = state.setdefault('zotero', {})
        cache = destinations.setdefault(api.base, {'synced': {}, 'not_before': 0})
        if not isinstance(cache.get('synced'), dict):
            raise ZoteroError('Invalid Zotero sync state; refusing to reset it')
        api.not_before = float(cache.get('not_before', 0))
        pending = ids - set(cache['synced'])
        result.update(cached=len(ids) - len(pending), pending=len(pending))
        try:
            collections = api.collections() if pending else {}
            for identifier in sorted(pending):
                paper = state['papers'].get(identifier)
                if not paper:
                    raise ZoteroError('Selected paper metadata missing from persistent state')
                outcome = api.save(paper, collections)
                result[outcome] += 1
                cache['synced'][identifier] = {'status': outcome}
                result['pending'] -= 1
                # Checkpoint every confirmed item, even if a later request fails.
                cache['not_before'] = api.not_before
                atomic_json(state_path, state)
        except Exception as exc:
            result.update(status='failed', error_type=type(exc).__name__,
                          reason=str(exc) if isinstance(exc, ZoteroError) else 'External failure; details suppressed to protect credentials')
            raise
        finally:
            cache['not_before'] = api.not_before
            atomic_json(state_path, state)
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
        if args.output.exists():
            previous = json.loads(args.output.read_text())
            result = {**previous, **result}
        atomic_json(args.output, result)
        print(json.dumps(result))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
