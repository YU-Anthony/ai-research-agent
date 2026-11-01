"""Offline approval demonstration with synthetic metadata, never real research evidence."""
import sqlite3
import tempfile
from pathlib import Path
from langgraph.types import Command
from research_agent.workflow import build_graph


def discover(*_):
    return [{'id': f'fixture-{i}', 'title': 'SYNTHETIC demonstration', 'abstract': 'Not a real paper',
             'authors': ['Fixture'], 'published': 'N/A', 'url': 'N/A'} for i in range(10)]


def analyze(*_):
    return {'gaps': [{'question': 'DEMO ONLY', 'evidence_ids': ['fixture-0'], 'limitation': 'Synthetic data'}],
            'hypotheses': [{'statement': f'DEMO hypothesis {i}', 'evidence_ids': ['fixture-0'],
                            'speculation': 'Unverified demonstration', 'dataset': 'Human-selected data',
                            'baseline': 'Fusion baseline', 'metric': 'mAP', 'compute': 'Synthetic estimate only: 1 GPU, 16 GB, 2 hours/seed, 3 seeds', 'test': 'Compare held-out scores'} for i in range(3)]}


with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    with sqlite3.connect(root / 'demo.sqlite', check_same_thread=False) as conn:
        graph = build_graph(conn, root, discover=discover, analyze=analyze)
        config = {'configurable': {'thread_id': 'offline-demo'}}
        graph.invoke({'topic': 'SYNTHETIC DEMO', 'max_calls': 1}, config)
        assert graph.get_state(config).next == ('approval',)
        print('Paused before planning; no experiment executed.')
        # This explicit fixture decision demonstrates resume, not approval of any real experiment.
        graph.invoke(Command(resume={'decision': 'approve', 'feedback': 'Synthetic demo only'}), config)
        print(graph.get_state(config).values['status'])
        assert (root / 'starter.py').exists()
