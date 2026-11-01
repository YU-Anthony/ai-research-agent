# Proposed scoping-review protocol v0.1

Status: written after the exploratory pilot, not preregistered. Human review and a final scope decision are needed before freezing the protocol. Pilot cutoff: 2026-11-01; a full search should record its actual completion date separately.

## Question and scope

What evidence supports claims that generative/conversational in-vehicle assistants provide useful driver support, and how are content quality, user preference, driver state and driving outcomes distinguished?

Core population/context: drivers or occupants interacting with an in-vehicle support assistant in manual or automated driving; report driver/passenger and automation roles separately. Core systems: LLM/generative assistants or multimodal systems generating driver-facing support/intervention messages. Older non-generative systems are a separately labelled comparison set, not silently pooled with generative systems. Emotion/stress regulation, passive-fatigue support and interaction workload are separate constructs; their inclusion is justified by driver-support evaluation and must not imply equivalent psychological outcomes.

Proposed core date range: 2023 to search completion; historical comparator/citation searches may precede 2023. The exploratory searches did not impose this date filter. English-language full-text review is proposed; language bias must be disclosed. This is an evidence-mapping/scoping review, not a clinical efficacy review or a meta-analysis.

## Research questions

RQ1. Which driver/occupant states and support needs are represented, and who labels them (self-report, observed behavior, physiology, acted speech, annotator or model)?

RQ2. Are modalities naturally synchronized, independently collected and synthetically paired, or generated? What does this allow the evaluation to establish?

RQ3. Does the system select when/whether to intervene, generate what to say, or merely score an existing message? Are user requests, explicit refusal, workload and road risk considered?

RQ4. Which outcomes are directly measured: recognition, content correctness/relevance, preference, subjective state, physiological state, workload, driving performance or longitudinal adoption?

RQ5. What comparison, allocation, sample accounting, masking, follow-up and measurement practices support the stated claim? Do metric labels match what was actually measured?

RQ6. What data, code, evaluation prompts and human-feedback records can be reused for reproducible experiments without confusing an offline proxy with real driver benefit?

## Eligibility

Include original evaluation studies addressing a core driver-support system and at least one observable evaluation endpoint. Include offline generation/metric studies as a distinct category even without human trials. Explicitly distinguish prototypes, validation studies, controlled human studies and observational work. Datasets, recognition-only systems, reviews and project descriptions may inform background but are not counted as completed support-intervention trials. Exclude unrelated robotics/general emotional-support work from the primary synthesis unless an explicit cross-domain comparison is prespecified. Manufacturer descriptions without evaluation are context, not outcome evidence.

Do not exclude a study solely because findings are negative, the method is non-LLM, it is a preprint, or a sponsor is involved. Record those properties separately. Verify publisher status independently; placeholder conference templates and an arXiv identifier do not establish acceptance. Do not interpret absence of a field in this pilot extraction as absence from the paper.

## Search plan and actual pilot

The exact executed arXiv strings and request limits are in search-log.json. Every pilot query requested only the top 20 results by relevance, with no exhaustive pagination; these searches cannot establish completeness. Three search families cover affective automotive interaction, conversational assistants, and emotion/context interventions.

For the complete review: search ACM Digital Library, IEEE Xplore and an interdisciplinary index available to the researcher; supplement with Crossref/OpenAlex/Semantic Scholar metadata and arXiv preprints. Publisher sites, indexes and metadata services are not equivalent independent databases: record coverage/overlap and each export's provenance. Validate controlled-vocabulary variants and run dated queries with complete pagination/export, limits and result counts. Search words should include vehicle/car/in-cabin/automotive, conversational/voice/LLM/generative/empathic, and support/regulation/assistance/intervention/workload. Keep emotion/stress and fatigue strata explicit. Screening pilots may motivate revisions, which must be documented rather than retroactively described as prespecified.

Conduct backward/forward citation checks on the nearest affective-UI review, the user-supplied HVI review and each included primary study. Seeds identified in references but not read remain unverified leads. Metadata API access and an ACM/IEEE landing page do not imply a full-text download license.

## Screening, deduplication and extraction

Deduplicate by DOI and arXiv base ID first, then title/authors/study family. A preprint and its journal version are one publication family; overlapping participants/experiments across papers must be identified before counts are interpreted. Preserve which version was coded and record changes if the full text differs.

Pilot screening/extraction is single-agent and provisional; no second reviewer or inter-rater statistic exists. Ask a human reviewer to verify all eight pilot extractions, ambiguities and exclusions before scaling. Where independent dual screening is feasible, record disagreement resolution honestly; do not claim it was performed merely because it is recommended.

Use codebook.md and source locators. Distinguish recruited, analyzed, task-specific and interview Ns. Keep discrepancies and not-extracted values explicit. Log outcome direction as author-reported; numerical effect extraction requires denominator, variance, unit, comparator and analysis design verification. Avoid causal effectiveness claims from observational association or uncontrolled preference ratings.

## Synthesis and appraisal

Produce evidence tables, an outcome-by-setting matrix and claim-to-measurement examples. No pooled effects are planned because interventions, constructs, comparators and outcomes differ. AURC/F1/LLM judge score, KSS, subjective satisfaction, DRT and lane variability must not be averaged into one "effectiveness" metric.

Develop design-appropriate appraisal questions covering data provenance, allocation, sample/exclusion accounting, independent outcome validity, measurement/model circularity, missing data, task realism, disclosure and reproducibility. Do not assign a numerical quality score until its rationale is reviewed. Treat a lack of real-road validation as a limit on transportability, not proof of poor offline research.

Stop/reframe if a recent review already provides the same evaluation taxonomy and updated evidence coverage, or if a complete search yields too little coherent core evidence. Do not add unrelated studies merely to reach a paper-count target.

## Outputs and authorization

Deliver a checked bibliography, transparent screening record, evidence/codebook tables, overlap analysis, manuscript draft and candidate experiment questions. No new driver study, real-world intervention, paid experiment, manuscript submission or aiXiv posting is authorized. The final manuscript requires explicit human review and submission approval.
