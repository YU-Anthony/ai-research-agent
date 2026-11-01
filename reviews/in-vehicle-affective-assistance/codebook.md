# Pilot extraction codebook

All rows are provisional single-agent, targeted-full-text extractions. "No" means the coded evaluation did not establish that endpoint in the inspected sections, not proof that the paper never mentions it. A human should confirm each row before publication. Fields are separate dimensions, not an ordinal quality score.

- `id`, `url`: exact retrieved arXiv version and verified record link. PDF retrieval requests were versionless; hashes in fulltext-fingerprints.json preserve retrieved content. Confirm version correspondence before finalizing citations.
- `scope_role`: generative_core or non_generative_comparator. Do not pool the two as one technology category.
- `design`, `setting`: identify concept/preference work, offline metric/generation evaluation, controlled human study, or interaction-load assessment, and simulator/closed-track/on-road/synthetic-pair conditions.
- `sample_note`: distinguish recruitment, analysis, interview and evaluation-sample units. A sample of generated messages is not a sample of drivers. Unknown or internally inconsistent Ns remain explicit.
- `intervention_or_comparator`: system behavior and actual comparison, if any. Do not infer random allocation or blinding.
- `measured_endpoints`: observed outputs/measurements, not just metrics claimed in a title.
- `human_experience_measured`: subjective experience/workload/acceptability/trust was assessed. These constructs are not interchangeable.
- `human_preference_measured`: explicit preference, adoption orientation or an expressed interaction preference is identified in the pilot extraction. `not_established_in_pilot` is used where inspected measurements show workload or subjective efficacy but do not establish a preference measure. Neither field establishes consent to intervention, emotion improvement or population-wide preference.
- `human_state_measured`: human emotion/stress/sleepiness state was assessed as an outcome. Physiology is not automatically a direct readout of mental state; fatigue and emotion remain distinct constructs.
- `driving_performance_measured`: vehicle-control/task measures were assessed as outcomes. DRT, gaze or subjective safety alone are not crash outcomes and are not coded as direct driving-performance evidence here.
- `real_vehicle_interaction`: assistant/intervention interaction in a real vehicle, including a closed track. This does not establish unrestricted on-road effectiveness, long-term adoption or production-level autonomy.
- `source_locator`: paper section or named result where extraction can be checked. Original PDF line numbers are not universal and are not used as publication locators.
- `limitations`: interpretation boundaries, disclosed interests, sample inconsistencies or unextracted fields.
- `verification_status`: human verification remains pending; no inter-rater agreement was measured.

Future extraction should add modality synchronization, supervision provenance, state/need/preference distinctions, intervention timing/opt-out, sample-family overlap, deployment latency, missingness, release/license/access status and funding. The current CSV does not claim all these fields are fully coded.
