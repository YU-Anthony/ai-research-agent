"""Deterministic reports and unexecuted experiment scaffold."""
import json
from pathlib import Path

STARTER = '''"""Unexecuted scaffold. Supply real licensed data and a reviewed training loop."""
import torch
from torch import nn

class FusionBaseline(nn.Module):
    def __init__(self, camera_dim: int, lidar_dim: int, outputs: int):
        super().__init__()
        self.head = nn.Linear(camera_dim + lidar_dim, outputs)

    def forward(self, camera_features, lidar_features):
        return self.head(torch.cat([camera_features, lidar_features], dim=-1))

if __name__ == "__main__":
    raise SystemExit("Training is not implemented. Review data, budget, and execution approval first.")
'''


def write_report(state, root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    lines = ['# Research gap report', state['topic'],
             'Evidence: retrieved arXiv metadata and abstracts. All gap/novelty claims are tentative.',
             'No experiments have been run. Dataset and resource recommendations are unverified.']
    lines += ['## Workflow status', 'Paused for explicit human approval before experiment planning. '
              'No experiment execution is implemented. State and decisions persist in state.sqlite.']
    usage = state['analysis'].get('model_usage')
    if usage:
        lines += ['## Model usage and estimated cost',
                  f"Model: {usage['model']}; input tokens: {usage['prompt_tokens']}; output tokens: {usage['completion_tokens']}; "
                  f"estimated cost: ${usage['estimated_cost_usd']:.6f}; request budget: ${usage['budget_usd']:.2f}.",
                  usage['pricing_note']]
    for gap in state['analysis']['gaps']:
        lines += [f"## Potential gap: {gap['question']}", f"Evidence IDs: {', '.join(gap['evidence_ids'])}", gap['limitation']]
    for i, h in enumerate(state['analysis']['hypotheses'], 1):
        lines += [f"## Hypothesis {i}: {h['statement']}", f"Evidence IDs: {', '.join(h['evidence_ids'])}",
                  f"Speculation: {h['speculation']}", f"Dataset: {h['dataset']}; baseline: {h['baseline']}; metric: {h['metric']}",
                  f"Falsifiable test: {h['test']}", f"Provisional compute estimate: {h['compute']}"]
    lines += ['## Retrieved references']
    for p in state['papers']:
        lines += [f"- [{p['id']}] {p['title']} — {', '.join(p['authors'])} ({p['published']}). {p['url']}", p['abstract']]
    (root / 'research-gap.md').write_text('\n\n'.join(lines))
    (root / 'papers.json').write_text(json.dumps(state['papers'], indent=2))
    (root / 'analysis.json').write_text(json.dumps(state['analysis'], indent=2))


def plan(state, root):
    root = Path(root)
    text = ['# Experiment plan — human review required',
            'Status: approved for planning only. No execution is implemented.',
            'Provisional estimate: feature-level pilot, CPU smoke test; full training may require 1 GPU, '
            '16–24 GB VRAM and 2–24 GPU-hours per seed. These are planning assumptions, not measured costs. '
            'Benchmark a small sample and approve a concrete monetary/GPU budget separately.',
            'Use fixed train/validation/test splits, prevent scene leakage, run at least three seeds, '
            'report confidence intervals, and compare against the same backbone without the proposed intervention.']
    for h in state['analysis']['hypotheses']:
        text += [h['statement'], f"Data: {h['dataset']}; baseline: {h['baseline']}; metric: {h['metric']}", h['test']]
    (root / 'experiment-plan.md').write_text('\n\n'.join(text))
    (root / 'starter.py').write_text(STARTER)


def draft(root):
    """Draft from persisted verified literature; deliberately leaves results empty."""
    root = Path(root)
    papers = json.loads((root / 'papers.json').read_text())
    report = (root / 'research-gap.md').read_text()
    (root / 'paper.md').write_text('# Research proposal draft\n\n' + report +
        '\n\n## Methods\nSee experiment-plan.md (if approved).\n\n## Results\nNo verified experiment results supplied.\n')
    def esc(s):
        table = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
                 '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
        return ''.join(table.get(c, c) for c in s)
    refs = '\n'.join(r'\item ' + esc(p['title'] + ' — ' + ', '.join(p['authors']) + ' ' + p['published'] + ' ' + p['url']) for p in papers)
    (root / 'paper.tex').write_text(r'\documentclass{article}\begin{document}\section{Research proposal}' +
        esc(report.split('## Retrieved references')[0]) + r'\section{Results}No verified experiment results supplied.' +
        r'\section{References}\begin{enumerate}' + refs + r'\end{enumerate}\end{document}')
