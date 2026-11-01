import argparse
import json
import re
import sqlite3
from pathlib import Path
from langgraph.types import Command
from .workflow import build_graph
from .artifacts import draft


def main(argv=None):
    p = argparse.ArgumentParser(description='Human-reviewed research agent; experiments are never executed')
    p.add_argument('--runs', type=Path, default=Path('runs'))
    sub = p.add_subparsers(dest='command', required=True)
    start = sub.add_parser('start')
    start.add_argument('run_id')
    start.add_argument('--topic', required=True, help='arXiv search expression')
    start.add_argument('--allow-paid-reasoning', action='store_true')
    start.add_argument('--max-calls', type=int, default=1)
    resume = sub.add_parser('decide')
    resume.add_argument('run_id')
    resume.add_argument('decision', choices=['approve', 'reject', 'revise'])
    resume.add_argument('--feedback', default='')
    resume.add_argument('--allow-paid-reasoning', action='store_true')
    for cmd in ('status', 'draft'):
        sub.add_parser(cmd).add_argument('run_id')
    args = p.parse_args(argv)
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', args.run_id):
        p.error('run_id must contain only letters, digits, underscore or hyphen')
    root = args.runs / args.run_id
    if args.command == 'start':
        if not args.allow_paid_reasoning:
            p.error('Live reasoning requires --allow-paid-reasoning (one bounded paid call by default)')
        if not 1 <= args.max_calls <= 5:
            p.error('--max-calls must be between 1 and 5')
        if root.exists():
            p.error('Run already exists; inspect status or use decide')
        root.mkdir(parents=True)
    elif not (root / 'state.sqlite').exists():
        p.error('Unknown run')
    if args.command == 'draft':
        draft(root)
        print('Proposal drafts written. Results remain explicitly empty.')
        return
    with sqlite3.connect(root / 'state.sqlite', check_same_thread=False) as connection:
        graph = build_graph(connection, root)
        config = {'configurable': {'thread_id': args.run_id}}
        if args.command == 'start':
            graph.invoke({'topic': args.topic, 'max_calls': args.max_calls, 'calls_used': 0, 'decisions': []}, config)
        elif args.command == 'decide':
            current = graph.get_state(config)
            if current.next != ('approval',):
                p.error('Run is not awaiting approval')
            if args.decision == 'revise':
                if not args.allow_paid_reasoning or not args.feedback.strip():
                    p.error('Revision requires feedback and --allow-paid-reasoning')
                if current.values.get('calls_used', 0) >= current.values.get('max_calls', 1):
                    p.error('Revision budget exhausted; reserve multiple calls when starting a run')
            graph.invoke(Command(resume={'decision': args.decision, 'feedback': args.feedback}), config)
        state = graph.get_state(config)
        print(json.dumps({'status': state.values.get('status'), 'pending': state.next,
                          'calls_reserved': state.values.get('calls_used', 0),
                          'decisions': state.values.get('decisions', []), 'output': str(root)}, indent=2))


if __name__ == '__main__':
    main()
