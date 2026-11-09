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
        if req.method == 'GET' and req.url.path.endswith('/collections'):
            return httpx.Response(200, json=[])
        if req.url.path.endswith('/items/top'):
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


def test_separate_operations_use_fresh_tokens():
    clock = FakeClock()
    tokens = []
    def handler(req):
        tokens.append(req.headers['Zotero-Write-Token'])
        return httpx.Response(200, json={'successful': {'0': {'key': 'saved'}}})
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        api = Zotero(client, '123', 'user', 'fake', clock=clock.time, sleep=clock.sleep)
        api.request('/collections', [{'name': 'same'}])
        api.request('/collections', [{'name': 'same'}])
    assert len(tokens[0]) == 32
    assert tokens[0] != tokens[1]


def test_item_412_is_only_success_after_remote_confirmation():
    clock = FakeClock()
    methods = []
    def handler(req):
        methods.append(req.method)
        if req.method == 'POST':
            return httpx.Response(412, text='untrusted provider body')
        return httpx.Response(200, json=[] if len(methods) == 1 else [
            {'data': {'url': 'https://arxiv.org/abs/2601.12345'}}])
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        api = Zotero(client, '123', 'user', 'fake', clock=clock.time, sleep=clock.sleep)
        assert api.save(PAPER, {n: n for n in categories(PAPER)}) == 'existing'
    assert methods == ['GET', 'POST', 'GET']


def test_unconfirmed_item_412_stays_pending_without_rewrite():
    from research_agent.zotero import ZoteroPreconditionError
    clock = FakeClock()
    methods = []
    def handler(req):
        methods.append(req.method)
        return httpx.Response(412, text='sensitive') if req.method == 'POST' else httpx.Response(200, json=[])
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        api = Zotero(client, '123', 'user', 'fake', clock=clock.time, sleep=clock.sleep)
        with pytest.raises(ZoteroPreconditionError, match='POST /items') as error:
            api.save(PAPER, {n: n for n in categories(PAPER)})
    assert 'sensitive' not in str(error.value)
    assert methods == ['GET', 'POST', 'GET']


def test_collection_412_reconciles_existing_collection():
    clock = FakeClock()
    calls = []
    names = categories(PAPER)
    def handler(req):
        calls.append((req.method, req.url.path))
        if req.url.path.endswith('/collections'):
            if req.method == 'POST':
                return httpx.Response(412)
            return httpx.Response(200, json=[{'key': str(i), 'data': {'name': n, 'parentCollection': False}}
                                             for i, n in enumerate(names)])
        if req.method == 'GET':
            return httpx.Response(200, json=[])
        return httpx.Response(200, json={'successful': {'0': {'key': 'saved'}}})
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        api = Zotero(client, '123', 'user', 'fake', clock=clock.time, sleep=clock.sleep)
        assert api.save(PAPER, {}) == 'created'
    assert sum(method == 'POST' and path.endswith('/collections') for method, path in calls) == 1


def test_paginated_snapshot_finds_item_even_when_search_would_miss():
    clock = FakeClock()
    reads = []
    def handler(req):
        assert req.method == 'GET', 'Existing item must never be written again'
        assert req.url.path.endswith('/items/top')
        assert 'q' not in req.url.params
        reads.append(int(req.url.params['start']))
        if reads[-1] == 0:
            return httpx.Response(200, json=[{'data': {'title': 'other'}} for _ in range(100)])
        return httpx.Response(200, json=[{'data': {'archiveID': '2601.12345v1'}}])
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        api = Zotero(client, '123', 'user', 'fake', clock=clock.time, sleep=clock.sleep)
        assert api.save(PAPER, {}) == 'existing'
        assert api.save(PAPER, {}) == 'existing'
    assert reads == [0, 100]


@pytest.mark.parametrize('data', [
    {'url': 'https://arxiv.org/pdf/2601.12345v3.pdf'},
    {'archiveID': '2601.12345'},
    {'extra': 'arXiv: 2601.12345v1'},
    {'DOI': '10.48550/arXiv.2601.12345'},
    {'title': PAPER['title'].upper(), 'creators': [{'creatorType': 'author', 'name': 'A. Researcher'}]},
])
def test_identity_matching_without_search(data):
    from research_agent.zotero import matches_paper
    assert matches_paper(data, PAPER)


def test_different_explicit_arxiv_id_is_not_a_title_match():
    from research_agent.zotero import matches_paper
    data = {'archiveID': '2601.12346', 'title': PAPER['title'],
            'creators': [{'creatorType': 'author', 'name': 'A. Researcher'}]}
    assert not matches_paper(data, PAPER)


def test_title_alone_does_not_merge_different_authors():
    from research_agent.zotero import matches_paper
    assert not matches_paper({'title': PAPER['title'], 'creators': [
        {'creatorType': 'author', 'name': 'Different Author'}]}, PAPER)


def test_github_registry_contains_only_confirmed_records_and_no_secret():
    from research_agent.zotero import sync_registry
    state = {'papers': {'2601.12345': PAPER}, 'zotero': {
        'https://api.zotero.org/users/123': {'synced': {
            '2601.12345': {'status': 'existing', 'item_key': 'ITEMKEY1'}}, 'not_before': 0}}}
    registry = sync_registry(state)
    entries = next(iter(registry['libraries'].values()))
    assert entries == [{'arxiv_id': '2601.12345', 'title': PAPER['title'],
                        'url': 'https://arxiv.org/abs/2601.12345',
                        'zotero_item_key': 'ITEMKEY1', 'status': 'existing'}]
    assert 'api.zotero.org/users/123' not in json.dumps(registry)
