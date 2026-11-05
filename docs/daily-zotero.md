# Daily monitoring and Zotero

The GitHub Actions monitor runs every day at nominal 09:00 America/New_York.
Two UTC schedules cover daylight saving; the gate checks the triggering cron,
not the actual execution hour, so ordinary GitHub queue delays do not skip work.
GitHub schedules are best effort and cannot guarantee exact arrival time.
Manual workflow_dispatch always runs. A seven-day overlapping search window
catches delayed arXiv indexing; stable IDs deduplicate papers across runs.

## GitHub repository configuration

Settings → Secrets and variables → Actions:

- Secrets: `OPENAI_API_KEY`, `ZOTERO_API_KEY` (Zotero library write access).
- Variables: `ZOTERO_LIBRARY_ID` (numeric), `ZOTERO_LIBRARY_TYPE` (`user` or `group`).
- Variables: `LITERATURE_PRICING_CONFIRMED=true`, `LITERATURE_INPUT_USD_PER_M`,
  `LITERATURE_OUTPUT_USD_PER_M`: operator-confirmed current model price ceilings.
- Enable Actions. The workflow needs contents:write to persist its state branch.

Cloud-environment secrets are separate from GitHub Actions secrets. Never paste
keys into the repository, reports, issues or chat. The code does not transfer them.
The estimated model-call ceiling must remain within the configured budget, at
most $0.20/run; it fails before calling when pricing is absent or too expensive.

## Zotero behavior

The sync reads selected papers from persistent history, not every discovered paper.
Each paper is checked against Zotero using the arXiv base identifier (versions
are not duplicated). Existing matches are left intact; no user tags or collections
are overwritten. New items get rule-based collections and the tags 待阅读 and
自动分类待复核. Collection assignment is tentative; it is not model-generated.
Full names use Zotero's single-field creator form to avoid guessing family names.
No PDFs are downloaded or uploaded. Cross-source DOI-only matches without an
arXiv identifier are not yet deduplicated.

History is replayed on subsequent successful monitoring runs, so a Zotero failure
does not lose papers already marked seen by the literature monitor. Deterministic
write tokens guard immediate replays. Writes have no automatic HTTP retries.
The shared Actions concurrency group serializes runs. External concurrent writers
and delayed search indexing can still affect cross-client duplicate detection.

Run locally after securely configuring the environment:

```sh
python -m research_agent.zotero --state monitor-state/state.json \
  --output reports/daily/zotero-status.json
```

Artifacts contain digest files, Zotero status and monitoring state. Sync errors
fail the job and record a safe error, while monitoring state is still saved.
Workflow changes must be merged into the default branch before schedules change.
For a manual verification use Actions → Daily research monitor → Run workflow;
check the Generate digest and Sync selected literature to Zotero steps, not just
the green clock job. Neither experiments nor aiXiv publication is part of this flow.
