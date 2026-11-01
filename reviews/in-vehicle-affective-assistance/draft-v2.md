# Evaluating Generative In-Vehicle Assistants: From Content Correctness to Human Outcomes

**Expanded working manuscript — not submission-ready; not a completed systematic review.**

## Provisional abstract

Generative in-vehicle assistants are evaluated using heterogeneous outcomes, from factual correctness and tool authorization to perceived interruption, subjective state and driving-related measurements. We propose a scoping review that distinguishes what is evaluated, who supplies the reference judgment, and the setting to which a claim can reasonably transfer. Across an exploratory arXiv retrieval and its expansion, nine query families returned 265 records, corresponding to 230 unique arXiv identifiers; review seeds produced a combined ledger of 233 records. Eighteen original-study publications have been provisionally coded: eight generative support studies, five historical/non-generative comparators and five evaluation-method comparators. This is a purposefully selected evidence map, not a field-wide denominator. Newly inspected work establishes direct precedents for proactive confirmation, communication timing and expert-grounded automated evaluation. These findings preclude broad claims that such problems or validations are absent. Instead, a potentially useful synthesis maps claim-to-measurement boundaries across content, interaction, human state and task outcomes. Database restrictions, incomplete screening, publication-family reconciliation and independent human verification remain substantial limitations.

## 1. Motivation and revised contribution

The relevant question is not simply whether an assistant can recognize emotion or generate plausible responses. It is what an evaluation establishes about the system's intended support function. Content may be factually correct without being welcome; a response may be preferred without changing stress; an acceptable workload result may not establish safer driving. Conversely, work on bounded content correctness can make a valid contribution without proving all downstream outcomes.

A new review must acknowledge mature prior synthesis. The affective automotive review [2003.13731] already covers regulation approaches and methodology. The in-cabin AI survey [2101.02082] organizes safety and comfort applications. The HVI/AI collaboration review [2412.08005] covers cognition, trust, workload, takeover and emotionally aware adaptation. Keep Calm and Relax [2408.09046] also organizes interfaces for trust, comfort and emotion regulation. Therefore, neither "emotion-aware vehicle interfaces" nor a broad sensing-to-intervention diagram is an adequate novelty claim.

The proposed contribution is an updated, claim-oriented map of generative in-vehicle assistant evaluation, with separate comparison strata and reproducibility information. Whether this is sufficiently distinct from recent dedicated reviews remains to be established through complete publisher/index searches.

## 2. Methods and actual progress

The protocol was developed after the exploratory search and is not preregistered. The original pilot remains available unchanged. Six additional query families cover in-car conversation, proactive agents, affective interventions, closest reviews, exact citation leads and a focused review check. Pagination was attempted to a prespecified resource cap of two 30-record pages for the first five expanded queries; three exhausted that cap. The focused review check used one page. A short result page indicates only that the endpoint pagination was exhausted for that particular query, not that the research topic is exhaustively covered.

The corpus ledger contains 233 candidate records, not 233 included studies. Of these, 13 original publications are in the primary/historical support map, five are evaluation-method comparators, six are review comparators and three are adjacent project/context/dataset records. Thirty-three retain their original pilot-only exclusions; seven original full-text decisions and 14 prioritized new candidates remain pending, while 152 new records have not been formally screened. These counts are reported to expose the remaining workload, not as a completed PRISMA flow.

Thirteen original-pilot PDFs and twelve new PDFs were retrieved and inspected in targeted sections. This does not constitute independent dual-reviewer assessment of all full texts. Exact query strings, source metadata, retrieval/page counts and file fingerprints are supplied. ACM/IEEE and three metadata sources remain inaccessible; a failed connection is not treated as an empty search. All extraction remains provisional and requires human checking.

## 3. What the newly inspected work changes

### 3.1 Proactivity and timing are established research subjects

Towards Proactive Interactions [2403.09135] defines levels along autonomy and assumption dimensions and reports feasibility and a subjective study with 40 participants. Its finding about strong assumptions with user confirmation is bounded by its conversational-simulator/user-perception setting; it is not proof of reduced accidents.

ProVoice [2601.19421] studies human-in-the-loop multi-objective design optimization in a VR driving simulator (N=19). It examines mental demand, predictability and usefulness. Because the intervention-design procedure is computational, it should not automatically be called a generative-language study.

When2Talk [2609.12503] compares event-triggered communication with Immediate/Delayed/Silent context-sensitive communication for 41 passengers in CARLA/VR fully automated rides. Both policies use the same canonical message when speaking. The policy comparison therefore addresses timing while controlling message content; it is relevant prior work, but its passenger findings cannot simply be transferred to active-driver workload.

### 3.2 Progress feedback has a distinct evidence base

What Are You Doing? [2602.15569] compares planned/intermediate feedback with final-only responses in a 45-person study. The apparatus includes a mouse-controlled lane-keeping dual task and a stationary condition. Perceived latency, trust, experience and task load are meaningful endpoints. Their setting must remain explicit rather than be summarized as an on-road safety intervention.

The existing pilot's ChatGPT simulator study [2508.08101], closed-track passive-fatigue study [2510.25421] and on-road visual/cognitive-demand study [2601.15034] address different outcomes. The expanded map must preserve those differences instead of collapsing them under "human evaluation".

### 3.3 Human preference is not the same as human state change

KYA [2607.16181] combines risky-dashcam-event perception with generated emotional response styles. Its evaluation includes 108 survey respondents and 20 video sequences. Anonymized response comparisons and style/adoption preferences supply human judgments; thus it would be false to call the work entirely unvalidated by humans. The inspected survey does not establish emotion regulation during actual driving, and public-platform video input does not make the survey a live driver intervention trial.

This differs from the synthetic-pair evaluation in [2608.06378], which explicitly uses independently collected road imagery and acted emotional speech. Both can evaluate their defined systems, but they represent different kinds of input provenance and human grounding.

### 3.4 Automated evaluation already has expert-grounded examples

InCA [2311.07469] compares model-based judgments with human annotations for domain-specific dialogue KPIs. Automated Factual Benchmarking [2504.01248] compares vehicle-manual-grounded evaluation against expert judgments. Automated Multi-Turn Evaluation [2609.35812] uses twelve annotators on 37 generated dialogues, alongside an industrial assistant with six backends. These establish prior work on human-referenced evaluation and multi-turn failures.

The remaining question is therefore not whether any judge has human agreement, but whether the validated construct matches the downstream claim. Expert agreement about vehicle-manual facts does not validate a stress measure. Dialogue annotation is not a driver workload study. A simulated user/assistant conversation loop is not closed-loop control of a physical vehicle. Repeated clustering or sampling on the same conversations must not be counted as independent study samples.

CAR-bench [2601.22027] already examines consistency, disambiguation and limit-awareness in a synthetic tool environment. The voice-command authorization benchmark [2609.19630] separately evaluates seven pre-action decision classes. Merely introducing clarification, confirmation or abstention would therefore not constitute a new contribution.

## 4. Revised synthesis framework

We propose four independent outcome layers:

| Layer | Examples | Appropriate evidence | Inference to avoid |
|---|---|---|---|
| Content/task correctness | factuality, constraints, tools, authorization | expert/reference checks and bounded task outcomes | correctness implies acceptance or emotional benefit |
| Interaction | timing, verbosity, confirmation, interruption, control | identified user-role/context studies and preference measures | passenger preference equals active-driver safety |
| Human state | affect, stress, sleepiness, physiological response | construct-specific instruments and valid comparisons | acted emotion labels or generated empathy imply regulation |
| Driving/task consequences | control variability, takeover, attention/workload | scenario- and role-specific task measurements | a proxy or short exposure establishes real-world crash reduction |

These layers are not a score hierarchy. A system need not evaluate every layer to be publishable; it must avoid claiming evidence it did not collect. Human annotators, users, passengers and active drivers should be separate populations. Distinguish inferred affect, explicit support requests and consent to intervention. The four-layer taxonomy remains a proposed synthesis device requiring comparison with previous reviews and human validation, not an established novel theory.

## 5. Reproducibility and study-family boundaries

The public CAR-bench README was accessible and describes a synthetic environment, API-backed evaluation and external dataset hosting. No benchmark was run and no API keys were supplied. The feedback-study supplement was accessible and lists condition videos and a qualitative codebook; it is not the same thing as open raw participant data. The AIDE repository README and CREMA-D documentation were accessible, but this does not prove all dataset access/licensing conditions are satisfied. CREMA-D's acted speech is not naturally synchronized in-car affect.

InCA and the factual benchmark both concern the CarExpert evaluation context. This suggests a platform-level family requiring traceability; it does not prove overlapping participants or justify automatically merging them into one study. Similar authorship is not enough to infer duplicate samples. The original pilot's sample-count discrepancy and sponsor-disclosure notes remain unresolved human-check items.

## 6. Research agenda to test, not assume

An empirical agenda could examine whether factual-correctness, message-quality and preference measures predict independently measured workload or state outcomes across contexts. Such a study requires paired observations and appropriate human data; this review does not create those labels or authorize collection. Another candidate concerns how response timing, user confirmation and support preferences interact, but When2Talk, ProVoice and the 2024 proactivity framework are necessary baselines and may already cover parts of that question.

Do not extrapolate a claimed research gap from absent search results while sources are blocked. A defensible agenda must be updated after publisher/index searches, remaining screening and study-specific appraisal.

## 7. Limitations and completion gates

This remains an expanded arXiv-focused evidence map, with noisy broad queries, capped pagination, incomplete eligibility screening and single-agent extraction. Human outcome designs and benchmarks are too heterogeneous for a pooled effect-size claim. Publication status, endpoint denominators, outcome validation, allocation/ordering, disclosure, overlapping data and release conditions need systematic checking. The number of retrieved records is neither a completeness measure nor evidence of novelty.

Before submission, complete broader searches and citation chaining, verify the closest recent reviews, finish screening, perform human extraction checks, reconcile study families, appraise evidence using design-appropriate questions and rewrite conclusions from the final included corpus. There were no paid model calls, experiments or public submissions during this expansion.

## Verified reference links for the expanded synthesis

- [2003.13731v2] Affective Automotive User Interfaces -- Reviewing the State of Emotion Regulation in the Car. https://arxiv.org/abs/2003.13731v2
- [2110.00472v1] Survey and synthesis of state of the art in driver monitoring. https://arxiv.org/abs/2110.00472v1
- [2412.08005v1] Survey on Human-Vehicle Interactions and AI Collaboration for Optimal Decision-Making in Automated Driving. https://arxiv.org/abs/2412.08005v1
- [2101.02082v1] Artificial Intelligence Methods in In-Cabin Use Cases: A Survey. https://arxiv.org/abs/2101.02082v1
- [2408.09046v1] Keep Calm and Relax -- HMI for Autonomous Vehicles. https://arxiv.org/abs/2408.09046v1
- [2403.09135v1] Towards Proactive Interactions for In-Vehicle Conversational Assistants Utilizing Large Language Models. https://arxiv.org/abs/2403.09135v1
- [2601.19421v1] ProVoice: Designing Proactive Functionality for In-Vehicle Conversational Assistants using Multi-Objective Bayesian Optimization to Enhance Driver Experience. https://arxiv.org/abs/2601.19421v1
- [2609.12503v1] When2Talk: When Should a Proactive In-Car Agent Talk?. https://arxiv.org/abs/2609.12503v1
- [2602.15569v2] What Are You Doing? Effects of Intermediate Feedback from Agentic LLM In-Car Assistants During Multi-Step Processing. https://arxiv.org/abs/2602.15569v2
- [2607.16181v1] Vision-Language Assistant for Emotional Reactions to Risky Driving. https://arxiv.org/abs/2607.16181v1
- [2311.07469v2] InCA: Rethinking In-Car Conversational System Assessment Leveraging Large Language Models. https://arxiv.org/abs/2311.07469v2
- [2504.01248v1] Automated Factual Benchmarking for In-Car Conversational Systems using Large Language Models. https://arxiv.org/abs/2504.01248v1
- [2609.35812v1] Automated Evaluation of Multi-Turn Dialogues in In-Car Conversational Assistants. https://arxiv.org/abs/2609.35812v1
- [2601.22027v1] CAR-bench: Evaluating the Consistency and Limit-Awareness of LLM Agents under Real-World Uncertainty. https://arxiv.org/abs/2601.22027v1
- [2609.19630v1] From Intent to Action: Benchmarking LLM Safety in Vehicle Voice Command Authorization. https://arxiv.org/abs/2609.19630v1
- [2508.08101v1] ChatGPT on the Road: Leveraging Large Language Model-Powered In-vehicle Conversational Agents for Safer and More Enjoyable Driving Experience. https://arxiv.org/abs/2508.08101v1
- [2510.25421v2] Small Talk, Big Impact? LLM-based Conversational Agents to Mitigate Passive Fatigue in Conditional Automated Driving. https://arxiv.org/abs/2510.25421v2
- [2601.15034v1] Visual and Cognitive Demands of a Large Language Model-Powered In-vehicle Conversational Agent. https://arxiv.org/abs/2601.15034v1
- [2608.06378v1] Multimodal Drivers' Emotion Recognition and Safety-Oriented Intervention for Intelligent Transportation Systems. https://arxiv.org/abs/2608.06378v1
