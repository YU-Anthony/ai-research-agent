"""Selective risk with frozen thresholds and explicitly post-hoc matched coverage."""
import numpy as np
from sklearn.metrics import f1_score, balanced_accuracy_score, roc_auc_score, brier_score_loss


def classification(y, p):
    pred = p >= .5
    ece = 0.0
    confidence = np.maximum(p, 1-p)
    for i in range(10):
        mask = (confidence >= i/10) & ((confidence < (i+1)/10) if i < 9 else (confidence <= 1))
        if mask.any():
            ece += mask.mean() * abs((pred[mask] == y[mask]).mean() - confidence[mask].mean())
    return {'macro_f1': float(f1_score(y, pred, average='macro', zero_division=0)),
            'balanced_accuracy': float(balanced_accuracy_score(y, pred)),
            'auroc': float(roc_auc_score(y, p)), 'brier': float(brier_score_loss(y, p)), 'ece': float(ece)}


def risk_curve(y, p, score, coverages):
    errors = ((p >= .5) != y).astype(float)
    order = np.argsort(-score, kind='stable')
    risks = np.cumsum(errors[order]) / np.arange(1, len(y)+1)
    return {'aurc': float(risks.mean()),
            'matched_coverage_risk': {str(c): float(risks[max(1, int(np.ceil(c*len(y))))-1]) for c in coverages}}


def threshold(score, coverage):
    k = max(1, int(np.ceil(len(score)*coverage)))
    return float(np.sort(score)[-k])


def frozen_risk(y, p, score, cutoff):
    keep = score >= cutoff
    return {'coverage': float(keep.mean()), 'risk': float(((p[keep] >= .5) != y[keep]).mean()) if keep.any() else None}


def cluster_interval(y, p, scores_a, scores_b, groups, coverage, repetitions, seed):
    """Paired bootstrap of recording groups; negative difference favours method A."""
    rng = np.random.default_rng(seed)
    unique = np.unique(groups)
    differences = []
    for _ in range(repetitions):
        selected = rng.choice(unique, len(unique), replace=True)
        indices = np.concatenate([np.flatnonzero(groups == group) for group in selected])
        def risk(score):
            return risk_curve(y[indices], p[indices], score[indices], [coverage])['matched_coverage_risk'][str(coverage)]
        differences.append(risk(scores_a) - risk(scores_b))
    return [float(x) for x in np.quantile(differences, [.025, .975])]
