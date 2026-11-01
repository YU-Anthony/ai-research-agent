# Generative in-vehicle support assistants: pilot evidence map

**Status: first review milestone, not a completed systematic review and not submission-ready.** No new participants, experiments, paid model calls or public submissions were involved.

Working title: **What Counts as Evidence? Evaluating Generative In-Vehicle Assistants for Driver Support: A Scoping Review and Evidence Map.**

The initially suggested broad "emotion recognition to intervention" angle overlaps substantially with Braun, Weber and Alt's affective-automotive review (arXiv first posted 2020; the retrieved PDF identifies an ACM Computing Surveys publication in 2021, DOI 10.1145/3460938). That review already covers emotion regulation evaluations and methodological considerations. This pilot therefore investigates a narrower, provisional angle: evidence and evaluation practices for generative/conversational driver-support systems, using selected older systems as comparators. Novelty is not established until broader database searches and nearest-review checks are completed.

## Delivered

- `protocol.md`: proposed scope, research questions, eligibility and remaining search plan.
- `search-log.json`: exact three pilot queries, relevance caps, retrieval times and all returned metadata.
- `records.json`, `screening.csv`: versioned references and provisional screening decisions with reasons.
- `review-seeds.json`, `review-overlap.md`: four nearest review comparators and overlap assessment.
- `evidence-map.csv`, `codebook.md`: eight targeted-full-text original-study records on independent evidence axes (five generative core studies and three non-generative comparators).
- `fulltext-access.json`, `fulltext-fingerprints.json`: retrieval evidence and PDF SHA-256 hashes. PDFs are not redistributed in this repository.
- `draft.md`: an evidence-limited manuscript skeleton with preliminary synthesis, not publication-ready results.
- `follow-up-seeds.csv`: backward-citation leads not yet retrieved or verified as primary evidence.
- `source-access.json`, `audit.json`: observed access failures and auditable pilot counts.
- `validate.py`: checks cross-file referential integrity and counts without API calls.

The three searches returned 60 records, or 57 unique arXiv IDs after removing version suffixes. Four review seeds add three new IDs, making 60 records in the combined ledger. Eight studies were purposefully selected for initial coding, 12 records remain pending full-text eligibility checks, three are adjacent context/dataset/project records, four are review comparators, and 33 are excluded **from this pilot** after title/abstract screening. These are not final PRISMA inclusion/exclusion counts, nor a field-wide prevalence estimate. Thirteen PDFs were retrieved and inspected in targeted sections; this is not independent dual-reviewer full-text assessment.

## What can currently be said

The pilot contains genuinely different evidence types: synthetic-pair/offline intervention evaluation; simulator driving outcomes; closed-track fatigue outcomes; and on-road workload/experience studies. These endpoint types should not be collapsed into a single claim that an assistant "helps drivers". Conversely, the pilot already includes human outcome studies, so it does not support a blanket claim that the field has no intervention evidence.

Extraction found a reporting discrepancy worth human checking: Road to Serenity's abstract says 85 participants, while Methods describes 88 recruited, five excluded and a final sample of 83. Endpoint-specific denominators still require verification. We retain the discrepancy rather than choose a convenient N. Another study reports sponsor involvement in study conceptualization and the decision to submit; this is a disclosure to record, not automatic grounds for exclusion.

## Remaining blockers and next decisions

ACM, IEEE, Crossref, OpenAlex and Semantic Scholar requests currently fail with ProxyError under the active cloud policy. Required destinations were saved in the environment draft but are not active yet. Review/apply the network settings (and publish if requested by the UI), then retest access. Publisher access and API credentials/rate limits may be separate prerequisites; network access does not guarantee full-text rights. No credentials should be entered in chat.

The pilot is strongly arXiv-biased and omits important HCI/human-factors literature. Human verification of screening and extracted fields, citation chaining, study-family deduplication, complete retrieval logs, and review-specific quality appraisal are pending. The protocol was written after exploratory pilot searches and is **not preregistered**. No effect-size pooling, proof of novelty, publication guarantee or verified aiXiv upload permission is claimed.

aiXiv publication requires review of the final manuscript and explicit per-submission authorization. AIXIV_TOKEN configuration and public endpoint connectivity do not prove submission permissions. No aiXiv write request has been sent.
