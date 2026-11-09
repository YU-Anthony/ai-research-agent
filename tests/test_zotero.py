import json
from datetime import datetime
import httpx
import pytest
from research_agent.zotero import Zotero, ZoteroError, categories
from research_agent.schedule import should_monitor

PAPER = {'id': '2601.12345v2', 'title': 'Multimodal driver behavior benchmark',
         'abstract': 'Dataset with uncertainty estimation.', 'authors': ['A. Researcher'],
         'published': '2026-01-20T00:00:00Z'}


def test_delayed_daily_trigger_and_dst():
    assert should_monitor('schedule', datetime.fromisoformat('2026-11-04T22:07:00+00:00'), '0 14 * * *')
    assert not should_monitor('schedule', datetime.fromisoformat('2026-11-04T22:07:00+00:00'), '0 13 * * *')
    assert should_monitor('schedule', datetime.fromisoformat('2026-07-08T23:00:00+00:00'), '0 13 * * *')


def test_duplicate_is_not_written():
    calls = []
    def handler(req):
        calls.append(req.method)
        return httpx.Response(200, json=[{'data': {'url': 'https://arxiv.org/abs/2601.12345v1'}}])
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        assert Zotero(client, '123', 'user', 'fake').save(PAPER, {}) == 'existing'
    assert calls == ['GET']


def test_create_with_multiple_collections():
    writes = []
    def handler(req):
        if req.method == 'GET':
            return httpx.Response(200, json=[])
        payload = json.loads(req.content)
        writes.append((req.url.path, payload))
        return httpx.Response(200, json={'successful': {'0': {'key': 'NEWKEY'}}})
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        assert Zotero(client, '123', 'user', 'fake').save(PAPER, {}) == 'created'
    item = writes[-1][1][0]
    assert item['url'] == 'https://arxiv.org/abs/2601.12345'
    assert len(item['collections']) == 4
    assert item['creators'][0]['name'] == 'A. Researcher'


def test_auth_failure_does_not_expose_response():
    with httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(403, text='sensitive'))) as client:
        with pytest.raises(ZoteroError, match='HTTP 403') as err:
            Zotero(client, '123', 'user', 'fake').save(PAPER, {})
    assert 'sensitive' not in str(err.value)


def test_fallback_classification():
    assert categories({'title': 'Unrelated topic'}) == ['待筛选']


def test_sync_history_retries_and_second_run_deduplicates(tmp_path, monkeypatch):
    from research_agent.zotero import synchronize
    from research_agent.monitor import atomic_json
    for name, value in [('ZOTERO_API_KEY', 'fake'), ('ZOTERO_LIBRARY_ID', '123'), ('ZOTERO_LIBRARY_TYPE', 'user')]:
        monkeypatch.setenv(name, value)
    state = {'version': 1, 'seen': {'2601.12345': {}}, 'requests': {},
             'papers': {'2601.12345': PAPER}, 'history': {'previous': {'papers': [{'id': PAPER['id']}]}}}
    path = tmp_path / 'state.json'
    atomic_json(path, state)
    stored = []
    def handler(req):
        if req.url.path.endswith('/collections'):
            return httpx.Response(200, json=[{'key': str(i), 'data': {'name': n, 'parentCollection': False}} for i, n in enumerate(categories(PAPER))])
        if req.method == 'GET':
            return httpx.Response(200, json=stored)
        item = json.loads(req.content)[0]
        stored.append({'data': item})
        return httpx.Response(200, json={'successful': {'0': {'key': 'saved'}}})
    def client():
        return httpx.Client(transport=httpx.MockTransport(handler))
    first = synchronize(path, tmp_path / 'first.json', client())
    second = synchronize(path, tmp_path / 'second.json', client())
    assert first['created'] == 1
    assert second['cached'] == 1
    assert second['existing'] == 0
    assert len(stored) == 1


class FakeClock:
    def __init__(self):
        self.now = 1000.0
        self.sleeps = []

    def time(self):
        return self.now

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


def test_429_retries_respect_headers_and_reuse_write_token():
    clock = FakeClock()
    requests = []
    def handler(req):
        requests.append(req)
        if len(requests) == 1:
            return httpx.Response(429, headers={'Retry-After': '7', 'Backoff': '9'})
        return httpx.Response(200, json={'successful': {'0': {'key': 'saved'}}})
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        api = Zotero(client, '123', 'user', 'fake', clock=clock.time, sleep=clock.sleep)
        api.request('/items', [{'title': 'test'}])
    assert clock.sleeps == [9]
    assert len(requests) == 2
    assert requests[0].headers['Zotero-Write-Token'] == requests[1].headers['Zotero-Write-Token']
    assert requests[0].content == requests[1].content


def test_success_backoff_applies_before_next_request():
    clock = FakeClock()
    calls = []
    def handler(req):
        calls.append(req)
        return httpx.Response(200, json=[], headers={'Backoff': '4'})
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        api = Zotero(client, '123', 'user', 'fake', clock=clock.time, sleep=clock.sleep)
        api.request('/items')
        api.request('/items')
    assert clock.sleeps == [4]


def test_long_cooldown_is_not_shortened_or_retried():
    clock = FakeClock()
    calls = []
    def handler(req):
        calls.append(req)
        return httpx.Response(429, headers={'Retry-After': '3600'})
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        api = Zotero(client, '123', 'user', 'fake', clock=clock.time, sleep=clock.sleep)
        with pytest.raises(ZoteroError, match='cooldown'):
            api.request('/items')
    assert len(calls) == 1
    assert clock.sleeps == []
    assert api.not_before == 4600


def test_repeated_429_is_bounded():
    clock = FakeClock()
    calls = []
    def handler(req):
        calls.append(req)
        return httpx.Response(429)
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        api = Zotero(client, '123', 'user', 'fake', clock=clock.time, sleep=clock.sleep)
        with pytest.raises(ZoteroError, match='bounded retries'):
            api.request('/items')
    assert len(calls) == 3
    assert clock.sleeps == [5, 10]


def test_partial_progress_persisted_before_failure(tmp_path, monkeypatch):
    from research_agent.zotero import synchronize
    from research_agent.monitor import atomic_json, read_state
    monkeypatch.setenv('ZOTERO_API_KEY', 'fake')
    monkeypatch.setenv('ZOTERO_LIBRARY_ID', '123')
    monkeypatch.setenv('ZOTERO_LIBRARY_TYPE', 'user')
    papers = {f'2601.1234{i}': {**PAPER, 'id': f'2601.1234{i}v1'} for i in [5, 6]}
    state = {'version': 1, 'seen': {}, 'requests': {}, 'papers': papers,
             'history': {'old': {'papers': [{'id': p['id']} for p in papers.values()]}}}
    path, output = tmp_path / 'state.json', tmp_path / 'status.json'
    atomic_json(path, state)
    def handler(req):
        if req.url.path.endswith('/collections'):
            return httpx.Response(200, json=[])
        if '12345' in str(req.url):
            return httpx.Response(200, json=[{'data': {'url': 'https://arxiv.org/abs/2601.12345'}}])
        return httpx.Response(429, headers={'Retry-After': '3600'})
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(ZoteroError, match='cooldown'):
            synchronize(path, output, client)
    cache = next(iter(read_state(path)['zotero'].values()))
    assert set(cache['synced']) == {'2601.12345'}
    assert cache['not_before'] > 0
    result = json.loads(output.read_text())
    assert result['pending'] == 1 and result['existing'] == 1
    assert result['status'] == 'failed'


def test_retry_after_http_date():
    from email.utils import formatdate
    clock = FakeClock()
    count = []
    def handler(req):
        count.append(req)
        if len(count) == 1:
            return httpx.Response(429, headers={'Retry-After': formatdate(1012, usegmt=True)})
        return httpx.Response(200, json=[])
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        Zotero(client, '123', 'user', 'fake', clock=clock.time, sleep=clock.sleep).request('/items')
    assert clock.sleeps == [12]


def test_saved_cooldown_prevents_new_requests(tmp_path, monkeypatch):
    import time
    from research_agent.zotero import synchronize
    from research_agent.monitor import atomic_json
    monkeypatch.setenv('ZOTERO_API_KEY', 'fake')
    monkeypatch.setenv('ZOTERO_LIBRARY_ID', '123')
    monkeypatch.setenv('ZOTERO_LIBRARY_TYPE', 'user')
    state = {'version': 1, 'seen': {}, 'requests': {},
             'papers': {'2601.12345': PAPER},
             'history': {'old': {'papers': [{'id': PAPER['id']}]}},
             'zotero': {'https://api.zotero.org/users/123': {'synced': {}, 'not_before': time.time() + 3600}}}
    path = tmp_path / 'state.json'
    atomic_json(path, state)
    def handler(req):
        pytest.fail('Persisted cooldown must prevent network access')
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(ZoteroError, match='cooldown'):
            synchronize(path, tmp_path / 'status.json', client)
