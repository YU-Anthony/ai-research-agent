# Minimal experiment protocol: temporal-evidence consistency

Status: framework and synthetic software tests only. No real dataset is prepared, no empirical advantage is established, and no real experiment is approved. Driver behavior/intention prediction is a separate long-term research direction and is outside this pilot. The current target is **pedestrian future crossing action**, not the driver's maneuver, human mental intent, VLM reasoning or emotion.

## One research question

At fixed prediction time and answer coverage, does consistency across valid temporal subsamples identify errors under frame loss better than the same predictor's confidence alone?

Falsifiable hypothesis: the consistency score lowers selective prediction risk relative to calibrated confidence at 80% coverage under an unseen burst-drop condition. Failure to obtain a stable improvement is a valid negative result. This is a candidate contribution requiring further novelty review; temporal modeling, uncertainty and abstention themselves are established.

## Fixed pilot scope

- A licensed PIE real-data subset, past observation window 0.5 s and future-action target at +1.0 s. Confirm these label definitions and class support before fixing the dataset manifest. "Currently crossing", "crossing by a horizon", "crossing at a horizon" and mental intention are different targets; this protocol uses **crossing action at the registered horizon**.
- No raw video classifier or VLM training. Inputs are observed pedestrian bounding-box tracks and synchronized ego-vehicle speed. First assess the protocol using these inexpensive structured features. RGB/foundation-model extensions require a later proposal.
- One transparent model family: standardized Logistic Regression, C=1. Two representations: last observed box/speed (5 features) and past-window last/mean/std/time-based slope (20 features). Different feature counts mean this representation comparison is descriptive, not evidence isolating capacity or temporal understanding.
- Three seeds (11,29,47). Logistic Regression is largely deterministic; seeds vary corruption/bootstrap draws and do not represent substantial independent training randomness.
- CPU only, BLAS threads capped at one, default hard subprocess timeout 600 s, at most 10,000 windows. RAM is measured, not hard limited. Initial engineering target is a much smaller subset; no runtime estimate has been measured on real PIE.

## Data contract and leakage controls

Prepare JSONL independently; do not fabricate labels. Each row needs:

```json
{
  "id": "unique-window-id",
  "recording_id": "original-continuous-recording-id",
  "video_id": "video-id",
  "pedestrian_id": "track-id",
  "split": "train",
  "label_source": "reviewed-PIE-crossing-action-annotation",
  "label": 0,
  "prediction_horizon_s": 1.0,
  "timestamps_s": [-0.5, -0.43, -0.36, -0.29, -0.22, -0.15, -0.08, 0.0],
  "boxes": [[0.5,0.5,0.1,0.2],[0.5,0.5,0.1,0.2],[0.5,0.5,0.1,0.2],[0.5,0.5,0.1,0.2],[0.5,0.5,0.1,0.2],[0.5,0.5,0.1,0.2],[0.5,0.5,0.1,0.2],[0.5,0.5,0.1,0.2]],
  "ego_speed_mps": [5,5,5,5,5,5,5,5]
}
```

This row is a schema illustration, **not real PIE data**. Boxes use normalized center-x, center-y, width, height; speed is metres/second. At least eight aligned observations are required. Relative timestamps must strictly increase, end at zero, and cover the registered past window. Samples and splits have unique identities. The same original recording or video may not cross splits; each split needs both classes and at least two recording groups. Adjacent clips from one continuous recording must share recording_id.

Four roles: training fits the scaler/classifier; calibration fits temperature; validation fixes score thresholds; test evaluates exactly once after choices are frozen. Use the official test partition as held-out test; derive the other disjoint partitions only from eligible training/validation material, respecting recording groups. Inspect the actual official split before claiming compatibility. Overlapping windows within a split are correlated and must remain grouped for uncertainty estimates.

The loader verifies structural constraints, not the truth of annotations or licenses. A reviewed PIE-to-JSONL adapter, video download, source-file checksums, split manifest, label-alignment audit and class-balance report remain required. The converter is deliberately not implemented until real annotation files and the exact target definition have been checked.

## Method and controls

The same fitted classifier predicts from a complete observed window and two deterministic lower-rate views. Both views keep the first/last observations and actual timestamps. Jensen-Shannon disagreement among the three binary probability distributions measures sampling sensitivity. Score = calibrated max probability minus 0.5 times normalized disagreement. Weight is fixed, not tuned on test data. This does not establish causal reasoning or explanation faithfulness; benign subsampling can change feature averages and cause distribution shift.

Compare no-abstention (100% coverage), raw confidence, calibrated confidence, negative entropy, temporal consistency, and a repeat-identical-view negative control. A temperature-scaled binary predictor preserves label and confidence ordering; confidence/entropy controls are not independent novel methods and their matched-coverage risk rankings may coincide. The repeat-view control must reproduce calibrated confidence exactly. The last-frame representation should be insensitive to interior frame loss, providing another diagnostic.

## Conditions and evaluation

Train/calibrate on clean observations. Thresholds use validation clean plus registered random interior dropout of 25%. Test clean, random dropout at 25%/50%, and burst dropout at 25%/50%. Burst loss is unseen during threshold selection. Preserve endpoints, physical time interval, observation cutoff and target label. These are artificial stress tests, not measurements of real camera failure. They assess interior evidence loss, not delayed/missing final frames.

Report Macro-F1, balanced accuracy, AUROC, Brier score and 10-bin ECE; mean risk across all ranked prefixes (AURC); risk at 50%,80%,90%,100% matched coverage; frozen validation thresholds and actual test coverage/risk. Matched-coverage test rankings are post-hoc evaluation, **not deployable threshold selection**. Deterministic score ties follow stable sample-ID ordering and must be noted for small subsets.

Primary comparison: temporal consistency minus calibrated-confidence error risk at 80% coverage under 50% burst drop. Secondary conditions are exploratory. Paired bootstrap original recording groups (200 default replicates) for each fitted seed; these intervals condition on the fitted model and do not include dataset-collection or training uncertainty. Report per-seed differences and actual retained counts, not only favorable aggregates. Tiny datasets/few groups cannot support strong significance claims. No subgroup/adaptive-window/model-search additions in this first pilot.

## Approval and execution

The research agent and scheduled literature workflow never call the experiment runner. The existing `research-agent decide approve` authorizes planning only and does not authorize this separate run. Review the exact data license, dataset/split/label manifest, source code and configuration, then explicitly authorize one local CPU invocation:

```bash
python -m pip install -e '.[dev,experiments]'
python -m pytest -q
# Only after human review and approval; this command has NOT been run on real data:
python -m research_agent.experiment \
  --data /path/to/reviewed-windows.jsonl \
  --config configs/experiments/temporal-consistency.json \
  --output runs/temporal-pilot-001 \
  --approve-cpu-run
```

No approval flag means no input execution/output creation. Output paths must be new. Approval records bind data/config/source SHA-256 hashes and configuration. The launcher isolates a local worker, removes conventional API-key/token environment variables, limits BLAS threads and kills the worker at timeout. No network/GPU/cloud provisioner, generated-code execution or publication exists. There is no process sandbox or strict memory cap; review the imported code and use an appropriate low-privilege environment. NumPy/scikit-learn are optional dependencies, separate from literature monitoring.

Outputs: approval.json, status.json, measured results.json, predictions.jsonl, and a deliberately non-interpretive report.md. Results include configuration, package versions, runtime and peak RSS on Linux. Synthetic software-test outputs are explicitly labeled and must never be used as scientific findings. Real model serialization/reload, plots, a PIE converter and cross-dataset experiments are outside this minimal framework. Framework tests with synthetic fixtures are code validation, not authorized real research experiments.
