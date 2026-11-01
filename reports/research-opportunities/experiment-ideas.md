# Experiment opportunities aligned with the research profile

These are proposed experiments, not demonstrated results or claims of novelty. The four prior-work records in verified-papers.json were retrieved from arXiv. Dataset repositories were read directly; video downloads and licenses have not been fully validated. No experiment has been executed.

## 1. Temporal evidence, rather than frame count, for trustworthy behavior prediction

**Question:** Does chronological motion information improve crossing-action prediction, or do gains mostly come from repeated appearance/context?

**Hypothesis:** Correctly ordered past frames improve Macro-F1 and calibration over the same last-frame baseline; reversing/shuffling the history weakens that benefit, especially before movement onset.

**Data:** PIE subset with pedestrian tracks, per-frame crossing labels and official splits. Labels for crossing action must not be presented as mental intention. Use an explicitly defined future crossing horizon; features end at observation time. Verify enough positives/negatives exist before fixing the task.

**Baselines:** Same linear classifier or small MLP over last-frame features; mean-pooled features (order invariant); ordered concatenated/difference features. Repeat-last-frame, shuffled/reversed history, matched observation time and dimensionality/parameter controls isolate temporal information.

**Metrics:** Macro-F1, balanced accuracy, AUROC where both classes exist, Brier score/ECE, CPU time and peak memory. Report confidence intervals grouped by video/subject and three seeds. Use official splits, excluding correlated footage across splits; never split neighboring frames randomly.

**CPU pilot:** Small real video subset, cached HOG/image statistics and optional track geometry, a few thousand windows. A 4-8 CPU-core / 8-16 GB RAM machine is a planning assumption; timing is unmeasured. Frozen neural features are an optional later extension, not a requirement. No new paper-level multimodal/VLM claim follows from a HOG-only pilot.

**Research value/risk:** A plain single-frame versus multi-frame comparison is established. A controlled temporal-order/uncertainty/error-stratification protocol is a more specific opportunity, but still requires prior-work checking. Walking/standing recognition is a simpler fallback if future-crossing labels are too sparse.

**Data evidence:** https://github.com/aras62/PIE and its annotations/README.md (video total approximately 74 GB; use a subset and on-demand decoding, not full frame extraction).

## 2. WOMD-Reasoning: intervention-based tests of explanation faithfulness

**Question:** Do explanations track the actual traffic-interaction facts used by a behavior predictor, or merely sound plausible?

**Hypothesis:** A structured evidence-constrained explanation layer reduces unsupported claims and reacts more consistently to changes in relevant interaction features than unconstrained explanation generation, without collapsing explanation coverage.

**Data:** A licensed, accessible WOMD scenario subset. Motion histories and map geometry can supply structured interactions. WOMD's motion benchmark is not itself a ready-made camera/text explanation dataset. Ground-truth motives such as "the driver wanted to yield" cannot be inferred as fact from tracks alone.

**Baselines:** A transparent feature-based behavior model with deterministic textual templates; an unconstrained text explanation baseline only if cached outputs exist or API spending is separately approved. Independent reviewers evaluate a small annotation set rather than using template labels as proof of template superiority.

**Interventions:** Mask a relevant versus irrelevant neighbor; perturb separation or velocity; change lane topology only if physically valid. Separate model-input interventions from causal claims about human motives. Define expected relation changes in advance.

**Metrics:** Unsupported-fact rate, intervention sensitivity/specificity, prediction-explanation consistency, explanation coverage, and human adjudication on a small held-out set. Compare to a trivial abstention baseline; a model saying nothing must not win solely on low error.

**CPU pilot:** Parse a small preprocessed motion subset, derive distances/relative velocity/TTC only when assumptions apply, and evaluate a linear/tree model plus templates. 4-8 cores / 8-16 GB RAM is an unmeasured planning assumption. Full WOMD ingestion and training may be much heavier.

**Research value/risk:** Better aligned with explainable driving and WOMD-Reasoning, but more setup and annotation work. Novelty would need a defined intervention protocol and checks against existing grounded driving QA/explanation benchmarks.

**Verified prior work:** WOMD https://arxiv.org/abs/2104.10133v1 ; DriveLM https://arxiv.org/abs/2312.14150v3 ; BDD-X https://arxiv.org/abs/1807.11546v1 .

## 3. Calibrated abstention under missing or conflicting modalities

**Question:** Can a small system know when visual and vehicle-state evidence is insufficient or contradictory?

**Hypothesis:** Held-out calibrated confidence with a modality-consistency check lowers error at matched coverage under sensor corruption more than an uncalibrated fusion model or confidence-only abstention.

**Data:** PIE image/track features plus synchronized ego-vehicle speed, or another real public paired-modality dataset after access checks. Test modality ablation, corrupted images, delayed state streams and cross-record mismatches. Mark artificial corruptions as stress tests, not real measured sensor failures.

**Baselines:** Visual-only and state-only classifiers; simple fusion; temperature/Platt calibration; confidence-only and consistency-aware abstention. Fit calibration only on validation data. Match retained coverage to prevent a reject-everything policy from appearing better.

**Metrics:** Risk-coverage curves, AURC, Brier score, calibration error, subgroup failure rates and task performance. Include unseen corruption types and video-disjoint splits.

**CPU pilot:** Cached visual/trajectory features plus logistic regression or a small MLP. No large foundation model training is required. Extending findings to VLMs requires a subsequent real VLM experiment.

**Research value/risk:** Bridges multimodal fusion, trustworthy AI and human-centered assistance. Calibration/abstention are established; the contribution must be more specific than applying standard calibration to an existing dataset.

## 4. Broad multimodal transfer: grounding versus confident hallucination

**Question:** Does evidence-aware abstention remain useful when a model moves from generic visual QA to driving scenes?

**Hypothesis:** An evidence verifier calibrated in-domain reduces unsupported driving-object claims at matched answer coverage more than transferring the same threshold from generic imagery.

**Data:** POPE-style object-presence evaluation plus a licensed driving-image subset with independently verified object labels. Reuse model outputs only if they are actually available and licensed; cached predictions are not assumed to exist.

**Baselines/metrics:** Fixed pretrained VLM, confidence-only rejection and object-evidence-aware rejection; hallucination precision/recall, risk-coverage, task accuracy, verifier cost. Ground-truth annotations and verifier outputs must be evaluated independently.

**Feasibility:** CPU-friendly if valid cached predictions/features exist; fresh VLM inference may be expensive on CPU, so this is a second-stage project rather than the first experiment.

**Verified prior work:** POPE https://arxiv.org/abs/2305.10355v3 ; DriveLM https://arxiv.org/abs/2312.14150v3 . POPE establishes prior work on object hallucination, not proof of a novel driving-transfer problem.

## Recommended order and approval boundary

Start with 1 for a reproducible CPU baseline. Choose 2 as a higher-value research direction after data and annotation feasibility are verified; 3 is a resource-conscious extension. Keep 4 as a bridge to broader foundation-model research. Driver-emotion inference is not prioritized for the first pilot because suitable supervision, subject-disjoint evaluation and consent/license conditions need more preparation.

Before any run: approve the task/label definition, exact data subset and license, code version, seeds, metrics, resource/time budget and output destination. No experiment execution, driver-assistance deployment, paid model evaluation, aiXiv posting or submission is authorized by this idea document.
