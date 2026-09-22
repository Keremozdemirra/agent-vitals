# Notes

One dated entry per day, written after the census has run. Facts only: what
moved, and what that does or does not let you conclude. Where an entry names a
repository, the claim is always about a date or a licence field, never about
the quality or safety of anyone's work.

---

## 2026-09-05

The scheduled 07:00 UTC run for today had not appeared in Actions history as
of 07:44 UTC, so the latest available snapshot is still 2026-09-04. The
`daily.yml` schedule trigger was only added to the workflow on 2026-09-04
14:21 CEST; today would be its first scheduled firing, and a first firing can
land later than the cron time. The only two runs on record (12:21 and 12:46
UTC, 2026-09-04) were both manual `workflow_dispatch`, not `schedule`.

The 2026-09-04 snapshot itself is the first census taken after the project's
scope was widened from MCP servers only to the broader agent-tooling
ecosystem (MCP servers, agent frameworks, skills) — total repositories went
from 16,106 to 36,593, and `churn.arrived_count` for that run is 20,487, more
than half the index. That is the widened query set producing first sightings,
not the ecosystem growing 56% in a day. Note that `churn.scope_changed` on
that snapshot reads `false`: the field compares the current query groups
against `groups` stored in the prior run's `servers.json`, and the
pre-widening `servers.json` predates the `GROUPS`/`scope_changed` schema
entirely, so there was nothing to compare against and the flag defaulted to
false. That is a one-time artifact of the schema transition, not a live bug —
now that `servers.json` carries the new schema, a future rescoping would be
detected correctly. Of the 36,593 repositories, 16.7% carry no licence file
and 7.8% (2,846) carry a licence GitHub cannot identify as a standard SPDX
identifier; 29.1% of repositories old enough to qualify (created 365+ days
ago) are abandoned.


---

## 2026-09-08

No census ran today. The last scheduled run was 2026-09-07 17:32 UTC and
neither the 07:00 nor the 12:00 UTC slot fired this morning, so the newest
snapshot is still 2026-09-07; a `workflow_dispatch` run was triggered
manually at 07:55 UTC to fill the gap. Against 2026-09-06, the 2026-09-07
census added 372 repositories (36,908 to 37,280) on 407 arrivals and 35
departures, with `churn.scope_changed` false — this is growth in the index,
not a change in what is measured. The share carrying no licence file moved
for the first time in the recorded window, from 16.7% to 17.1% (6,176 to
6,389): 213 of the day's 372 net additions had no licence file, so more than
half of yesterday's growth was repositories under default exclusive
copyright. Abandonment among repositories old enough to qualify held at
29.1% for the fourth consecutive day.

`collect.py` fixed: `newly_archived` did not require a repository to have
been in the previous index, so a repository first seen already archived was
reported as having been archived that day. On 2026-09-05 that mislabelled 2
of the 4 entries, and on 2026-09-04 at least 2 of 100. `newly_abandoned`
was already correct — a missing prior status reads as `None` — but
`archived` is a boolean whose `.get` default is indistinguishable from a
real `False`, so the membership test had to be explicit. Past snapshots are
not rewritten; the field is correct from the next run onward.

---

## 2026-09-09

No census had run by 08:51 UTC. The last snapshot is 2026-09-08, written by
yesterday's manually dispatched run; the 07:00 UTC slot failed to fire for the
second consecutive day, and a `workflow_dispatch` run was triggered at 08:51
UTC to fill today's gap. Against 2026-09-07, the 2026-09-08 census added 98
repositories net (37,280 to 37,378) on 123 arrivals and 25 departures, with
`churn.scope_changed` false — the smallest daily net addition in the five days
recorded so far, after +372 the day before. The share carrying no licence file
held at 17.1% (6,389 to 6,395): 6 of the day's 98 net additions had no licence
file, against 213 of 372 on 2026-09-07, so the step from 16.7% to 17.1%
recorded yesterday did not continue. Abandonment among repositories old enough
to qualify moved to 29.0% from 29.1%, its first movement in the recorded
window; 6 repositories crossed into `abandoned` and 3 were newly archived.

The dispatched run completed at 09:54 UTC and wrote `data/daily/2026-09-09.json`
with an empty `errors` list. Against 2026-09-08 it added 190 repositories net
(37,378 to 37,568) on 223 arrivals and 33 departures, `churn.scope_changed`
false. The share carrying no licence file held at 17.1% for the third
consecutive day (6,395 to 6,412), and abandonment among repositories old enough
to qualify held at 29.0% for the second. 14 repositories crossed into
`abandoned`, against 6 the day before, and 3 were newly archived.

---

## 2026-09-10

No snapshot existed at 08:05 UTC and a `workflow_dispatch` run was triggered
then; it is still collecting at the time of writing. The 2026-09-08 and
2026-09-09 entries above record that the 07:00 UTC slot "failed to fire", and
the run history contradicts that: every day since 2026-09-05 has produced
exactly two scheduled runs, and both arrive hours after their nominal slot.
The first run of each day started at 11:09, 11:32, 13:19, 12:00 and 12:11 UTC
on 09-05 through 09-09, against a `0 7 * * *` cron, and the second at 14:50,
15:10, 17:32, 16:17 and 16:12 against `0 12 * * *`. The 2026-09-06 and
2026-09-07 snapshots were written by those delayed scheduled runs
(`generated_at` 12:29 and 14:19 UTC), so the schedule does deliver the census
unassisted; on the other three days a manual dispatch at around 08:00 UTC got
there first and the guard step turned the delayed run into a no-op. The
mechanism is delay of four to six hours, not a dropped slot, which matches
GitHub's documented behaviour for schedules on the hour under load.

---

## 2026-09-11

No snapshot existed at 11:11 UTC and no scheduled run had started (the last
run of any kind was the 16:04 UTC no-op on 2026-09-10), so a
`workflow_dispatch` was triggered at 11:12 UTC; it is collecting at the time
of writing. This is a longer delay than the four-to-six-hour range recorded
yesterday, which makes 2026-09-11 the first day since 2026-09-05 with no
scheduled run by late morning UTC.

The 2026-09-10 snapshot (the newest available) is `complete` with an empty
`errors` list: 37,750 repositories, up 182 net on 219 arrivals and 37
departures, `churn.scope_changed` false. The share with no licence file
slipped from 17.1% to 17.0% (6,412 to 6,423 on a larger base) after three
days flat; abandonment among eligible repositories held at 29.1%. 13
repositories crossed into `abandoned` and 5 were newly archived. 11 of the 37
departures are matched by an arrival with the same repository name under a
different owner (for example `theagenticguy/erpaval` to
`laithalsaadoon/erpaval`, `kpavlov/tachyon` to `tachyonmcp/tachyon`): those
are renames or transfers, not exits, so real turnover that day was closer to
26 out and 208 in.

## 2026-09-12

No snapshot existed at 07:01 UTC and no run of any kind had started, so a
`workflow_dispatch` was triggered; it is collecting at the time of writing.
The 07:00 slot has not fired on time on any day since 2026-09-08.

Yesterday's 12:03 UTC scheduled run failed, and the failure is a defect in
the workflow rather than in the collector. The run was created at 12:03
while the 11:11 dispatch was still collecting, waited in the concurrency
group, and started at 12:17:13, seven seconds after the dispatch had pushed
the day's census. `actions/checkout` defaults to the commit the run was
created for, so the guard step inspected a tree from before that push,
found no snapshot, collected for an hour, and lost the result to a rebase
conflict on six files. Checkout now pins `ref: main`, so a queued run reads
the branch as it is when the run starts. The dispatch's snapshot is the one
in the dataset; nothing was lost.

The 2026-09-11 snapshot is `complete` with an empty `errors` list: 37,950
repositories, up 200 net on 242 arrivals and 42 departures,
`churn.scope_changed` false. Both figures are the highest since the
2026-09-07 scope-driven spike; the 7-day mean is 236 in and 34 out. The
share with no licence file held at 17.0% (6,454), abandonment among
eligible repositories at 29.1%. 12 repositories crossed into `abandoned`
and 5 were newly archived. 8 of the 42 departures reappear as an arrival
with the same repository name under a different owner, so real turnover was
closer to 34 out and 234 in.

## 2026-09-14

No snapshot existed at 07:16 UTC and no run had started, so a
`workflow_dispatch` was triggered; it is collecting at the time of writing.
The 07:00 slot did not fire on 2026-09-13 either: that day's census came
from the 12:00 slot (run started 12:34 UTC, snapshot generated 13:37). The
07:00 slot has not fired on time on any day since 2026-09-08.

The 2026-09-13 snapshot is `complete` with an empty `errors` list: 38,259
repositories, up 192 net on 230 arrivals and 38 departures,
`churn.scope_changed` false. Both figures sit on the 7-day mean of 228 in
and 35 out. The share with no licence file held at 17.0% (6,502),
abandonment among eligible repositories at 29.0%. 9 repositories crossed
into `abandoned` and 9 were newly archived, five of the latter under one
owner. 8 of the 38 departures reappear as an arrival with the same
repository name under a different owner or casing, so real turnover was
closer to 30 out and 222 in.

Total stars rose 118,138 to 18,792,783, the largest one-day rise in the
series against a 7-day mean of about 64,000. Two arrivals explain most of
it: `reactive-resume/reactive-resume` (42,666 stars, MIT, created
2020-03-25), which is the departed `reactive-resume/app` under a new name,
and `drawdb-io/drawdb` (39,507 stars, AGPL-3.0, created 2023-07-16), which
is new to the index. Neither is a new project; the star total moved because
the scope's topic queries picked them up, not because the ecosystem grew.

Addendum, 08:16 UTC: the dispatch finished and the 2026-09-14 snapshot
is `complete` with an empty `errors` list: 38,414 repositories, up 155
net on 175 arrivals and 20 departures, `churn.scope_changed` false. Both
are below the 7-day mean of 224 in and 34 out; 20 out is the lowest
since 2026-09-08. The share with no licence file held at 17.0% (6,538),
abandonment among eligible repositories at 29.1%. 9 repositories crossed
into `abandoned`, none were newly archived. Total stars rose 43,021, back
on the ordinary daily rate after yesterday's two-repository jump.

## 2026-09-21

No snapshot existed at 07:02 UTC and no run had started, so a
`workflow_dispatch` was triggered; it is collecting at the time of writing.
The 07:00 slot has still not fired on any day: every census from 2026-09-15
to 2026-09-20 came from the 12:00 slot, starting between 11:49 and 12:28
UTC, and the second scheduled run of each day landed at 15:37 to 16:33 UTC
and exited on the guard. No note was written for 2026-09-15 through
2026-09-20; those six snapshots exist and are `complete` with empty
`errors` lists.

The 2026-09-20 snapshot is `complete` with an empty `errors` list: 39,418
repositories, up 161 net on 191 arrivals and 30 departures,
`churn.scope_changed` false. Both figures are below the 7-day mean of 213
in and 43 out. The share with no licence file fell to 16.8% (6,637), the
first reading below 16.9% in the series; abandonment among eligible
repositories held at 29.2%. 8 repositories crossed into `abandoned` and 4
were newly archived, three of the latter under one owner. 11 of the 30
departures reappear as an arrival with the same repository name under a
different owner or casing. Total stars rose 64,664 to 19,264,153; the
largest arrival is `tonhowtf/omniget` (13,988 stars, GPL-3.0, created
2026-02-11), which is new to the index rather than new to GitHub.

## 2026-09-22

No snapshot existed at 07:56 UTC and no run had started: the new 03:23
slot (moved off the top of the hour in 078fbb3 on 2026-09-21) did not fire
on its first day, so a `workflow_dispatch` was triggered at 07:56 UTC and
is collecting at the time of writing. Yesterday's dispatch at 07:02 UTC
failed at 08:05 UTC in the push step: the push was rejected because
096744e and 078fbb3 had landed on `main` during collection, and the retry
rebase stopped on a content conflict in `docs/index.html`, a rendered
file that both sides had changed. The day was saved by the scheduled run
created at 15:56 UTC, which found no snapshot and collected. The push
retry rebases but cannot resolve a conflict in rendered output; re-running
`render.py` after the rebase stops would. Not changed here.

The 2026-09-21 snapshot is `complete` with an empty `errors` list: 39,627
repositories, up 209 net on 251 arrivals and 42 departures,
`churn.scope_changed` false. Arrivals are the highest since 2026-09-15
(289) and above the 7-day mean of 218; departures sit close to the 7-day mean
of 45. The share with no licence file held at 16.8% (6,643), licences GitHub
cannot identify at 7.8% (3,081), abandonment among eligible repositories
at 29.2%. 7 repositories crossed into `abandoned` and 2 were newly
archived. 6 of the 42 departures reappear as an arrival with the same
repository name under a different owner or casing. Total stars rose 78,291
to 19,342,444; the largest arrival is `TykTechnologies/tyk` (10,826 stars,
created 2014-05-07, `license_state` non-standard), new to the index rather
than new to GitHub, followed by `bostrot/wslmanager` (4,005, non-standard)
and `miqdadbadjuber/anti-slop` (3,438, MIT, created 2026-08-07).
