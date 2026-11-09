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
Before any write, confirmed IDs are checked in the GitHub-persisted ledger.
For uncached IDs, all existing top-level Zotero items are paginated once and
matched locally using explicit arXiv identifiers (versions ignored), DOI when
available, or an exact normalized title AND author set. Distinct explicit arXiv
IDs are not merged by title. This replaces `qmode=everything` search: real-library
audit found that searching an arXiv ID returned zero despite existing entries.
The in-memory snapshot is updated after every successful creation. Existing matches are left intact; no user tags or collections
are overwritten. New items get rule-based collections and the tags 待阅读 and
自动分类待复核. Collection assignment is tentative; it is not model-generated.
Full names use Zotero's single-field creator form to avoid guessing family names.
No PDFs are downloaded or uploaded. Cross-source DOI-only matches without an
arXiv identifier are not yet deduplicated.

Selected history is reconciled against a persistent, destination-specific sync
ledger in state.json. Each confirmed created/existing item is checkpointed
immediately; future runs skip it without a Zotero query. Changing the library
starts a separate ledger. Existing items are left intact, including user deletions
after a confirmed sync (delete that ledger entry explicitly to resync it).

Requests are spaced at least one second apart. Both Backoff and Retry-After
headers are respected, including HTTP-date Retry-After values. HTTP 429 may be
retried at most twice, with an identical per-operation random write token and payload. A new operation
gets a fresh token; content hashes are not reused across runs. HTTP 412 on a
write triggers a read-only reconciliation of the item/collection. Only a
confirmed remote match counts as success; otherwise it remains pending without
blindly repeating the write.
Network errors and other HTTP errors are not automatically retried. Total sleep
per invocation is limited to 60 seconds, in chunks no longer than 30 seconds. If a
server cooldown exceeds this limit, the sync stops without shortening it; the
cooldown and confirmed progress persist for the next invocation. Persistent rate
limiting still fails the job with a safe, actionable status report and pending
count rather than pretending all papers were saved. Do not repeatedly rerun.

For a backlog-only retry, manually dispatch the workflow with `zotero_only=true`.
This restores persistent state and syncs pending papers without arXiv or OpenAI
calls. It still runs the existing tests and saves progress after failure. The
status artifact reports created/existing/cached/pending counts.
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

Pricing variables must be plain decimal numbers in USD per million tokens (no
currency symbols, commas or unit suffixes). Empty or malformed values now report
the exact variable name without echoing its contents. `LITERATURE_PRICING_CONFIRMED`
must be exactly `true`; do not confuse the $0.20 per-run budget with token prices.


## GitHub synchronized-paper list

The `literature-state` branch contains `state.json` (authoritative history and
ledger) and `zotero-sync-list.json` (a human-readable view of confirmed syncs).
The standalone list includes stable arXiv IDs, titles, paper links, confirmation
status and Zotero item keys when available. Older ledger records may have a null
item key. It contains no credentials and hashes the destination namespace rather
than displaying the account number. The standalone list is generated from the
ledger in the same Git commit, not maintained independently. Do not manually edit
only the view and expect deduplication to change.

Before writing, the restored ledger skips confirmed entries. Unconfirmed items
are compared against the actual library snapshot; a failed read never counts as
an empty library. Only confirmed created/existing entries enter the list. A lost
or first-run ledger still benefits from snapshot matching. Existing duplicates
are not deleted or merged by this workflow; review their notes/attachments and
collection/tag unions before any cleanup.
