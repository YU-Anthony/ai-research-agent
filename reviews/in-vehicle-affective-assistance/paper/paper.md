# Evaluating Generative In-Vehicle Assistants: From Content Correctness to Human Outcomes

**Author-review draft.** This manuscript develops an exploratory evidence map. Database coverage, eligibility screening and human verification are incomplete. It must not be represented or submitted as a completed systematic review. Author names, affiliations and submission venue are intentionally not supplied.

## Abstract

Generative in-vehicle assistants can answer questions, initiate conversations, communicate task progress and produce context-dependent support messages. Evaluating these capabilities requires more than measuring response fluency or task completion: a correct answer, a preferred interaction, a change in driver state and an improvement in driving performance are distinct outcomes. This article develops a structured exploratory evidence map of evaluation practices for generative driver-support assistants, with historical and methodological comparators. Nine arXiv query families returned 265 records, corresponding to 230 unique identifiers; review seeds produced a combined ledger of 233 candidate records. Eighteen original-study publications were provisionally coded, comprising eight generative core studies, five non-generative or historical comparators and five evaluation-method comparators. We organize their evidence across content correctness, interaction quality, human state and driving/task consequences, while separately identifying participant role, input provenance and experimental setting. The inspected literature includes expert-grounded automated evaluation, human preference studies, simulator experiments and real-vehicle interaction studies. Consequently, neither the absence of human validation nor the absence of intervention research is a defensible general characterization. The central synthesis concerns how claims should remain bounded by the constructs, populations and settings actually evaluated. Broader retrieval, complete screening, publication-family reconciliation and independent human checking are needed before field-wide conclusions or submission.

**Keywords:** in-vehicle conversational assistants; generative AI; driver support; multimodal interaction; affective interfaces; human-centered evaluation; evidence mapping.

## 1. Introduction

In-vehicle assistants increasingly combine language generation with contextual information about the vehicle, journey or occupant. Their possible functions include explaining vehicle features, clarifying ambiguous requests, offering proactive suggestions and adapting conversational responses to perceived affect. These functions create evaluation questions that extend beyond whether a model produces linguistically plausible text. An explanation can be factually correct yet arrive at an inconvenient moment. A conversational style can be preferred without changing stress. A system can perform well in a simulated tool environment while leaving the effects of actual interaction with a driver untested.

The literature already contains substantial work on these questions. In-car dialogue assessment examines domain-specific criteria and agreement with expert judgments [1, 2]. Proactivity and communication timing have been studied through conversational simulators and virtual-reality experiments [3, 4, 5]. Other investigations examine conversational agents using driving simulators, closed test tracks or on-road workload measurements [6, 7, 8]. The challenge for synthesis is therefore to preserve distinctions among evaluation targets while explaining how the evidence relates to the claims made for a system.

This issue is particularly relevant to affect-aware assistance. Recognizing an emotion label, inferring a need for support, deciding whether to speak and delivering a useful intervention are related but separate tasks. Their separation is visible in the contrast between synthetic-pair multimodal generation, response-preference surveys and studies measuring human state or task outcomes [7, 9, 10, 11]. A review that groups all of them under a single category of effective assistance risks obscuring the contribution and limitations of each.

Earlier reviews already organize much of the background. Braun, Weber and Alt synthesize affective automotive interfaces and emotion-regulation approaches, including methodological considerations [12]. Driver monitoring and in-cabin AI surveys organize states, indicators, sensing methods and safety/comfort applications [13, 14]. The human–vehicle interaction review covers cognition, trust, workload, handover and emotionally aware adaptation [15], while Keep Calm and Relax discusses interfaces for trust and comfort in automated vehicles [16]. Our proposed focus is the relationship between evaluation constructs and claims in generative in-vehicle assistance. It does not establish a new field merely by connecting emotion recognition to intervention.

The present draft offers three provisional contributions: a traceable map of selected evaluation studies; a four-layer organization of their measured outcomes; and a discussion of boundaries that should be respected when transferring findings between tasks, people and settings. These are synthesis proposals requiring comparison with additional reviews and human verification. We do not introduce a new assistant, report new driver experiments or claim that the retrieved corpus is exhaustive.

## 2. Scope, terminology and review questions

### 2.1 System scope

We use **generative in-vehicle assistant** for a system that uses a generative model to produce context-dependent language or agentic responses in an automotive interaction. This includes conversational support and some tool-oriented functions, but it does not imply autonomous control of the vehicle. A voice interface is not automatically generative: a system may select fixed messages or optimize when they are delivered. Such systems can be informative comparators without being counted as generative support systems [4, 5].

The core interest is driver support. Passenger interaction and generic in-car question answering are retained only where their role is explicit. Automated factual or tool benchmarks inform measurement methodology, rather than being treated as studies of emotional support. Likewise, historical respiratory guidance and affective-interface work provide comparisons without being relabelled as language-model interventions [11, 17, 18].

### 2.2 Distinct constructs

An inferred affective state is not equivalent to an explicit request for help or permission to intervene. Preference for a response style is not equivalent to an emotional change following exposure to that response. Fatigue, stress, trust and workload also require separate interpretation. For example, a sleepiness scale used during conditional automated driving addresses a different construct from preference ratings for emotionally expressive text [7, 10].

Experimental roles matter as well. Active drivers, passengers in fully automated rides, survey respondents and dialogue annotators have different tasks and exposure. These roles cannot be combined under an undifferentiated label of human evaluation. Their actual study settings and measurements must accompany any synthesis.

### 2.3 Review questions

This exploratory map addresses four questions:

1. **What is evaluated?** Which system functions and support claims are operationalized as tasks or outcomes?
2. **What grounds the evaluation?** Are judgments based on expert references, model-generated scores, subjective reports, observed behavior, physiological measures or driving/task performance?
3. **Where and for whom does the evidence apply?** What roles, data provenance, settings and exposure durations constrain interpretation?
4. **What remains to be demonstrated?** Which inferential links require additional evidence before content quality or interaction preference can support stronger human-outcome claims?

## 3. Review approach and current corpus

### 3.1 Retrieval and provenance

The work began as an exploratory pilot and was subsequently expanded. The retained retrieval snapshot is dated 1 November 2026; exact extraction timestamps are recorded in the source logs. The protocol was written after initial retrieval and is not preregistered. The original round used three arXiv query families capped at 20 results each. Six additional families addressed in-car conversation, proactive assistants, affective interventions, nearest reviews and citation-specific leads. The first five expanded queries allowed up to two pages of 30 results; three reached that cap. A focused review check used one page. Exact strings, offsets, result counts and metadata are retained in the accompanying search logs.

Across both rounds, 265 returned records corresponded to 230 unique arXiv base identifiers. Additional review seeds produced a ledger of 233 candidate records. These are retrieval counts, not the number of relevant or included studies. Broad queries produced substantial irrelevant material; neither a large candidate count nor pagination exhaustion for a particular query establishes coverage of a research topic.

Attempts to access ACM, IEEE, Crossref, OpenAlex and Semantic Scholar failed under the active environment's network policy. These failures are recorded as access failures, not zero-result searches. The present evidence base is therefore arXiv-focused and cannot support a claim of complete coverage of automotive HCI, human factors or affective computing.

### 3.2 Selection and evidence strata

Eighteen original-study publication records were purposefully selected for provisional coding. Eight concern generative driver-support functions, five are non-generative or historical comparators, and five concern evaluation methodology. These strata are kept separate because their purposes and evidential units differ. A publication count is not a count of independent trials, participant cohorts or datasets.

The wider ledger also contains six review comparators and three adjacent context/project/dataset records. Seven original full-text decisions and 14 prioritized candidates remain pending; 152 new records have not been formally screened. Thirty-three records retain their first-round pilot exclusions. This is an auditable account of unfinished selection, not a completed systematic-review flow diagram.

### 3.3 Extraction and synthesis

Twenty-five PDFs were obtained across the two rounds and inspected in targeted method and result sections. Extracted fields include design, setting, sample accounting, intervention/comparator, endpoints, source locators and interpretation limits. The evidence table separately records human experience, preference, state measures, driving-related performance and real-vehicle interaction. All extraction is single-agent and provisional; no independent human verification or inter-rater agreement is claimed.

Our synthesis is qualitative. We do not pool effect sizes or average scores across incompatible outcomes. An expert-factuality agreement, a subjective preference, a sleepiness measure and lane variability should not be combined into one estimate of assistant effectiveness. Numerical results from individual papers are used sparingly because endpoint-specific denominators, variance and study-family relationships have not been completely reconciled.

## 4. A claim-to-measurement framework

We organize evaluation into four layers, treating them as distinct questions rather than a quality ranking.

| Layer | Evaluation target | Typical reference or measurement | Claim boundary |
|---|---|---|---|
| Content and task correctness | Facts, constraints, dialogue continuity, tool decisions | Expert/reference labels, execution rules, annotated conversations | Correctness does not itself establish welcome or beneficial intervention |
| Interaction quality | Timing, verbosity, proactivity, confirmation, user control | Context-specific preferences, perceived interruption, trust and usability | Experience in one role or setting does not automatically transfer to another |
| Human state | Stress, affect, sleepiness or other specified state | Construct-specific self-report, behavior or physiological measures | Recognition labels and generated empathy are not evidence of state regulation |
| Driving and task consequences | Driving control, takeover, attention or workload | Appropriate scenario- and role-specific task measures | A short exposure or proxy does not establish population-wide crash reduction |

The final layer contains different endpoint families that must still be distinguished. Workload, gaze behavior and direct vehicle-control performance are not interchangeable. A paper can contribute at any one layer; the requirement is that its conclusions remain aligned with the measurement it performed.

A practical extraction unit is therefore **function → reference source → measured endpoint → supported claim → transfer boundary**. For example, a factuality evaluator may be supported by expert agreement but remain unvalidated as a measure of emotional benefit. A passenger timing study may identify preferred communication policies without measuring active-driver distraction. The framework makes these boundaries visible; it is not presented as a validated scale or proven novel taxonomy.

## 5. Evidence on support and interaction

### 5.1 Historical comparisons: affect, embodiment and regulation

Historical work provides useful reminders that user-centered vehicle support predates generative language models. What If Your Car Would Care? evaluates affective use cases with 65 drivers in Germany and China, providing evidence about perceived benefits and cultural preferences [17]. Beyond Voice Assistants examines an embodied assistant through initial interviews, non-driving tasks and on-road experiences [18]. These studies inform expectations about companionship and interaction, but preference and perceived reassurance should not be relabelled as measured emotion regulation.

Road to Serenity examines tactile respiratory guidance in a driving simulator and analyzes physiological, subjective and behavioral responses together with individual differences [11]. It supplies a comparison for the kinds of human-state measurements that an intervention can require. It also illustrates the importance of sample accounting: the abstract reports 85 participants, whereas Methods describes 88 recruited, five excluded and 83 in the final sample. We retain this discrepancy for human checking rather than select a denominator or calculate a pooled effect. Individual endpoint denominators remain to be reconciled.

These comparisons prevent a misleading narrative in which all earlier research is reduced to recognition accuracy. The appropriate distinction is the evaluated function and outcome, not simply whether a system contains an LLM.

### 5.2 Proactivity, communication timing and progress feedback

Towards Proactive Interactions defines proactivity through autonomy and assumption dimensions and evaluates five levels using feasibility and subjective experiments, including 40 participants [3]. Its reported preference for strong assumptions combined with user confirmation makes confirmation an established research variable. It does not establish a general rule that every proactive intervention improves safety.

ProVoice uses human-in-the-loop multi-objective design optimization in a VR driving simulator with 19 participants, examining mental demand, predictability and usefulness [4]. The study connects design choices to multiple user-experience objectives. Its value as a comparator does not depend on assuming that a voice interface is generative or that optimization is equivalent to emotional support.

When2Talk studies 41 passengers in a CARLA/VR fully automated ride, comparing an event-triggered policy with a context-sensitive policy that can communicate immediately, delay or remain silent [5]. When both policies speak, they use the same canonical message. This is an important design distinction: the comparison concerns communication selection and timing while controlling message content. Passenger activity and event priority provide a basis for interpreting interruption findings, but the role and task do not match those of an active driver.

What Are You Doing? studies planned-step and intermediate-result feedback against final-only responses in a 45-person design with stationary and dual-task conditions [19]. The apparatus includes a mouse-controlled lane-keeping simulation. Perceived latency, trust, experience and task-load findings can inform agentic feedback design; the setting should remain visible when describing their implications. Feedback that improves perceived responsiveness may still require evaluation under different interaction demands and driving conditions.

Together, these publications show that proactivity, confirmation, timing and verbosity already have an empirical foundation. A new system cannot claim novelty merely by adding these features. A stronger evaluation would specify which existing design decision it changes and how its comparator isolates that change.

### 5.3 Generative conversation and human outcomes

ChatGPT on the Road compares no-agent, scripted-agent and ChatGPT-based interaction in a motion-based driving simulator with 40 drivers [6]. Its author-reported driving-variability, trust and preference findings constitute evidence tied to that simulator and those comparators. They should not be generalized into a demonstrated reduction in real-world crashes or a demonstrated emotional-regulation effect.

Small Talk, Big Impact? investigates a conversational agent during conditional automated driving on a closed test track with 40 participants [7]. Its use of sleepiness ratings, behavioral video and interviews addresses passive fatigue and interaction experience. The paper also distinguishes participant and interview denominators: 39 transcripts were analyzed because one participant did not consent to AI-enabled transcription. The single-session exposure, prototype automation and variable agent latency constrain interpretation. Passive-fatigue outcomes are informative for driver support, but fatigue should not be treated as another label for emotional distress.

Visual and Cognitive Demands evaluates Gemini Live interactions on-road with 32 licensed drivers, using comparison tasks including navigation, phone conversation and OSPAN [8]. DRT, gaze and subjective workload measurements address interaction demands. They are different evidence from response preference or vehicle-control measures. The inspected paper discloses sponsor involvement in conceptualization, system access and the decision to submit; disclosure belongs in appraisal, without automatically invalidating the study or resolving its interpretation.

This group demonstrates that human and real-vehicle evidence does exist. Its heterogeneity also makes a single verdict about whether conversational assistance is beneficial inappropriate at the current stage. The relevant synthesis must retain who interacted, what they did, the comparator and the endpoint.

### 5.4 Emotion-aligned generation and response preference

The multimodal safety-intervention framework in [9] combines road imagery and emotional speech to generate risk reports and emotion-aligned verbal responses. Its Dataset Construction section explicitly identifies the pairs as synthetically aligned rather than naturally synchronized in-vehicle recordings. This disclosure defines the evidence boundary: a controlled multimodal-generation evaluation can test feasibility under its construction, but does not establish a naturally observed relationship between a particular driver's affect and the paired road situation.

The Driver Safety-Aware Intervention Score evaluates generated messages through rules and model judging, with dimensions including contextual relevance, cognitive load and driver acceptability [20]. Those labels should be interpreted through their operational definitions. A linguistic or judge-based proxy called cognitive load is not the same instrument as a DRT or a workload report from an exposed driver. Agreement between judges assesses consistency among those judges; validation against the intended human construct remains a separate question.

KYA includes 108 survey respondents evaluating emotional response styles, alongside perception input from 20 dashcam sequences [10]. Anonymized response comparisons and preference/adoption judgments supply human grounding. It would therefore be inaccurate to describe the work as lacking human evaluation. However, the inspected survey is not an intervention trial that measures emotion changes while participants drive. The distinction allows the study's preference evidence to be acknowledged without assigning it an unmeasured regulatory effect.

### 5.5 Summary of selected support evidence

| Publication | Role and setting | Main evaluation focus | Important boundary |
|---|---|---|---|
| What If Your Car Would Care? [17] | Affective use-case evaluation | Perceived benefits and cultural preferences | Use-case preference is not measured regulation |
| Road to Serenity [11] | Simulator respiratory intervention | State response, behavior and individual differences | Non-conversational comparator; sample discrepancy unresolved |
| Beyond Voice Assistants [18] | Embodied assistant; non-driving/on-road | Experience, companionship and perceived risks | Interview sample must not substitute for every task sample |
| ChatGPT on the Road [6] | Driver simulator comparison | Driving variability, trust and preference | Simulator result is not real-road crash evidence |
| Small Talk, Big Impact? [7] | Closed-track automated driving | Sleepiness, behavior and interaction experience | Fatigue and emotion are distinct; short-term exposure |
| Visual and Cognitive Demands [8] | On-road task comparison | DRT, gaze and workload | Relative workload does not establish universal safety |
| Multimodal safety intervention [9] | Offline synthetic pairing | Emotion/risk/intervention generation | Pairing does not establish natural coupling or regulation |
| Safety-aware message evaluation [20] | Offline generated-message evaluation | Composite rule/judge scores | Named human outcomes may be proxies |
| Towards Proactive Interactions [3] | Conversation simulator | Proactivity levels and confirmation | Perceived utility is not a driving-outcome measure |
| What Are You Doing? [19] | Stationary/dual-task laboratory study | Feedback, perceived latency, trust and load | Lane-keeping surrogate differs from on-road driving |
| KYA [10] | Response survey and dashcam input | Emotional alignment and style preference | No measured emotion-regulation effect in driving |
| ProVoice [4] | VR design optimization | Mental demand, predictability and usefulness | Comparator status should remain separate from generative systems |
| When2Talk [5] | Automated-vehicle passenger VR | Timing, appropriateness and interruption | Passenger evidence cannot be transferred directly to active drivers |

## 6. Automated evaluation, references and agent reliability

### 6.1 Expert grounding is already part of the literature

InCA evaluates domain-specific conversational criteria using model judgments and comparison with human annotations [1]. Automated Factual Benchmarking compares vehicle-manual-grounded judgments with expert evaluations [2]. Their existence rules out a broad assertion that in-car automated evaluation has no human reference. The more precise question is the domain and construct over which agreement has been demonstrated.

A factual answer can be evaluated against a manual when the relevant statement is identifiable. Appropriate emotional support is less readily reduced to one textual reference. The distinction is methodological: success on one reference-grounded task does not automatically validate a score for a different construct. It also does not make factual evaluation unimportant. An assistant explaining vehicle functions requires reliable factual grounding even when its longer-term human effects remain outside the study.

### 6.2 Multi-turn assessment changes the unit of analysis

Automated Evaluation of Multi-Turn Dialogues uses an industrial assistant with six model backends and compares automated judgments with twelve annotators on 37 generated conversations [21]. The human reference concerns conversations and evaluation criteria, not drivers exposed to an assistance intervention. Its simulated-user loop is a conversation-testing mechanism, not a closed vehicle-control loop.

This distinction matters when reporting sample size and replication. Conversations, turns, annotations, model backends and repeated clustering procedures are different units. Repeated analysis of the same dialogues does not create additional independent participants. A review should preserve those units and the level at which agreement or failure is assessed.

### 6.3 Reliability includes decisions not to execute

CAR-bench investigates consistency and limit-awareness using simulated users and a tool environment, including ambiguity and missing-capability tasks [22]. The vehicle voice-command authorization benchmark separates pre-action choices such as execution, refusal, clarification, confirmation and deferral across reference scenarios [23]. Both are important precedents for capability-sensitive behavior.

Their scope also identifies a boundary. A model's correct decision label is not itself an independent enforcement mechanism, and successful simulated tool interaction is not evidence of safe real-vehicle operation. Reference decisions, policy compliance and execution constraints should therefore be evaluated and described separately. A system incorporating refusal or clarification must be compared against this existing work rather than present those behaviors as a new research problem.

| Evaluation comparator | Reference and unit | Established evaluation target | Downstream construct not established by that target alone |
|---|---|---|---|
| InCA [1] | Domain-specific expert/model dialogue judgments | Conversational KPIs | Driver-state change |
| Factual benchmark [2] | Expert evaluation of manual-grounded answers | Factual correctness | Preference, support need or emotional benefit |
| Multi-turn evaluation [21] | Annotators and generated conversations | Dialogue failures and conversation quality | Driver workload or vehicle-control safety |
| CAR-bench [22] | Synthetic-user/tool tasks | Consistency, ambiguity and limit-awareness | Actual occupant acceptance or support efficacy |
| Authorization benchmark [23] | Reference scenarios and decision classes | Pre-action authorization alignment | Enforced physical-system safety |

## 7. Cross-cutting methodological issues

### 7.1 Input provenance and ecological correspondence

An evaluation should make clear whether its modalities were recorded together, independently collected and paired, or generated. Synthetic pairing can isolate a defined task and enable controlled comparisons. It does not establish that the combined signals co-occur in a real person's experience. Similarly, acted emotional speech supports defined recognition tasks without supplying ground truth for a driver's support needs.

This affects interpretation across the assistant pipeline. A classifier trained on affect labels may inform a generation prompt, but the label does not by itself establish a wish to receive a particular intervention. Reusing a recognition dataset for message generation therefore requires an explicit account of the newly introduced supervision and evaluation target [9, 20].

### 7.2 Alignment between a named metric and its construct

Terms such as trust, acceptability, cognitive load and safety can conceal different operationalizations. A named dimension in an automated score, a questionnaire, a behavioral task and a physiological response do not become equivalent because they share a label. The review's extraction should record the actual instrument, reference source and task rather than only a metric name.

Human agreement is similarly bounded. Expert or annotator agreement can validate an evaluator against the specified judgment task [1, 2, 21]. It does not establish that the judgment is an adequate substitute for an unmeasured driver outcome. A productive synthesis should examine both the value and the transfer limits of this grounding.

### 7.3 Comparators, timing and exposure

Different controls isolate different contributions. When2Talk holds canonical content constant while comparing timing policies [5]. The ChatGPT simulator study compares generated conversation with scripted and no-agent conditions [6]. The feedback study varies how processing progress is communicated [19]. These are not interchangeable tests of a generic assistant advantage.

Exposure duration and setting also shape interpretation. A response survey, a short laboratory interaction and a closed-track session can answer useful questions, but cannot establish the same claims about long-term use. Novelty effects, adaptation, habituation and individual preference require appropriate observation rather than assumptions based on initial satisfaction. The single-session limitation reported in the passive-fatigue study is an example of a boundary that should accompany its findings [7].

### 7.4 Study families and reproducibility

InCA and the factual benchmark concern the CarExpert evaluation context [1, 2]. This creates a study-family reconciliation question, not proof of duplicate data or participants. Platform reuse, benchmark overlap and participant overlap should be checked independently before any aggregate counts are interpreted.

The public CAR-bench repository describes a synthetic environment and model/API requirements. The feedback-study supplement provides condition videos and a qualitative codebook. These are different forms of openness: a readable repository, usable benchmark, available participant data and permission to reuse that data should not be treated as one binary property. Documentation checks performed for this review did not download datasets or reproduce the experiments.

### 7.5 Transparency and human control

The ethical driver-monitoring review-to-design paper places consent, transparency and emotional well-being within its stated scope [24, abstract-only comparison here]. Such issues should be considered alongside performance, while avoiding claims that the present draft has completed their appraisal. In particular, an inferred emotional state and an explicit interaction preference should remain distinct records.

Disclosure also belongs in evaluation appraisal. Sponsor participation, participant exclusions and annotation procedures should be recorded accurately rather than used as automatic inclusion or exclusion rules. A review can identify where additional checking is needed without alleging invalidity or resolving ambiguity in the author's favor by assumption.

## 8. Research directions emerging from the evidence map

The following are proposed research questions, not established gaps or experiments conducted by this review.

### 8.1 Transfer from evaluation scores to human outcomes

A candidate empirical question is whether factuality, message-quality and preference scores predict independently measured workload or state outcomes in the same task and population. Testing this would require paired data, a justified construct definition and an appropriate comparison. The existence of expert-grounded factual and dialogue evaluation means the contribution would have to concern a specific transfer question, rather than merely adding human annotation [1, 2, 21].

### 8.2 Joint evaluation of content and timing

Content and timing can be studied separately, but an assistant ultimately combines them. A possible question concerns whether a context-sensitive timing policy changes the effect of a particular support message under a defined workload. When2Talk, ProVoice and the proactivity framework already provide relevant comparisons [3, 4, 5]. A new study must identify which interaction among variables they leave unresolved; this draft does not claim that a joint evaluation is absent from the complete literature.

### 8.3 Support requests, affect estimates and interaction preferences

Another question is how systems should distinguish an observed or inferred state from a request to act. The inspected preference and confirmation studies provide foundations [3, 5, 10, 17]. A future protocol could record explicit requests, response preferences and state estimates separately and test how policy decisions change when they disagree. Suitable labels cannot simply be inferred from an existing emotion dataset, and the current review supplies no new user-ground-truth data.

### 8.4 Evaluation under persistent use

Short-term interaction results motivate questions about sustained use, changing preferences and longitudinal burden. These require designs that can distinguish adaptation from initial novelty and record exposure rather than treating repeated utterances as independent observations. Prototype latency, deployment constraints and the role of automation should remain part of the study description [7, 19]. No longitudinal effectiveness claim can be made from the present evidence map.

### 8.5 Practical reporting for future experiments

A useful reporting record would identify the intended user role, system function, model/version, data and label provenance, response-selection policy, comparator, exposure, outcome instrument, analysis denominator and uncertainty. It should also record opt-out or confirmation behavior where relevant and distinguish model simulation from actual participant exposure. This is a proposed checklist for discussion; it is not a validated reporting standard or substitute for venue-specific requirements.

## 9. Limitations and completion requirements

The current corpus is exploratory, purposefully selected and dominated by arXiv availability. Search caps, broad-query noise and unresolved eligibility prevent conclusions about field-wide frequencies. ACM/IEEE and additional index access remain incomplete. Recent dedicated reviews may overlap with or supersede the proposed synthesis. Publication versions and venue status also require reconciliation; an arXiv identifier or conference template does not establish acceptance.

The evidence map has been extracted by one agent through targeted section inspection. Human checking, independent screening where feasible, design-specific appraisal, study-family reconciliation and endpoint-level sample verification are pending. Existing automated checks establish consistency among records, citations and counts, not the truth of scientific interpretations.

We have not pooled effects, ranked systems on a combined effectiveness score, or reproduced any cited experiment. The four-layer organization is an analytical proposal rather than a verified novel theory. Before submission, complete the planned searches and screening, verify the extracted evidence with a human reviewer, refine the nearest-review comparison and revise the abstract and conclusions around the final corpus. Unresolved denominators or unclear measurements should remain visible rather than be replaced with assumptions.

## 10. Conclusion

Generative in-vehicle assistants are evaluated through several legitimate but distinct forms of evidence. The inspected publications include factual and dialogue assessment, user-preference studies, proactive-policy comparisons, human-state measures and driving-related outcomes. Their coexistence makes a broad claim of missing human validation untenable, while their differences make a single conclusion about effectiveness premature.

The proposed review contribution is to connect each claim to its measured construct, reference source, participant role and evaluation setting. Such a map can identify what an individual result supports and what requires an additional study. Completing the broader search and human verification is essential before presenting this exploratory synthesis as a finished review.

## Declarations and author-review status

No new participant study or vehicle experiment was conducted for this manuscript. Literature metadata, targeted-section extraction and this working text were prepared with AI assistance. Human authors must verify the references, interpretations, methods description, author contributions and applicable venue policies before any submission. Funding, competing interests and author/affiliation declarations remain for the human authors to complete; no declaration is invented here. No public submission is authorized or has been made as part of this drafting work.

## References

[1] Ken E. Friedl, Abbas Goher Khan, Soumya Ranjan Sahoo, Md Rashad Al Hasan Rony, Jana Germies, Christian Süß. **InCA: Rethinking In-Car Conversational System Assessment Leveraging Large Language Models**. arXiv:2311.07469v2. https://arxiv.org/abs/2311.07469v2

[2] Rafael Giebisch, Ken E. Friedl, Lev Sorokin, Andrea Stocco. **Automated Factual Benchmarking for In-Car Conversational Systems using Large Language Models**. arXiv:2504.01248v1. https://arxiv.org/abs/2504.01248v1

[3] Huifang Du, Xuejing Feng, Jun Ma, Meng Wang, Shiyu Tao, Yijie Zhong, Yuan-Fang Li, Haofen Wang. **Towards Proactive Interactions for In-Vehicle Conversational Assistants Utilizing Large Language Models**. arXiv:2403.09135v1. https://arxiv.org/abs/2403.09135v1

[4] Josh Susak, Yifu Liu, Pascal Jansen, Mark Colley. **ProVoice: Designing Proactive Functionality for In-Vehicle Conversational Assistants using Multi-Objective Bayesian Optimization to Enhance Driver Experience**. arXiv:2601.19421v1. https://arxiv.org/abs/2601.19421v1

[5] Kaiser Hamid, Peihang Li, Nade Liang. **When2Talk: When Should a Proactive In-Car Agent Talk?**. arXiv:2609.12503v1. https://arxiv.org/abs/2609.12503v1

[6] Yeana Lee Bond, Mungyeong Choe, Baker Kasim Hasan, Arsh Siddiqui, Myounghoon Jeon. **ChatGPT on the Road: Leveraging Large Language Model-Powered In-vehicle Conversational Agents for Safer and More Enjoyable Driving Experience**. arXiv:2508.08101v1. https://arxiv.org/abs/2508.08101v1

[7] Lewis Cockram, Yueteng Yu, Jorge Pardo, Xiaomeng Li, Andry Rakotonirainy, Jonny Kuo, Sebastien Demmel, Mike Lenné, Ronald Schroeter. **Small Talk, Big Impact? LLM-based Conversational Agents to Mitigate Passive Fatigue in Conditional Automated Driving**. arXiv:2510.25421v2. https://arxiv.org/abs/2510.25421v2

[8] Chris Monk, Allegra Ayala, Christine S. P. Yu, Gregory M. Fitch, Dara Gruber. **Visual and Cognitive Demands of a Large Language Model-Powered In-vehicle Conversational Agent**. arXiv:2601.15034v1. https://arxiv.org/abs/2601.15034v1

[9] Chang Liu, Dalai Mengke, Hanbo Zhou, Jia Hu, Peter Mihajlik, Tamas Sziranyi. **Multimodal Drivers' Emotion Recognition and Safety-Oriented Intervention for Intelligent Transportation Systems**. arXiv:2608.06378v1. https://arxiv.org/abs/2608.06378v1

[10] Harine Choi, Eun Hak Lee, Zhengzhong Tu. **Vision-Language Assistant for Emotional Reactions to Risky Driving**. arXiv:2607.16181v1. https://arxiv.org/abs/2607.16181v1

[11] A. J. Bequet, C. Jallais, J. Quick, D. Ndiaye, A. R. Hidalgo-Munoz. **Road to Serenity: Individual Variations in the Efficacy of Unobtrusive Respiratory Guidance for Driving Stress Regulation**. arXiv:2406.09777v1. https://arxiv.org/abs/2406.09777v1

[12] Michael Braun, Florian Weber, Florian Alt. **Affective Automotive User Interfaces -- Reviewing the State of Emotion Regulation in the Car**. arXiv:2003.13731v2. https://arxiv.org/abs/2003.13731v2 The retrieved PDF identifies the published version in ACM Computing Surveys 54(7), Article 137 (2021), DOI: 10.1145/3460938.

[13] Anaïs Halin, Jacques G. Verly, Marc Van Droogenbroeck. **Survey and synthesis of state of the art in driver monitoring**. arXiv:2110.00472v1. https://arxiv.org/abs/2110.00472v1

[14] Yao Rong, Chao Han, Christian Hellert, Antje Loyal, Enkelejda Kasneci. **Artificial Intelligence Methods in In-Cabin Use Cases: A Survey**. arXiv:2101.02082v1. https://arxiv.org/abs/2101.02082v1

[15] Abu Jafar Md Muzahid, Xiaopeng Zhao, Zhenbo Wang. **Survey on Human-Vehicle Interactions and AI Collaboration for Optimal Decision-Making in Automated Driving**. arXiv:2412.08005v1. https://arxiv.org/abs/2412.08005v1

[16] Tima M. Yekta, Julius Schöning. **Keep Calm and Relax -- HMI for Autonomous Vehicles**. arXiv:2408.09046v1. https://arxiv.org/abs/2408.09046v1

[17] Michael Braun, Jingyi Li, Florian Weber, Bastian Pfleging, Andreas Butz, Florian Alt. **What If Your Car Would Care? Exploring Use Cases For Affective Automotive User Interfaces**. arXiv:2004.02481v1. https://arxiv.org/abs/2004.02481v1

[18] Yuanchao Li, Lachlan Urquhart, Nihan Karatas, Shun Shao, Hiroshi Ishiguro, Xun Shen. **Beyond Voice Assistants: Exploring Advantages and Risks of an In-Car Social Robot in Real Driving Scenarios**. arXiv:2402.11853v2. https://arxiv.org/abs/2402.11853v2

[19] Johannes Kirmayr, Raphael Wennmacher, Khanh Huynh, Lukas Stappen, Elisabeth André, Florian Alt. **What Are You Doing? Effects of Intermediate Feedback from Agentic LLM In-Car Assistants During Multi-Step Processing**. arXiv:2602.15569v2. https://arxiv.org/abs/2602.15569v2

[20] Keito Inoshita. **Safety-Aware Evaluation of LLM-Generated Driver Intervention Messages through Multi-Task Risk Fusion**. arXiv:2606.22706v1. https://arxiv.org/abs/2606.22706v1

[21] Vaishnav Negi, Lev Sorokin, Soroosh Tayebi Arasteh, Andrea Stocco. **Automated Evaluation of Multi-Turn Dialogues in In-Car Conversational Assistants**. arXiv:2609.35812v1. https://arxiv.org/abs/2609.35812v1

[22] Johannes Kirmayr, Lukas Stappen, Elisabeth André. **CAR-bench: Evaluating the Consistency and Limit-Awareness of LLM Agents under Real-World Uncertainty**. arXiv:2601.22027v1. https://arxiv.org/abs/2601.22027v1

[23] Diba Afroze, Xingli Zhang, Yazhou Tu, Xiali Hei. **From Intent to Action: Benchmarking LLM Safety in Vehicle Voice Command Authorization**. arXiv:2609.19630v1. https://arxiv.org/abs/2609.19630v1

[24] Bilal Khana, Waseem Shariff, Rory Coyne, Muhammad Ali Farooq, Peter Corcoran. **From Review to Design: Ethical Multimodal Driver Monitoring Systems for Risk Mitigation, Incident Response, and Accountability in Automated Vehicles**. arXiv:2605.06439v1. https://arxiv.org/abs/2605.06439v1
