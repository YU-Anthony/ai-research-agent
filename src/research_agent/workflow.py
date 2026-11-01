"""Durable LangGraph interrupts. Approval never launches an experiment."""
import sqlite3
from typing import TypedDict
from pathlib import Path
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt
from langgraph.checkpoint.sqlite import SqliteSaver
from . import arxiv, artifacts, reasoning


class State(TypedDict, total=False):
    topic: str
    papers: list[dict]
    analysis: dict
    feedback: str
    decisions: list[dict]
    decision: str
    calls_used: int
    max_calls: int
    status: str


def build_graph(connection: sqlite3.Connection, output: Path, *, discover=arxiv.search, analyze=reasoning.reason):
    def discover_node(s):
        papers = discover(s['topic'], 10)
        output.mkdir(parents=True, exist_ok=True)
        import json
        (output / 'papers.json').write_text(json.dumps(papers, indent=2))
        return {'papers': papers, 'status': 'discovered'}

    def reserve(s):
        used = s.get('calls_used', 0)
        if used >= s.get('max_calls', 1):
            raise RuntimeError('Model-call budget exhausted')
        return {'calls_used': used + 1}

    def do_analyze(s):
        # The reservation node persists before any paid operation.
        result = analyze(s['topic'], s['papers'], s.get('feedback', ''))
        return {'analysis': reasoning.validate(result, s['papers']), 'status': 'awaiting_approval'}

    def report(s):
        artifacts.write_report(s, output)
        return {}

    def approval(s):
        answer = interrupt({'message': 'Review research-gap.md. Approve planning, reject, or revise; no experiment will run.',
                            'allowed': ['approve', 'reject', 'revise'], 'analysis': s['analysis']})
        if not isinstance(answer, dict) or answer.get('decision') not in ('approve', 'reject', 'revise'):
            raise ValueError('An explicit approve, reject, or revise decision is required')
        if answer['decision'] == 'revise' and not str(answer.get('feedback', '')).strip():
            raise ValueError('Revision requires feedback')
        from datetime import datetime, timezone
        record = {'decision': answer['decision'], 'feedback': str(answer.get('feedback', '')),
                  'timestamp': datetime.now(timezone.utc).isoformat(), 'scope': 'planning only'}
        return {'decision': record['decision'], 'feedback': record['feedback'],
                'decisions': s.get('decisions', []) + [record], 'status': record['decision']}

    def planning(s):
        artifacts.plan(s, output)
        return {'status': 'planned_not_executed'}

    g = StateGraph(State)
    for name, node in [('discover', discover_node), ('reserve', reserve), ('analyze', do_analyze),
                       ('report', report), ('approval', approval), ('plan', planning)]:
        g.add_node(name, node)
    g.add_edge(START, 'discover')
    g.add_edge('discover', 'reserve')
    g.add_edge('reserve', 'analyze')
    g.add_edge('analyze', 'report')
    g.add_edge('report', 'approval')
    g.add_conditional_edges('approval', lambda s: s['decision'],
                            {'approve': 'plan', 'reject': END, 'revise': 'reserve'})
    g.add_edge('plan', END)
    return g.compile(checkpointer=SqliteSaver(connection))
