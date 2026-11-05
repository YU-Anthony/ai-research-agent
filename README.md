# AI Research Agent MVP

Python 3.11+ / LangGraph / SQLite. Focus: machine learning, multimodal reasoning and autonomous driving. The default workflow retrieves **10 real arXiv records**, reasons over their abstracts, writes a gap report and exactly three hypotheses, then durably interrupts for human review.

## Setup

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
pytest -q
python examples/approval_demo.py
```

Set `OPENAI_API_KEY` through your environment or secret manager, never in source control. `RESEARCH_MODEL` defaults to `gpt-4.1-mini`; budgeted reasoning currently rejects other models. Live calls need HTTPS access to `export.arxiv.org` and `api.openai.com`. The offline demo uses clearly labeled synthetic fixtures; these are not research evidence. PyTorch is intentionally not installed: the generated scaffold is never imported or executed by the agent.

## Example live workflow

```bash
research-agent start driving --topic 'all:multimodal AND all:autonomous AND all:driving' --allow-paid-reasoning --max-calls 2
research-agent status driving
# Read runs/driving/research-gap.md before deciding:
research-agent decide driving revise --feedback 'Focus on missing LiDAR robustness' --allow-paid-reasoning
research-agent decide driving approve
research-agent draft driving
```

Alternatively `research-agent decide driving reject` ends the workflow. Decisions, feedback, timestamps and model-call reservations are saved in `runs/driving/state.sqlite`. Resume works across processes. Approval authorizes **planning only**: it produces an experiment plan and starter PyTorch code, never executes training. There is no experiment runner, GPU scheduler, paid-service provisioner or submission command. Actual experiment execution requires a separate reviewed implementation and explicit approval of dataset, code and compute budget.

A run permits one model call by default, up to five explicitly configured. The initial live run used exactly one call. Each call checks a conservative UTF-8 byte-based token estimate against a $0.10 request cap, using assumed input/output rates of $0.40/$1.60 per million tokens; this is not a billing guarantee or an aggregate cap across revisions. Revisions consume the same run budget, and require another paid-reasoning flag. Each call reserves budget durably before contacting OpenAI, disables SDK retries, limits input to 60,000 characters and output to 3,200 tokens (library configurable up to 4,000). This bounds calls and tokens, not dollar spend: check current model pricing and use provider spending limits. Failed calls consume their reservation; failed CLI runs should be inspected, not blindly retried as new runs. Do not run concurrent writers on a single run.

## Evidence and output contract

- `papers.json` retains retrieved metadata including source and retrieval time; the live path never uses fixtures.
- `research-gap.md` includes titles, authors, dates, abstract text and canonical URLs assembled from arXiv records. Model evidence IDs must belong to those records. This prevents invented bibliography entries; it does not prove that every model claim follows from an abstract. Humans must check entailment, full papers, novelty and dataset licensing.
- Hypotheses distinguish speculation and provide datasets, baselines, metrics and falsifiable tests. Recommendations are unverified until reviewed.
- Approved plans include a coarse, explicitly provisional compute estimate and `starter.py`. The scaffold is feature fusion only, not a completed experimental implementation.
- `analysis.json` stores validated hypotheses, per-hypothesis provisional compute estimates and actual API token usage. `paper.md` and `paper.tex` are proposal drafts based on the persisted report and retrieved references. Results remain explicitly empty. **Actual result ingestion is not implemented in this MVP**, so the writer cannot assert experimental findings. LaTeX generation is supported; compilation requires an optional external TeX installation.
- Reports and state may contain sensitive research topics; keep `runs/` private. Paper abstracts are untrusted model inputs. Do not run generated code without inspecting it.

## Optional aiXiv module

`research_agent.aixiv.AiXivClient` reads only `AIXIV_TOKEN` from the environment and never logs it. Submission and discussion methods require explicit approval and then **fail closed**. The official API routes, authentication and payloads could not be verified in this environment; no speculative endpoint has been implemented. This adapter is an extension boundary, not a functioning integration. Verify official documentation before enabling any read/write transport, and retain explicit per-action human approval. No aiXiv requests or submissions are made by this MVP.

## Project layout

`src/research_agent/`: arXiv discovery, bounded OpenAI reasoning, durable workflow, artifact writer, optional aiXiv boundary, CLI. `tests/`: isolated metadata, reference validation, SQLite restart, approval/reject/revise and safety checks. `examples/approval_demo.py`: offline interrupt/resume demonstration.

## First live research workflow

The first real run is in `reports/multimodal-driving-first/`. It contains ten distinct-title arXiv records, three gaps and hypotheses, provisional compute estimates, token usage and a Markdown report. Discovery requests up to 20 candidates and retains ten distinct titles to avoid duplicate bibliographic records. No full-text review or experiment has been performed.

```bash
research-agent --runs reports status multimodal-driving-first
python examples/verify_run.py reports/multimodal-driving-first
# Only after reviewing reports/multimodal-driving-first/research-gap.md:
research-agent --runs reports decide multimodal-driving-first approve
```

The live run is still paused; the verification script only reopens and checks persisted state. `approve` generates planning artifacts only. It does not authorize or launch GPU work. A revise decision needs unused model-call budget; this first run deliberately reserves only one call. Start a separately budgeted revision run if needed.

To reproduce with a fresh run ID (one paid API call, no experiments):

```bash
research-agent --runs reports start driving-new --topic 'all:"autonomous driving" AND (all:"multimodal" OR all:"vision-language") AND all:"reasoning"' --allow-paid-reasoning --max-calls 1
```

The first analysis used 4,381 input tokens and 1,059 output tokens (estimated $0.003447 at the documented assumed rates). Billing is determined by OpenAI. The human review must verify that evidence supports each claim; abstract-only statements about missing comparisons are tentative, not established gaps. Model-suggested paid baselines need separate authorization. Compute estimates are model speculation and may be inaccurate; no GPU resources have been allocated.

Live API authentication and connectivity were verified in this cloud session. Credentials are provided by the cloud secret proxy; never copy them into files. aiXiv is unused in this workflow. Its official documentation is at https://aixiv.science/api-docs; a public GET succeeds, but no documented read-only Agent Token authentication check was found. The optional adapter remains disabled. Saved environment configuration and publication are separate from current-instance validation.

## Scheduled literature monitoring

The existing agent is reused by `python -m research_agent.monitor` (installed console entry point: `literature-monitor`). It searches arXiv's official Atom API for recent multimodal autonomous driving, driving behavior understanding and explainable driving reasoning papers. The newest 60 results in the lookback window are considered, with up to 30 unseen records sent to one OpenAI ranking request; 5–10 are selected. If fewer than five new records exist, all are summarized and the shortfall is reported. No model call is made when nothing is new. This is a bounded monitor, not an exhaustive systematic review. OpenAlex enrichment is optional and is not implemented.

Stable arXiv IDs with version suffixes removed prevent repeat digests across runs. Only summarized papers are marked seen. Updated versions of already summarized papers are intentionally skipped. Reports include official arXiv links, authors, dates, reported contributions, tentative limitations/research gaps and token/cost accounting; abstract metadata is retained as evidence. No experiments, aiXiv calls or automatic scientific claims are produced.

### Manual execution

Securely provide `OPENAI_API_KEY` in the environment. Confirm the current price ceilings for the pinned `gpt-4.1-mini-2025-04-14` model before running. Example conservative ceilings, to verify against current pricing: $1 input / $4 output per million tokens.

```bash
export LITERATURE_PRICING_CONFIRMED=true
export LITERATURE_INPUT_USD_PER_M=1
export LITERATURE_OUTPUT_USD_PER_M=4
python -m research_agent.monitor --days 7 --budget-usd 0.20
```

The default state is `monitor-state/state.json`; report output is `reports/weekly/`. Both are ignored by Git. Use `--state`, `--output`, and `--run-id` to isolate runs. One writer per state file is required. Corrupt state causes a failure rather than a reset.

The model is pinned, endpoint fixed to api.openai.com, redirects disabled, retries disabled, and output limited to 6,500 tokens. A conservative input-token bound uses UTF-8 bytes plus a 4,096-token framing margin. The request stops **before calling** if its calculated ceiling exceeds the configured budget (maximum $0.20), or if price confirmation/rates/credentials are missing. A reservation is persisted before calling; a repeated run ID cannot reserve another request. Provider billing cannot be independently guaranteed: these controls depend on accurate operator-confirmed price ceilings. If pricing is uncertain, leave confirmation unset and the paid step fails closed. Set provider spending limits separately. Each new manual invocation has its own budget; do not launch repeated invocations as an automatic retry policy.

Per the latest supplied research vision, monitoring runs Mondays at 09:00 America/New_York. The seven-day lookback is retained to catch indexing delays; persistent IDs prevent repeat summaries. The per-run estimated cap remains $0.20 (up to $1.00 over five weekly runs); runs without new papers make no model call.

### GitHub Actions settings

After merging `.github/workflows/literature-monitor.yml` into the default branch:

1. Enable GitHub Actions and permit the checkout, setup-python and upload-artifact actions.
2. Add repository Actions Secret **OPENAI_API_KEY**. The Codex cloud network secret does not automatically configure GitHub Actions Secrets. Never paste a key into a workflow, issue or command log.
3. Set repository Actions Variables `LITERATURE_PRICING_CONFIRMED=true`, `LITERATURE_INPUT_USD_PER_M`, and `LITERATURE_OUTPUT_USD_PER_M` only after checking current prices.
4. Permit the workflow's `contents: write` permission and bot pushes to the dedicated `literature-state` branch. Main-branch protection can remain enabled. State is stored as a JSON-only Git commit on that branch; no generated state is committed to main.
5. Run **Actions → Weekly research monitor → Run workflow**. Inputs accept 1–90 lookback days and a budget no greater than $0.20.

Schedules use both 13:00 and 14:00 UTC on Mondays; a New York timezone gate selects 09:00 across EST/EDT. The other occurrence skips the monitor job. GitHub schedules run only from the default branch and are best effort: delays past the gate's 09:00 local hour can skip that week's run. Use manual dispatch if necessary. GitHub can disable schedules in inactive public repositories after 60 days.

A repository-wide concurrency group serializes scheduled/manual runs without canceling an active run. The JSON state branch is fetched before work, then updated with a normal non-force push even after ordinary model/report failure. Remote-read failures never silently reset state. State includes seen IDs, run reservations, abstract metadata and complete analysis history, but no credentials or full-paper texts. The local SQLite library is rebuilt from this portable state and included in Actions artifacts. Deleting the state branch resets cross-run deduplication. Hard runner loss before the save step can lose its latest reservation; avoid retrying an uncertain charged run without reviewing OpenAI usage. A rerun with a preserved reservation stops instead of charging again.

Every attempted monitor job uploads `reports/weekly/` and available state as an Actions artifact for 90 days, including machine-readable `status.json` on CLI failure. The job fails on API, validation, budget or state-persistence failures, and GitHub's failure notifications/job summary provide the alert. Early dependency/state-restore failures may occur before report files exist; inspect job logs. Provider response bodies and exception text are deliberately excluded from error reports because they can echo credentials. Public reports are model analyses, not verified full-text conclusions.

Validation commands: `python -m pytest -q`. The monitor tests cover version-independent deduplication, repeated runs with zero calls, fewer-than-five results, unknown/duplicate model references, corrupted state, fail-closed budget checks and safe error reporting. Existing research-agent tests remain intact.

Manual validation evidence is committed under `reports/weekly-monitor-validation/`: the final 30-day run considered 20 unseen records and produced five distinct summaries using one model request. Its conservative preflight ceiling was $0.059912; measured token usage was 9,412 input / 789 output (estimated $0.012568 at the conservative $1/$4 ceilings). An offline replay of those real paper IDs produced zero candidates and zero model calls. 27 tests passed, including DST dates and an actual local bare-Git state-branch roundtrip. Earlier live tests produced 3- and 10-paper digests; subsequent duplicate model responses were safely rejected. The final implementation removes duplicate selections and still requires at least five distinct summaries when enough candidates exist. Usage is now retained before validation. This is local/manual validation, not a completed GitHub-hosted Actions run. A cloud GitHub API policy denial currently prevents PR creation and remote dispatch; allow api.github.com in the active Codex environment. Dispatch also requires the workflow to exist on the default branch first.


## Research-profile milestone

The supplied vision is preserved in [docs/research-vision.md](docs/research-vision.md); the updated broad research interests are in [docs/research-interests.md](docs/research-interests.md). Evidence-grounded experiment opportunities are in [reports/research-opportunities/experiment-ideas.md](reports/research-opportunities/experiment-ideas.md), with verified arXiv metadata. These are untested ideas, not claims of novelty.

The monitor now asks the same single bounded model request for cross-paper trends/comparisons and two or three ranked, falsifiable research proposals. Each includes evidence IDs, method, datasets, baselines, metrics, provisional compute, risks and a novelty-check plan. References must match retrieved candidates, and every synthesis reference is rendered with its verified arXiv link. Supporting candidate abstracts may be cited even if not among the five-to-ten ranked summaries. Novelty/priority are heuristic and require human/full-text review.

Portable JSON state retains discovered metadata (including on paid-analysis failure), successful digests and proposals. SQLite tables `papers` and `research_runs` provide a local searchable projection:

```bash
python -m research_agent.library "reasoning" --state monitor-state/state.json
```

The console entry point is `research-library`. Search is offline and incurs no model cost. Restore the state branch first when moving to a new machine. Existing version-1 deduplication state is migrated additively; earlier metadata that was never saved cannot be recovered automatically.

ArXiv-only discovery is implemented. OpenAlex/Semantic Scholar adapters, citation-based trend statistics, full-text novelty verification, notification integrations, approved experiment execution, actual result ingestion and aiXiv publication are deferred. No notification channel is configured. Existing LangGraph experiment-planning approval remains available through the original research-agent CLI; monitor proposals are pending human review and do not invoke an experiment runner.

## Narrow CPU experiment framework (not yet run on real data)

[Temporal-consistency protocol](docs/experiments/temporal-consistency-protocol.md) defines one pedestrian crossing-action experiment. Driver behavior/intention, VLM explanation and emotion-recognition tasks are excluded from this pilot. The framework includes a validated JSONL window interface, last-frame/temporal Logistic Regression, validation-only calibration/thresholds, temporal-consistency abstention, recording-group bootstrap, and explicit per-run CPU approval with hashes and a hard launcher timeout. Optional dependencies: `pip install -e '.[dev,experiments]'`. Run `pytest -q` with these extras to exercise the synthetic software smoke tests; these tests are skipped if optional numerical dependencies are absent. No experiment runs from GitHub literature monitoring. Real PIE access, licensing, label alignment and the data converter remain outstanding; synthetic fixtures are not experimental findings. A real CPU run needs a separately reviewed dataset/config and `--approve-cpu-run`.

### Daily literature monitoring with Zotero

The monitor now schedules daily at 09:00 America/New_York (best-effort GitHub
execution), with optional manual dispatch. Ranked papers are deduplicated and
saved to Zotero with tentative collections and tags. Configure GitHub Actions
secrets/variables separately from cloud credentials; see [setup and failure
handling](docs/daily-zotero.md). Reports are Actions artifacts under reports/daily.
