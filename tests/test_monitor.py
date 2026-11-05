import json
import pytest
from research_agent import monitor


def papers(n=6):
    return [{'id': f'2601.{i:05d}v1', 'title': f'Fixture {i}', 'authors': ['Fixture'],
             'abstract': 'Fixture abstract', 'published': '2026-01-01T00:00:00Z',
             'url': f'https://arxiv.org/abs/2601.{i:05d}v1'} for i in range(n)]


def rows(ps):
    return [{'id': p['id'], 'contribution': 'Reported fixture claim',
             'limitation': 'Tentative fixture limitation', 'gap': 'Speculative fixture gap'} for p in ps]


def synthesis(ps):
    refs = [ps[0]['id']]
    return {'trends': [{'finding': 'Fixture trend', 'uncertainty': 'Abstract only', 'evidence_ids': refs}],
            'comparisons': [{'comparison': 'Fixture comparison', 'limitation': 'Not controlled', 'evidence_ids': refs}],
            'ideas': [{**{k: 'Untested fixture hypothesis' for k in ['question', 'hypothesis', 'method', 'datasets',
                'baselines', 'metrics', 'compute', 'risk', 'novelty_check', 'priority_rationale']},
                'evidence_ids': refs} for _ in range(2)]}


def test_stable_versions():
    assert monitor.stable_id('2601.00001v2') == monitor.stable_id('2601.00001v1')
    assert monitor.stable_id('cs/9901001v3') == 'cs/9901001'
    with pytest.raises(ValueError): monitor.stable_id('invented')


def test_two_runs_deduplicate_and_no_call_when_empty(tmp_path):
    calls = []
    def rank(ps, *args):
        calls.append(1)
        return rows(ps), {}, synthesis(ps)
    state = tmp_path / 'state.json'
    result = monitor.run(state, tmp_path / 'first', discover=lambda _: papers(), rank=rank)
    assert result['selected'] == 6
    later = papers()
    for p in later: p['id'] = p['id'].replace('v1', 'v2')
    result = monitor.run(state, tmp_path / 'second', discover=lambda _: later, rank=rank)
    assert result['selected'] == 0 and len(calls) == 1
    assert len(monitor.read_state(state)['seen']) == 6
    assert 'No new matching papers' in (tmp_path / 'second/weekly-digest.md').read_text()


def test_invalid_model_ids_rejected():
    data = rows(papers())
    data[0]['id'] = 'invented'
    with pytest.raises(ValueError): monitor.validate_ranking({'papers': data}, papers())
    data = rows(papers()); data[1] = data[0]
    assert len(monitor.validate_ranking({'papers': data}, papers())) == 5
    with pytest.raises(ValueError): monitor.validate_ranking({'papers': [data[0]]*6}, papers())


def test_small_window_and_failed_model_does_not_mark_seen(tmp_path):
    state = tmp_path / 'state.json'
    monitor.run(state, tmp_path / 'small', discover=lambda _: papers(2), rank=lambda ps,*_: (rows(ps), {}, synthesis(ps)))
    assert 'Fewer than five' in (tmp_path / 'small/weekly-digest.md').read_text()
    def fail(*args): raise RuntimeError('fixture failure')
    before = state.read_text()
    with pytest.raises(RuntimeError): monitor.run(state, tmp_path / 'bad', discover=lambda _: papers(8), rank=fail)
    assert monitor.read_state(state)['seen'] == json.loads(before)['seen']
    assert len(monitor.read_state(state)['papers']) == 8


def test_fail_closed_budget_and_pricing(tmp_path, monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'fixture-not-a-secret')
    monkeypatch.delenv('LITERATURE_PRICING_CONFIRMED', raising=False)
    with pytest.raises(ValueError, match='Confirm'): monitor.pricing()
    monkeypatch.setenv('LITERATURE_PRICING_CONFIRMED', 'true')
    monkeypatch.setenv('LITERATURE_INPUT_USD_PER_M', '0.4')
    monkeypatch.setenv('LITERATURE_OUTPUT_USD_PER_M', '1.6')
    state = {'version':1,'seen':{},'requests':{}}
    for budget in [0.000001, float('nan'), .21]:
        with pytest.raises(ValueError): monitor.analyze(papers(), budget, state, tmp_path/'state', 'budget')
    assert not state['requests']
    assert monitor.estimate('fixture', 3500, [.4,1.6]) < .20


def test_failure_reporting_redacts_exception(tmp_path, monkeypatch):
    def fail(*a, **kw): raise RuntimeError('secret-must-not-appear')
    monkeypatch.setattr(monitor, 'run', fail)
    with pytest.raises(SystemExit): monitor.main(['--output',str(tmp_path)])
    status=(tmp_path/'status.json').read_text()
    assert 'secret-must-not-appear' not in status
    assert json.loads(status)['error_type'] == 'RuntimeError'


def test_corrupt_state_rejected(tmp_path):
    path=tmp_path/'state'; path.write_text('{"version":2}')
    with pytest.raises(ValueError): monitor.read_state(path)


def test_state_branch_roundtrip_without_checkout_changes(tmp_path):
    import subprocess
    import sys
    from pathlib import Path
    def git(*args):
        return subprocess.check_output(['git',*args],cwd=tmp_path).decode().strip()
    git('init','--bare',str(tmp_path/'remote.git'))
    local=tmp_path/'local'; local.mkdir()
    subprocess.run(['git','init',str(local)],check=True,capture_output=True)
    subprocess.run(['git','-C',str(local),'remote','add','origin',str(tmp_path/'remote.git')],check=True)
    state=tmp_path/'state.json'
    state.write_text(json.dumps({'version':1,'seen':{'2601.00001':{}},'requests':{}}))
    helper=Path(__file__).resolve().parents[1]/'examples/monitor_state.py'
    for mode in ['save','restore']:
        if mode=='restore': state.unlink()
        subprocess.run([sys.executable,str(helper),mode,str(state)],cwd=local,check=True,capture_output=True)
    assert '2601.00001' in monitor.read_state(state)['seen']
    assert subprocess.check_output(['git','status','--porcelain'],cwd=local)==b''


def test_one_request_and_usage_retained_on_bad_response(tmp_path, monkeypatch):
    from types import SimpleNamespace
    monkeypatch.setenv('OPENAI_API_KEY', 'fixture-not-a-secret')
    monkeypatch.setenv('LITERATURE_PRICING_CONFIRMED', 'true')
    monkeypatch.setenv('LITERATURE_INPUT_USD_PER_M', '1')
    monkeypatch.setenv('LITERATURE_OUTPUT_USD_PER_M', '4')
    calls=[]
    def create(**kw):
        calls.append(kw)
        assert kw['response_format']['json_schema']['strict']
        assert kw['max_completion_tokens']==6500
        return SimpleNamespace(choices=[SimpleNamespace(finish_reason='stop',message=SimpleNamespace(content='{"papers":[]}'))],
            usage=SimpleNamespace(prompt_tokens=100,completion_tokens=10))
    def client(**kw):
        assert kw['max_retries']==0 and not kw['http_client'].follow_redirects
        return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
    monkeypatch.setattr(monitor,'OpenAI',client)
    path=tmp_path/'state'
    state={'version':1,'seen':{},'requests':{}}
    with pytest.raises(ValueError): monitor.analyze(papers(),.20,state,path,'once')
    saved=monitor.read_state(path)
    assert saved['requests']['once']['completion_tokens']==10
    assert not saved['seen']
    with pytest.raises(ValueError,match='already reserved'):
        monitor.analyze(papers(),.20,saved,path,'once')
    assert len(calls)==1


@pytest.mark.parametrize('stamp,expected',[
    ('2026-07-06T13:00:00+00:00',True),('2026-07-06T14:00:00+00:00',False),
    ('2026-11-02T14:00:00+00:00',True),('2026-11-02T13:00:00+00:00',False),
    ('2026-11-03T14:00:00+00:00',True),
    ('2026-11-07T14:00:00+00:00',True)])
def test_new_york_schedule_across_dst(stamp,expected):
    from datetime import datetime
    from research_agent.schedule import should_monitor
    assert should_monitor('schedule',datetime.fromisoformat(stamp), '0 ' + str(datetime.fromisoformat(stamp).hour) + ' * * *') is expected
    assert should_monitor('workflow_dispatch',datetime.fromisoformat(stamp))


def test_research_proposals_must_cite_selected_evidence():
    selected = rows(papers())
    data = synthesis(papers())
    assert len(monitor.validate_synthesis(data, selected)['ideas']) == 2
    data['ideas'][0]['evidence_ids'] = ['invented']
    with pytest.raises(ValueError, match='unknown'):
        monitor.validate_synthesis(data, selected)
    data = synthesis(papers())
    del data['ideas'][0]['compute']
    with pytest.raises(ValueError, match='Incomplete'):
        monitor.validate_synthesis(data, selected)


def test_library_history_and_literal_search(tmp_path):
    from research_agent.library import sync, search
    state = {'papers': {'2601.00000': papers(1)[0]}, 'history': {'first': {'ideas': ['fixture']}}}
    db = tmp_path/'library.sqlite'
    sync(state, db)
    sync(state, db)
    assert len(search(db, 'Fixture')) == 1
    assert search(db, "%' OR 1=1 --") == []
    import sqlite3
    with sqlite3.connect(db) as conn:
        assert conn.execute('SELECT count(*) FROM research_runs').fetchone()[0] == 1


def test_report_and_portable_history_include_proposals(tmp_path):
    state_path = tmp_path/'state.json'
    monitor.run(state_path,tmp_path/'report',discover=lambda _:papers(),
        rank=lambda ps,*args:(rows(ps), {}, synthesis(ps)),run_id='research')
    state = monitor.read_state(state_path)
    assert len(state['history']['research']['synthesis']['ideas']) == 2
    assert len(state['papers']) == 6
    text = (tmp_path/'report/weekly-digest.md').read_text()
    assert 'awaiting human review' in text and 'No experiment or publication is authorized' in text
    assert (tmp_path/'library.sqlite').exists()
