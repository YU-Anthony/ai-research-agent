"""Searchable SQLite projection of portable research history; never calls a model."""
import argparse
import json
from pathlib import Path
import sqlite3


def sync(state, database):
    database = Path(database)
    database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS papers (id TEXT PRIMARY KEY, title TEXT, abstract TEXT, metadata TEXT)')
        conn.execute('CREATE TABLE IF NOT EXISTS research_runs (id TEXT PRIMARY KEY, record TEXT)')
        for key, paper in state.get('papers', {}).items():
            conn.execute('INSERT OR REPLACE INTO papers VALUES (?, ?, ?, ?)',
                         (key, paper['title'], paper['abstract'], json.dumps(paper)))
        for key, record in state.get('history', {}).items():
            conn.execute('INSERT OR REPLACE INTO research_runs VALUES (?, ?)', (key, json.dumps(record)))


def search(database, query, limit=20):
    if not 1 <= limit <= 100:
        raise ValueError('Limit must be between 1 and 100')
    # Bound parameters and escaped wildcards make this a literal substring search.
    pattern = '%' + query.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_') + '%'
    with sqlite3.connect(database) as conn:
        rows = conn.execute("SELECT metadata FROM papers WHERE title LIKE ? ESCAPE '\\' OR abstract LIKE ? ESCAPE '\\' ORDER BY id DESC LIMIT ?",
                            (pattern, pattern, limit)).fetchall()
    return [json.loads(row[0]) for row in rows]


def main():
    from .monitor import read_state
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query')
    parser.add_argument('--state', type=Path, default=Path('monitor-state/state.json'))
    parser.add_argument('--database', type=Path, default=Path('monitor-state/library.sqlite'))
    args = parser.parse_args()
    if not args.state.is_file():
        parser.error('Research state does not exist; restore or run monitoring first')
    sync(read_state(args.state), args.database)
    for paper in search(args.database, args.query):
        print(json.dumps({'id': paper['id'], 'title': paper['title'], 'url': paper['url']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
