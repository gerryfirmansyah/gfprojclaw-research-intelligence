# J3 Profile / Project Selector Binding v0

Status: **IMPLEMENTATION TARGET**

J3 now has production-backed reference Profiles and Projects. The remaining J3 exit artifact is the HUMAN-visible selector binding.

Target behavior:

- Profile selector reads canonical `research_profile` rows and their current versions.
- Project selector reads canonical `research_project` rows beneath the selected Profile and their current versions.
- Selection changes Cockpit context only; it does not create scientific evidence or HUMAN decisions.
- Profile A and Profile B use the same read path with no domain-specific core branch.
- Static prototype labels may remain illustrative elsewhere, but selector identity must come from canonical production data.

Acceptance path:

`PostgreSQL canonical state → generic read path → Profile selector → Project selector → Cockpit context`

J3 exits when this path is implemented and verified for both reference Profiles.
