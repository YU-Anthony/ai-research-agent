"""Explicitly approved, isolated CPU experiment entry point. Never invoked by the agent."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys


def read_config(path):
    c = json.loads(Path(path).read_text())
    expected = {'name', 'prediction_horizon_s', 'observation_window_s', 'seeds', 'coverages',
                'consistency_weight', 'logistic_c', 'max_iter', 'bootstrap_repetitions', 'max_samples', 'max_seconds'}
    if set(c) != expected:
        raise ValueError('Unexpected or missing config fields')
    if not isinstance(c['seeds'], list) or not 1 <= len(c['seeds']) <= 5 or any(type(x) is not int or x < 0 for x in c['seeds']):
        raise ValueError('Invalid seeds')
    if len(set(c['seeds'])) != len(c['seeds']):
        raise ValueError('Duplicate seeds')
    for k, maximum in [('max_iter', 1000), ('bootstrap_repetitions', 1000), ('max_samples', 10000), ('max_seconds', 1800)]:
        if type(c[k]) is not int or not 1 <= c[k] <= maximum:
            raise ValueError('CPU pilot resource bound invalid')
    for k in ('prediction_horizon_s', 'observation_window_s', 'logistic_c', 'consistency_weight'):
        if type(c[k]) not in (int, float) or not math.isfinite(c[k]) or c[k] <= 0:
            raise ValueError('Config values must be positive finite numbers')
    if not isinstance(c['coverages'], list) or not c['coverages'] or any(
            type(v) not in (int,float) or not math.isfinite(v) or not 0 < v <= 1 for v in c['coverages']):
        raise ValueError('Invalid coverage grid')
    return c


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', type=Path, required=True)
    p.add_argument('--config', type=Path, default=Path('configs/experiments/temporal-consistency.json'))
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--approve-cpu-run', action='store_true', help='Explicit approval of this input, code and resource-limited local CPU run')
    p.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = p.parse_args(argv)
    if not args.approve_cpu_run:
        p.error('Review data license, labels, split protocol, code and config, then explicitly approve with --approve-cpu-run')
    config = read_config(args.config)
    if args.worker:
        from .experiments.runner import run_experiment
        run_experiment(args.data, config, args.output)
        return
    # Never overwrite a previous result or approval record.
    args.output.mkdir(parents=True, exist_ok=False)
    source = Path(__file__).parent
    manifest = {'approved_at': datetime.now(timezone.utc).isoformat(), 'scope': 'local CPU pilot only; no network/GPU/publication',
                'data_sha256': sha(args.data), 'config_sha256': sha(args.config), 'config': config,
                'source_sha256': {str(f.relative_to(source)): sha(f) for f in [source/'experiment.py', *sorted((source/'experiments').glob('*.py'))]}}
    (args.output/'approval.json').write_text(json.dumps(manifest, indent=2))
    environment = dict(os.environ)
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        environment[name] = '1'
    # Child receives no API credentials; this experiment needs only reviewed local data.
    for name in list(environment):
        if name.endswith(('_API_KEY', '_TOKEN')):
            environment.pop(name)
    command = [sys.executable, '-m', 'research_agent.experiment', '--worker', '--approve-cpu-run',
               '--data', str(args.data.resolve()), '--config', str(args.config.resolve()), '--output', str(args.output.resolve())]
    try:
        result = subprocess.run(command, env=environment, timeout=config['max_seconds'], capture_output=True)
        status = {'status': 'completed' if result.returncode == 0 else 'failed', 'exit_code': result.returncode}
    except subprocess.TimeoutExpired:
        status = {'status': 'timeout', 'max_seconds': config['max_seconds']}
    # Do not echo arbitrary data or exception text. Results/approval remain available for inspection.
    (args.output/'status.json').write_text(json.dumps(status, indent=2))
    print(json.dumps(status))
    if status['status'] != 'completed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
