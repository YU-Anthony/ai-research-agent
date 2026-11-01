# What Counts as Evidence? Evaluating Generative In-Vehicle Assistants for Driver Support

**Working manuscript skeleton and pilot synthesis — not submission-ready.**

## Provisional abstract

Generative in-vehicle assistants are increasingly proposed to support drivers through conversation, risk-sensitive advice and affect-aware interaction. Their evaluations span recognition accuracy, automated message scores, subjective experience, driver-state measures and driving-related outcomes. We propose a scoping review that maps these distinct forms of evidence and examines how they support claims about usefulness, emotional support and driving safety. An exploratory arXiv pilot retrieved 60 records across three relevance-capped queries (57 unique arXiv identifiers). Four review seeds yielded a combined ledger of 60 unique records. Eight original studies were purposefully selected for provisional extraction, alongside review, dataset and context records. The pilot identifies heterogeneous evaluation settings, including synthetically paired offline inputs, simulation, closed-track driving and on-road interaction. It also identifies reporting and interpretation issues requiring full-text checking. These observations motivate a claim-to-measurement taxonomy; they do not establish field-wide prevalence, pooled efficacy or an absence of prior intervention evidence. Broader database retrieval, remaining screening and independent human checking are required before conclusions or submission.

## 1. Introduction and positioning

A driver-support system may be described as effective because it classifies emotion accurately, produces a relevant message, is liked by participants, reduces subjective sleepiness, or changes a driving-performance measure. Each can be a legitimate research outcome, but each answers a different question. An evidence map should preserve those distinctions and examine the inferential steps connecting a system's inputs, generated action and claimed benefit.

This problem is not addressed by claiming that prior work stops at emotion recognition. Braun, Weber and Alt's review already synthesizes emotion regulation approaches and methodology [R1]. The driver-monitoring review maps states, indicators and sensors [R2], while the user-supplied HVI review covers cognition, trust, workload, handover and emotional adaptation [R3]. Our provisional focus is narrower: evaluation of generative driver-support assistants, including whether their evidence supports content-quality, human-state or driving claims. Exact novelty remains an open eligibility/overlap question, particularly while ACM and IEEE access is blocked.

## 2. Proposed method and work actually completed

The proposed protocol, inclusion questions and codebook are supplied separately. The initial three arXiv searches were relevance-ranked and capped at 20 returned records per query; they were not exhaustive database exports. Searches were exploratory, and the protocol was written afterward. No preregistration, independent dual screening or inter-rater agreement is claimed.

The combined ledger contains eight purposefully selected original-study records, four review comparators, three adjacent project/context/dataset records, 12 full-text-pending records and 33 title/abstract exclusions **from the pilot**. These categories are not final systematic-review flow counts. Thirteen PDFs were retrieved for targeted section inspection; this does not mean every paper was independently read twice or fully appraised.

For each pilot study, we recorded setting/design, the sample unit and denominator where available, intervention/comparator, measured endpoints, separate human-experience/preference/state/driving fields, source locators and limitations. All extraction remains provisional. Outcome directions are author-reported and have not been reanalyzed. Exact records and searchable provenance are in the associated JSON/CSV files. No newly generated experimental findings appear in this draft.

## 3. Preliminary claim-to-measurement map

| Study | Setting and evaluated object | Evidence that can inform this review | Interpretation boundary |
|---|---|---|---|
| What If Your Car Would Care? [P1] | Affective use-case evaluation; 65 drivers | Perceived benefits and cultural preferences | Preferences about use cases do not establish state regulation or driving benefit |
| Road to Serenity [P2] | Simulator; tactile respiratory guidance | Physiological/subjective response, behavioral measures and individual differences | Preserve the abstract/Methods N discrepancy; this is not LLM dialogue evidence |
| Beyond Voice Assistants [P3] | Voice/embodied assistant; non-driving and on-road tasks | Experience, companionship and perceived risks | Initial interview N=30 must not be assumed to be every experiment's analysis N |
| ChatGPT on the Road [P4] | Motion-based simulator; 40 drivers; no/scripted/ChatGPT agent comparisons | Driving-variability measures, trust and preference | Simulator outcomes do not establish real-road crash reduction or emotion regulation |
| Small Talk, Big Impact? [P5] | Closed-track prototype automation; 40 participants | KSS sleepiness, video/interview evidence and adoption orientations | Fatigue differs from emotion; a single session does not establish long-term benefit |
| Visual and Cognitive Demands [P6] | On-road Gemini Live study; 32 licensed drivers | DRT, gaze and subjective workload relative to specified tasks | Relative workload and visual-demand measures are not universal evidence of safe deployment |
| Multimodal Drivers' Emotion Recognition… [P7] | Offline synthetically aligned road images/emotional speech | Composite emotion/risk/intervention scoring and feasibility of generation | Artificial pairing is not naturally coupled road–driver evidence; generated support is not demonstrated regulation |
| Safety-Aware Evaluation… [P8] | Offline AIDE-derived message evaluation | Rule/LLM-judge metric behavior and agreement | Judge agreement is not ground truth for actual driver load, acceptance or improved state |

The map illustrates why broad claims need endpoint-level scrutiny. It does **not** support the assertion that all current systems are offline, or that no systems have measured human outcomes. The pilot explicitly contains human studies, and the final review must account for their controls and limitations rather than dismissing them.

### 3.1 Input provenance

P7 explicitly describes its multimodal pairs as synthetically aligned, using BDD100K road imagery and CREMA-D emotional speech; it distinguishes this controlled setting from naturally synchronized in-vehicle recordings (Dataset Construction). This is a useful methodological disclosure. The proper inference is that the study evaluates feasibility under the constructed conditions, not that its method is invalid or that driver emotion is naturally caused by the paired road scene.

The adjacent InCarEmo dataset paper [A1] describes scripted in-cabin scenarios, actor preparation and model-assisted dialogue annotation. Such data can support defined recognition tasks, but a driver-support study must separately validate state labels, ecological transfer and intervention effects. Public release, license and current download availability have not been independently verified in this pilot.

### 3.2 Content metrics and human endpoints

P8's DSAIS includes dimensions named cognitive load and driver acceptability, operationalized through rules and model judging. These are not the same measurement instruments as the DRT/eye-tracking/subjective ratings used in P6, or a user's own expressed preference. The draft review should ask what a score actually measures before grouping findings by a familiar metric name.

P4 and P5 provide distinct human outcome evidence: simulator driving measures in one case, and sleepiness/interaction evidence on a test track in the other. Neither should be silently relabelled as proven emotional comfort. Findings should retain their task, exposure duration and comparator boundaries.

### 3.3 Sample accounting and disclosure

P2's abstract reports 85 participants, whereas Methods §2.1 reports 88 recruited, five excluded and a final sample of 83. The discrepancy is recorded for human verification; endpoint-specific denominators must be extracted before any effect-size calculation. This is not a reason to invent a reconciled sample count or allege misconduct.

P6 discloses Google support and involvement in conceptualization, access to Gemini Live/Android Auto and the decision to submit. This belongs in appraisal and transparency fields, not an automatic exclusion rule. P5 separately reports 40 participants but 39 interview transcripts because one participant did not consent to AI-enabled transcription; interview and participant denominators must remain distinct.

## 4. Candidate synthesis contribution

A useful final review could make explicit the chain from **observed input → inferred state/need → selected intervention → evaluated endpoint → supported claim**. It should distinguish inferred affect from requested support, and perceived helpfulness from measured state change. It should also examine whether timing, user control and preferences are studied, rather than infer them from the presence of an emotion classifier.

The candidate contribution is a transparent, updated evaluation map of generative driver support, with historical comparators and reproducibility information. A broad recognition-to-regulation taxonomy alone is insufficiently differentiated from R1. An updated nearest-review search is therefore a go/no-go criterion, not a formality after writing.

Potential subsequent experiments include comparing automated intervention-score rankings against independent human workload/preference judgments, or testing preference-sensitive intervention timing. These are hypotheses derived from an evidence question, not protocols authorized or validated by this review. No new driver data collection or paid experiment is underway.

## 5. Limitations and completion requirements

This pilot is arXiv-biased, relevance-capped, purposefully sampled and extracted by one agent. Important ACM/IEEE/human-factors sources are not yet accessible in the active environment. Twelve full-text eligibility decisions and backward/forward citation checks remain open. Publication status, overlapping study populations, releases/licenses and design-specific risk of bias are not completely reconciled. No quantitative meta-analysis is justified by the current heterogeneous endpoints.

Before submission: restore source access; freeze and, where appropriate, register the revised protocol prospectively; run complete dated searches; reconcile versions/families; complete screening; verify extraction with a human reviewer; conduct appropriate appraisal; update tables/counts; and rewrite abstract/discussion from the completed evidence. Independent review is required even if automated metadata checks pass. The current draft must not be submitted as a finished systematic review.

## Verified reference anchors

R1. Braun, Weber, Alt. Affective Automotive User Interfaces. https://arxiv.org/abs/2003.13731v2 . Retrieved PDF identifies ACM Computing Surveys (2021), DOI 10.1145/3460938.

R2. Halin, Verly, Van Droogenbroeck. Survey and synthesis of state of the art in driver monitoring. https://arxiv.org/abs/2110.00472v1 .

R3. Muzahid, Zhao, Wang. Survey on Human-Vehicle Interactions and AI Collaboration for Optimal Decision-Making in Automated Driving. https://arxiv.org/abs/2412.08005v1 .

P1. What If Your Car Would Care? https://arxiv.org/abs/2004.02481v1 .

P2. Road to Serenity. https://arxiv.org/abs/2406.09777v1 .

P3. Beyond Voice Assistants. https://arxiv.org/abs/2402.11853v2 .

P4. ChatGPT on the Road. https://arxiv.org/abs/2508.08101v1 .

P5. Small Talk, Big Impact? https://arxiv.org/abs/2510.25421v2 . First-post year and the paper's reported conference year differ; verify the final publisher record separately.

P6. Visual and Cognitive Demands of a Large Language Model-Powered In-vehicle Conversational Agent. https://arxiv.org/abs/2601.15034v1 .

P7. Multimodal Drivers' Emotion Recognition and Safety-Oriented Intervention for Intelligent Transportation Systems. https://arxiv.org/abs/2608.06378v1 .

P8. Safety-Aware Evaluation of LLM-Generated Driver Intervention Messages through Multi-Task Risk Fusion. https://arxiv.org/abs/2606.22706v1 .

A1. InCarEmo. https://arxiv.org/abs/2607.14683v1 . Adjacent dataset, not an intervention trial.

Full bibliographic metadata and author lists are preserved in records.json. This reference list does not assert peer review or publication acceptance for all preprints.
