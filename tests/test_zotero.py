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
    assert second['existing'] == 1
    assert len(stored) == 1
