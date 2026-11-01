"""Contract for independently prepared, reviewed real-data observation windows."""
import json
from pathlib import Path
import numpy as np

SPLITS = ('train', 'calibration', 'validation', 'test')


def load_windows(path, horizon, max_samples=10000):
    path = Path(path)
    if path.stat().st_size > 50_000_000:
        raise ValueError('Input exceeds the 50 MB pilot limit')
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not rows or len(rows) > max_samples:
        raise ValueError('Invalid sample count for CPU pilot')
    ids, groups = set(), {}
    for r in rows:
        required = ['id', 'recording_id', 'video_id', 'pedestrian_id', 'split', 'label_source']
        if any(not isinstance(r.get(k), str) or not r[k].strip() for k in required):
            raise ValueError('Missing sample identity, source, or split')
        if r['id'] in ids or r['split'] not in SPLITS:
            raise ValueError('Duplicate sample ID or unknown split')
        ids.add(r['id'])
        for kind in ('recording_id', 'video_id'):
            key = (kind, r[kind])
            if key in groups and groups[key] != r['split']:
                raise ValueError('Correlated recording/video crosses data splits')
            groups[key] = r['split']
        if type(r.get('label')) is not int or r['label'] not in (0, 1):
            raise ValueError('Binary crossing-action label required')
        if r.get('prediction_horizon_s') != horizon:
            raise ValueError('Prediction horizon differs from approved config')
        t, boxes, speed = [np.asarray(r.get(k), dtype=float) for k in ('timestamps_s', 'boxes', 'ego_speed_mps')]
        if t.ndim != 1 or len(t) < 8 or boxes.shape != (len(t), 4) or speed.shape != t.shape:
            raise ValueError('Expected at least eight aligned frames, boxes and speeds')
        if not all(np.isfinite(x).all() for x in (t, boxes, speed)):
            raise ValueError('Non-finite observations')
        if not np.all(np.diff(t) > 0) or t[-1] != 0 or t[0] >= 0:
            raise ValueError('Use increasing relative timestamps ending at observation time zero')
        if (boxes < 0).any() or (boxes > 1).any() or (boxes[:, 2:] <= 0).any():
            raise ValueError('Boxes must be normalized cx,cy,width,height')
        if (speed < 0).any():
            raise ValueError('Ego speed must be nonnegative metres per second')
    for split in SPLITS:
        subset = [r for r in rows if r['split'] == split]
        if {r['label'] for r in subset} != {0, 1}:
            raise ValueError('Each split must contain both classes')
        if len({r['recording_id'] for r in subset}) < 2:
            raise ValueError('Each split needs at least two independent recording groups')
    return sorted(rows, key=lambda r: r['id'])


def select_frames(row, indices):
    copy = dict(row)
    for key in ('timestamps_s', 'boxes', 'ego_speed_mps'):
        copy[key] = np.asarray(row[key])[indices].tolist()
    return copy


def corrupt(row, kind, severity, rng):
    """Drop interior observations only; preserve both endpoints, times and target."""
    n = len(row['timestamps_s'])
    if kind == 'clean':
        return row
    interior = np.arange(1, n - 1)
    count = min(len(interior), max(1, int(len(interior) * severity)))
    if kind == 'random_drop':
        removed = rng.choice(interior, count, replace=False)
    elif kind == 'burst_drop':
        start = int(rng.integers(1, n - count))
        removed = np.arange(start, start + count)
    else:
        raise ValueError('Unknown temporal corruption')
    return select_frames(row, np.array([i for i in range(n) if i not in set(removed)]))


def features(row, mode='temporal'):
    t = np.asarray(row['timestamps_s'], dtype=float)
    x = np.column_stack([np.asarray(row['boxes']), np.asarray(row['ego_speed_mps'])])
    if mode == 'last':
        return x[-1]
    if mode != 'temporal':
        raise ValueError('Unknown representation')
    centered = t - t.mean()
    slope = (centered[:, None] * x).sum(axis=0) / (centered @ centered)
    # Equal feature dimensionality for all sampling views; actual time gaps are retained.
    return np.concatenate([x[-1], x.mean(axis=0), x.std(axis=0), slope])


def views(row):
    n = len(row['timestamps_s'])
    # Same physical time interval and last frame; never reverse or fabricate frames.
    return [select_frames(row, np.unique(np.r_[0, np.arange(offset, n, 2), n-1]).astype(int))
            for offset in (0, 1)]
