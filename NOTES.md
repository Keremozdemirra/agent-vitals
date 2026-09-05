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

