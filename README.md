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
