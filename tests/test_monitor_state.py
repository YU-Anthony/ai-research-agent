"""Exercise the actual Git persistence helper against a local bare remote."""
import json
import os
from pathlib import Path
import subprocess
import sys


def test_state_and_zotero_list_are_persisted_together(tmp_path):
    root = Path(__file__).resolve().parents[1]
    remote, checkout = tmp_path / 'remote.git', tmp_path / 'checkout'
    subprocess.run(['git', 'init', '--bare', str(remote)], check=True, capture_output=True)
    subprocess.run(['git', 'init', str(checkout)], check=True, capture_output=True)
    subprocess.run(['git', '-C', str(checkout), 'remote', 'add', 'origin', str(remote)], check=True)
    state = {'version': 1, 'seen': {}, 'requests': {}, 'papers': {'2601.12345': {'title': 'Example'}},
             'history': {}, 'zotero': {'https://api.zotero.org/users/123': {'synced': {
                 '2601.12345': {'status': 'existing', 'item_key': 'ITEMKEY1'}}}}}
    path = checkout / 'state.json'
    path.write_text(json.dumps(state))
    env = {**os.environ, 'PYTHONPATH': str(root / 'src')}
    def helper(mode):
        subprocess.run([sys.executable, str(root / 'examples/monitor_state.py'), mode, str(path)],
                       cwd=checkout, env=env, check=True, capture_output=True)
    helper('save')
    def show(name):
        return json.loads(subprocess.check_output(['git', '--git-dir', str(remote), 'show',
                                                  'literature-state:' + name]))
    assert show('state.json') == state
    entries = next(iter(show('zotero-sync-list.json')['libraries'].values()))
    assert entries[0]['arxiv_id'] == '2601.12345'
    assert entries[0]['zotero_item_key'] == 'ITEMKEY1'
    path.unlink()
    helper('restore')
    assert json.loads(path.read_text()) == state
