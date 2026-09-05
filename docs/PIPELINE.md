# The seam between the census and the setup that consumes it

Two halves, in two repositories, run by two different schedulers. They have
never spoken to each other and they never will. This file is the contract
between them, and it exists because parallel workers diverge on whatever their
brief leaves to judgement — a shared contract written once converts an
expensive integration problem into a cheap authoring one.

## Who does what

**Producer — `agent-vitals`, GitHub Actions.** Two cron slots, 07:00 and 12:00
UTC; the second is a no-op on any day the first worked, because a daily
obligation carried by one slot is one you learn about after it has been missed.
It writes, and commits to `main`:

| Path | Contract |
|---|---|
| `data/servers.json` | Every repository in the index. `generated_at` is the census timestamp and is the freshness signal the consumer reads. |
| `data/history.csv` | One row per run. The consumer cross-checks its own recomputation against this row and refuses to answer when they disagree. |
| `data/daily/<date>.json` | The run's own record; its existence is the guard against a duplicate run. |

Fields the consumer depends on, per repository: `full_name`, `stars`,
`license`, `license_state` (`spdx` | `none` | `non-standard`), `status`
(`active` | `slowing` | `stale` | `abandoned`), `archived`, `is_fork`,
`first_seen`, `pushed_at`, `days_since_push`, `topics`, `description`.

**Changing any of those names is a breaking change.** The consumer reads them
positionally by key and will silently return nothing rather than error.

**Consumer — `rota`, launchd.** `com.rota.daily` at 10:15 local, after both CI
slots have had their chance. It pulls this repository, filters the arrivals
through `rota/vetting.yaml`, and appends the survivors to
`rota/ledger/arrivals.md`. It notifies nobody: the Monday brief is where they
get read, so there is one place to look rather than two.

## What each side must not assume

The producer must not assume anyone is reading. The consumer must not assume
the producer ran.

That second one is the failure this seam is built against: if CI stops, nothing
downstream errors. The consumer keeps answering, and every answer is an old
census presented as current ground. So the consumer checks `generated_at` and
says so above the results when the census is more than two days old, and it
compares its own recomputed totals against `history.csv` and exits non-zero
when they disagree. A silent disagreement between two computations of one fact
is worse than either being wrong alone, because it looks like corroboration.

## What "useful" means, and where that is decided

Not here. Reach is not fit: a repository with fifty thousand stars that does a
job already covered is not a candidate. The fit test lives in
`rota/vetting.yaml` — jobs already covered with their incumbents named,
categories already declined with the reason, the domains the work actually
touches, and the hard stops. It is a file rather than code so it can be argued
with, and it is versioned so a decision can be traced to the day it changed.

The producer stays neutral. It measures the ground; it does not decide what to
stand on.

## Changing this

A change to a field name, a schedule, or an output path is a change to this
file first. The half that moves without the other reading about it is the half
that breaks the pipeline, and neither half will notice.

---

## Answers to the proposer's three questions (2026-09-04)

Written here rather than sent, because an agreement that lives in a chat is an
agreement neither side can check later.

**1. Are the filters right?** They are correct and incomplete. `registry.yaml`
holds seventeen routes; the installed surface is thirty-six skills, thirty-one
agents, sixteen MCP servers and ten plugins. A candidate absent from
`registry.yaml` may still be fully covered — `mem0ai/mem0` has 64,000 stars,
passes every filter you listed, and is redundant here.

Read `rota/vetting.yaml` instead. It carries what `registry.yaml` cannot:
ten jobs already covered with their incumbents named, four categories declined
with the reason, the domains the work touches, and the hard stops.

Two thresholds added there, both as noise floors rather than quality
judgements: **100 stars** (your tiers start at 2 and 10, which is right for
measuring the ground and far too low for proposing) and **30 days of age** (a
repository that spiked last week has not shown whether anyone maintains it; of
the repos in this census old enough to judge, 29.1% had already gone quiet).

No language filter. Language says nothing about fit here.

**2. Which gaps to search for?** The `covered` map in `vetting.yaml` is the
answer by subtraction: a gap is a job inside `domains` that is not in
`covered`. That derivation stays true as things are installed, which a list
handed over once would not.

**3. Who closes the loop?** `vetting.yaml` now has `declined_repos` —
repository, reason, date. Fifteen entries to start, every one a decision
actually taken. Check it before proposing; a name in it is answered, and the
answer is the record.

Not a separate `declined.txt`: a second file holding the same kind of
judgement drifts from the first, and then neither is authoritative. One file,
versioned, so a decision can be traced to the day it changed.

**What stays yours.** The census, the schema, the schedule, and neutrality
about what any of it means. The producer measures the ground; it does not
decide what to stand on. If a filter here ever looks wrong, change this file
before changing either side's code.
