"""Approved CPU pilot. No network calls, GPU imports, or generated-code execution."""
from datetime import datetime, timezone
import json
from pathlib import Path
import resource
import time
import warnings

import numpy as np
import sklearn
from scipy.optimize import minimize_scalar
from scipy.special import expit, logit
from sklearn.linear_model import LogisticRegression
from sklearn.exceptions import ConvergenceWarning
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .data import load_windows, features, views, corrupt
from .metrics import classification, risk_curve, threshold, frozen_risk, cluster_interval


def temperature(p, y):
    logits = logit(np.clip(p, 1e-7, 1-1e-7))
    def loss(t):
        q = np.clip(expit(logits/t), 1e-7, 1-1e-7)
        return float(-(y*np.log(q) + (1-y)*np.log(1-q)).mean())
    result = minimize_scalar(loss, bounds=(.1, 10), method='bounded')
    if not result.success:
        raise ValueError('Temperature fitting failed')
    return float(result.x)


def predictions(model, t, rows, mode, weight):
    raw = model.predict_proba(np.array([features(r, mode) for r in rows]))[:, 1]
    p = expit(logit(np.clip(raw, 1e-7, 1-1e-7))/t)
    ps = [p]
    for index in (0, 1):
        q = model.predict_proba(np.array([features(views(r)[index], mode) for r in rows]))[:, 1]
        ps.append(expit(logit(np.clip(q, 1e-7, 1-1e-7))/t))
    probabilities = np.clip(np.array(ps), 1e-7, 1-1e-7)
    mean = probabilities.mean(axis=0)
    disagreement = (probabilities*np.log(probabilities/mean) +
                    (1-probabilities)*np.log((1-probabilities)/(1-mean))).mean(axis=0)/np.log(2)
    disagreement = np.clip(disagreement, 0, 1)
    confidence = np.maximum(p, 1-p)
    entropy = -(p*np.log(p) + (1-p)*np.log(1-p))
    return p, {'raw_confidence': np.maximum(raw, 1-raw), 'calibrated_confidence': confidence,
               'negative_entropy': -entropy, 'temporal_consistency': confidence-weight*disagreement,
               'repeat_view_control': confidence.copy()}


def run_experiment(data, config, output):
    started = time.monotonic()
    rows = load_windows(data, config['prediction_horizon_s'], config['max_samples'])
    if any(abs(r['timestamps_s'][0] + config['observation_window_s']) > 1e-6 for r in rows):
        raise ValueError('Observation duration differs from approved config')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    partitions = {name: [r for r in rows if r['split'] == name]
                  for name in ('train', 'calibration', 'validation', 'test')}
    conditions = [('clean', 0), ('random_drop', .25), ('random_drop', .5), ('burst_drop', .25), ('burst_drop', .5)]
    results = []
    prediction_path = output/'predictions.jsonl'
    with prediction_path.open('w') as predictions_file:
        for seed in config['seeds']:
            for mode in ('last', 'temporal'):
                if time.monotonic()-started > config['max_seconds']:
                    raise TimeoutError('Pilot deadline exceeded')
                train = partitions['train']
                model = make_pipeline(StandardScaler(), LogisticRegression(C=config['logistic_c'],
                    max_iter=config['max_iter'], random_state=seed, solver='lbfgs'))
                with warnings.catch_warnings():
                    warnings.simplefilter('error', ConvergenceWarning)
                    model.fit(np.array([features(r, mode) for r in train]), np.array([r['label'] for r in train]))
                cal = partitions['calibration']
                t = temperature(model.predict_proba(np.array([features(r, mode) for r in cal]))[:, 1],
                                np.array([r['label'] for r in cal]))
                # Frozen validation thresholds: only clean + the registered random-drop regime.
                val = partitions['validation']
                val_rng = np.random.default_rng(seed)
                val_observed = val + [corrupt(r, 'random_drop', .25, val_rng) for r in val]
                _, val_scores = predictions(model, t, val_observed, mode, config['consistency_weight'])
                cutoffs = {method: {str(c): threshold(score, c) for c in config['coverages']}
                           for method, score in val_scores.items()}
                for index, (kind, severity) in enumerate(conditions):
                    rng = np.random.default_rng(seed+1000*index)
                    test = [corrupt(r, kind, severity, rng) for r in partitions['test']]
                    y = np.array([r['label'] for r in test])
                    p, scores = predictions(model, t, test, mode, config['consistency_weight'])
                    record = {'seed': seed, 'representation': mode, 'condition': kind, 'severity': severity,
                              'temperature': t, 'classification': classification(y, p), 'methods': {}}
                    for method, score in scores.items():
                        record['methods'][method] = {**risk_curve(y, p, score, config['coverages']),
                            'validation_thresholds': cutoffs[method],
                            'frozen_threshold_results': {str(c): frozen_risk(y, p, score, cutoffs[method][str(c)])
                                                         for c in config['coverages']}}
                    record['paired_risk_difference_ci95_at_0.8'] = cluster_interval(y, p,
                        scores['temporal_consistency'], scores['calibrated_confidence'],
                        np.array([r['recording_id'] for r in test]), .8, config['bootstrap_repetitions'], seed)
                    results.append(record)
                    for row, label, probability, i in zip(test, y, p, range(len(test))):
                        predictions_file.write(json.dumps({'id': row['id'], 'recording_id': row['recording_id'],
                            'seed': seed, 'representation': mode, 'condition': kind, 'severity': severity,
                            'label': int(label), 'probability': float(probability),
                            'scores': {k: float(v[i]) for k,v in scores.items()}})+'\n')
    payload = {'status': 'completed', 'completed_at': datetime.now(timezone.utc).isoformat(),
               'data_kind': 'synthetic_test' if all(r['label_source']=='synthetic_test' for r in rows) else 'reviewed_input',
               'config': config, 'sample_counts': {k: len(v) for k,v in partitions.items()},
               'numpy_version': np.__version__, 'sklearn_version': sklearn.__version__,
               'elapsed_seconds': time.monotonic()-started,
               'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               'caveat': 'Matched-coverage curves are post-hoc evaluation, not deployment thresholds. '
                         'Bootstrap intervals condition on the fitted model; seeds are separate runs. '
                         'No causal, VLM, or clinical/emotion claims follow from this feature pilot.',
               'results': results}
    (output/'results.json').write_text(json.dumps(payload, indent=2))
    (output/'report.md').write_text('# Temporal-consistency CPU pilot\n\n'
        f"Data kind: {payload['data_kind']}. See results.json and per-sample predictions.jsonl.\n\n"
        'These are measured outputs for the supplied data only. Synthetic tests are not research findings.\n\n'
        'No automated novelty or statistical-significance claim is made. Compare temporal_consistency with '
        'calibrated_confidence at matched coverage and check frozen-threshold realized coverage.\n\n'+payload['caveat']+'\n')
    return payload
