"""Verify a completed live run offline, without resuming or making API requests."""
import argparse
import json
import sqlite3
from pathlib import Path
from research_agent.reasoning import validate
from research_agent.workflow import build_graph


def verify(root: Path):
    papers = json.loads((root / 'papers.json').read_text())
    analysis = json.loads((root / 'analysis.json').read_text())
    assert len(papers) == len({p['id'] for p in papers}) == 10
    assert len({p['title'].casefold() for p in papers}) == 10
    for paper in papers:
        assert all(paper[k] for k in ('title', 'authors', 'abstract', 'published', 'url', 'retrieved_at'))
        assert paper['source'] == 'https://export.arxiv.org/api/query'
        assert paper['url'] == 'https://arxiv.org/abs/' + paper['id']
    validate(analysis, papers)
    # Reopen persisted state in a new connection/process; never approve the live run.
    with sqlite3.connect(root / 'state.sqlite', check_same_thread=False) as conn:
        graph = build_graph(conn, root)
        state = graph.get_state({'configurable': {'thread_id': root.name}})
        assert state.next == ('approval',)
        assert state.values['status'] == 'awaiting_approval'
        assert state.values['calls_used'] == 1
        assert state.values['papers'] == papers
        assert state.values['analysis'] == analysis
        assert state.values.get('decisions', []) == []
    assert not (root / 'starter.py').exists()
    assert not (root / 'experiment-plan.md').exists()
    assert analysis['model_usage']['estimated_cost_usd'] < 0.10
    report = (root / 'research-gap.md').read_text()
    assert all(p['url'] in report for p in papers)
    checks = {'papers': 10, 'hypotheses': 3, 'approval_pending': True,
              'state_reopened': True, 'experiments_executed': False,
              'model_calls': 1, 'estimated_cost_usd': analysis['model_usage']['estimated_cost_usd']}
    print(json.dumps(checks, indent=2))
    return checks


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_directory', type=Path)
    verify(parser.parse_args().run_directory)
