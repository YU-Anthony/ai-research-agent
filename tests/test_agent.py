import sqlite3
import pytest
from langgraph.types import Command
from research_agent.arxiv import parse_feed
from research_agent.reasoning import validate
from research_agent.workflow import build_graph
from research_agent.aixiv import AiXivClient


def papers(*args):
    return [{'id': f'2401.{i:05d}', 'title': 'Synthetic test fixture', 'abstract': 'Fixture only',
             'authors': ['Test Author'], 'published': '2024-01-01', 'url': f'https://arxiv.org/abs/2401.{i:05d}'} for i in range(10)]


def analyze(*args):
    return {'gaps': [{'question': 'Missing modality robustness?', 'evidence_ids': ['2401.00000'],
                      'limitation': 'Fixture only; no novelty established'}],
            'hypotheses': [{'statement': f'Dropout improves robustness at rate {i}', 'evidence_ids': ['2401.00000'],
                            'speculation': 'Unverified', 'dataset': 'nuScenes (verify license)',
                            'baseline': 'Concatenation', 'metric': 'mAP',
                            'compute': 'Speculative pilot: 1 GPU, 16 GB VRAM, 2 hours/seed, 3 seeds; full training unestimated',
                            'test': 'Compare paired seeds under held-out sensor dropout'} for i in range(3)]}


def test_arxiv_metadata():
    xml = '''<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>http://arxiv.org/abs/2401.12345v1</id><title>Real metadata fixture</title><summary>Abstract</summary><author><name>A</name></author><published>2024-01-01</published><updated>2024-01-02</updated></entry></feed>'''
    p = parse_feed(xml)[0]
    assert p['authors'] == ['A'] and p['url'] == 'https://arxiv.org/abs/2401.12345v1'
    with pytest.raises(ValueError):
        parse_feed(xml.replace('2401.12345v1', 'error'))


def test_unverified_reference_rejected():
    data = analyze()
    data['hypotheses'][0]['evidence_ids'] = ['invented']
    with pytest.raises(ValueError):
        validate(data, papers())


@pytest.mark.parametrize('decision', ['approve', 'reject', 'revise'])
def test_persistent_approval(tmp_path, decision):
    db = tmp_path / 'state.sqlite'
    config = {'configurable': {'thread_id': 'test'}}
    with sqlite3.connect(db, check_same_thread=False) as conn:
        graph = build_graph(conn, tmp_path, discover=papers, analyze=analyze)
        graph.invoke({'topic': 'fixture', 'max_calls': 2}, config)
        assert graph.get_state(config).next == ('approval',)
        assert not (tmp_path / 'starter.py').exists()
    with sqlite3.connect(db, check_same_thread=False) as conn:
        graph = build_graph(conn, tmp_path, discover=papers, analyze=analyze)
        graph.invoke(Command(resume={'decision': decision, 'feedback': 'Test revision'}), config)
        state = graph.get_state(config)
        assert state.values['decisions'][0]['decision'] == decision
        assert (tmp_path / 'starter.py').exists() == (decision == 'approve')
        assert state.next == (('approval',) if decision == 'revise' else ())


def test_budget_and_invalid_approval(tmp_path):
    with sqlite3.connect(':memory:', check_same_thread=False) as conn:
        graph = build_graph(conn, tmp_path, discover=papers, analyze=analyze)
        config = {'configurable': {'thread_id': 'bad'}}
        graph.invoke({'topic': 'fixture', 'max_calls': 1}, config)
        with pytest.raises(ValueError):
            graph.invoke(Command(resume={'decision': 'automatic'}), config)


def test_aixiv_fails_closed():
    client = AiXivClient()
    with pytest.raises(PermissionError):
        client.submit('draft')
    with pytest.raises(NotImplementedError):
        client.submit('draft', human_approved=True)


def test_exhausted_revision_budget(tmp_path):
    calls = []
    def counted(*args):
        calls.append(1)
        return analyze()
    with sqlite3.connect(':memory:', check_same_thread=False) as conn:
        graph = build_graph(conn, tmp_path, discover=papers, analyze=counted)
        config = {'configurable': {'thread_id': 'budget'}}
        graph.invoke({'topic': 'fixture', 'max_calls': 1}, config)
        with pytest.raises(RuntimeError, match='budget'):
            graph.invoke(Command(resume={'decision': 'revise', 'feedback': 'change'}), config)
        assert len(calls) == 1
        assert graph.get_state(config).values['decisions'][0]['decision'] == 'revise'


def test_draft_has_no_findings(tmp_path):
    from research_agent.artifacts import write_report, draft
    write_report({'topic': 'fixture', 'papers': papers(), 'analysis': analyze()}, tmp_path)
    draft(tmp_path)
    assert 'No verified experiment results supplied' in (tmp_path / 'paper.md').read_text()
    assert 'No verified experiment results supplied' in (tmp_path / 'paper.tex').read_text()


def test_cost_guard_and_supported_model(monkeypatch):
    from research_agent.reasoning import reason, cost_bound
    monkeypatch.setenv('OPENAI_API_KEY', 'test-fixture-not-a-real-key')
    monkeypatch.setenv('RESEARCH_MODEL', 'gpt-4.1-mini')
    assert 0 < cost_bound('short', 3200) < 0.10
    with pytest.raises(ValueError, match='cost estimate'):
        reason('fixture', papers(), max_cost_usd=0.000001)
    monkeypatch.setenv('RESEARCH_MODEL', 'expensive-unsupported-model')
    with pytest.raises(ValueError, match='supports only'):
        reason('fixture', papers())


def test_compute_estimate_required():
    data = analyze()
    del data['hypotheses'][0]['compute']
    with pytest.raises(ValueError, match='Incomplete'):
        validate(data, papers())


def test_arxiv_search_deduplicates_titles(monkeypatch):
    from research_agent import arxiv
    entries = ''.join(f'<entry><id>http://arxiv.org/abs/2401.{i:05d}</id><title>{title}</title><summary>Abstract</summary><author><name>A</name></author><published>2024-01-01</published></entry>' for i, title in enumerate(['Duplicate', 'Duplicate', 'Different']))
    class Response:
        text = f'<feed xmlns="http://www.w3.org/2005/Atom">{entries}</feed>'
        def raise_for_status(self): pass
    class Client:
        def __init__(self, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def get(self, *args, **kwargs):
            assert kwargs['params']['max_results'] == 4
            return Response()
    monkeypatch.setattr(arxiv.httpx, 'Client', Client)
    assert [p['title'] for p in arxiv.search('fixture', 2)] == ['Duplicate', 'Different']


def test_reasoning_one_bounded_call(monkeypatch):
    import json
    from types import SimpleNamespace
    from research_agent import reasoning
    monkeypatch.setenv('OPENAI_API_KEY', 'test-fixture-not-a-real-key')
    monkeypatch.setenv('RESEARCH_MODEL', 'gpt-4.1-mini')
    calls = []
    def create(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(choices=[SimpleNamespace(finish_reason='stop',
            message=SimpleNamespace(content=json.dumps(analyze())))],
            usage=SimpleNamespace(prompt_tokens=100, completion_tokens=200))
    def client(**kwargs):
        assert kwargs['base_url'] == 'https://api.openai.com/v1'
        assert kwargs['max_retries'] == 0
        assert not kwargs['http_client'].follow_redirects
        return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
    monkeypatch.setattr(reasoning, 'OpenAI', client)
    result = reasoning.reason('fixture', papers())
    assert len(calls) == 1
    assert calls[0]['max_completion_tokens'] == 3200
    assert calls[0]['model'] == 'gpt-4.1-mini'
    assert result['model_usage']['estimated_cost_usd'] < 0.10
