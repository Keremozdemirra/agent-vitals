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
