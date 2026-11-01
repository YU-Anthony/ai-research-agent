"""Restore/persist monitor state on a dedicated Git branch, without touching the index."""
import argparse
from pathlib import Path
import subprocess

BRANCH = 'refs/heads/literature-state'
REF = 'refs/remotes/origin/literature-state'


def git(*args, data=None):
    return subprocess.check_output(['git', *args], input=data).decode().strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['restore', 'save'])
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    remote = subprocess.run(['git', 'ls-remote', '--exit-code', '--heads', 'origin', BRANCH],
                            capture_output=True, text=True)
    if remote.returncode not in (0, 2):
        raise SystemExit('Cannot inspect remote state branch; refusing to reset deduplication state')
    parent = None
    if remote.returncode == 0:
        subprocess.run(['git', 'fetch', '--no-tags', 'origin', f'{BRANCH}:{REF}'], check=True)
        parent = git('rev-parse', REF)
    if args.mode == 'restore':
        if parent:
            content = subprocess.check_output(['git', 'show', f'{parent}:state.json'])
            args.path.parent.mkdir(parents=True, exist_ok=True)
            args.path.write_bytes(content)
        else:
            print('No state branch: first run')
        return
    if not args.path.exists():
        print('No state file to persist')
        return
    from research_agent.monitor import read_state
    read_state(args.path)  # fail closed on malformed state
    blob = git('hash-object', '-w', '--stdin', data=args.path.read_bytes())
    tree = git('mktree', data=f'100644 blob {blob}\tstate.json\n'.encode())
    if parent and git('rev-parse', f'{parent}^{{tree}}') == tree:
        print('State unchanged')
        return
    command = ['-c', 'user.name=github-actions[bot]', '-c',
               'user.email=41898282+github-actions[bot]@users.noreply.github.com',
               'commit-tree', tree, '-m', 'Persist literature monitoring state']
    if parent:
        command += ['-p', parent]
    commit = git(*command)
    subprocess.run(['git', 'push', 'origin', f'{commit}:{BRANCH}'], check=True)


if __name__ == '__main__':
    main()
