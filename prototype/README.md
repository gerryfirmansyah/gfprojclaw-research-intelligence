# GFPROJCLAW Research Cockpit Prototype

This folder contains a static interactive UI prototype derived from the accepted J1 UX specifications.

## Purpose

The prototype is not production code and does not define the J2 object model or database schema. It exists so the HUMAN researcher can visualize the intended end-state experience before implementation.

The current prototype includes dummy data for:

- Today / What Changed?
- Research Journey R0–R16
- Research Opportunities / Gap–Solution reasoning
- Evidence Explorer
- Knowledge Evolution
- Human Review
- Coverage & Health
- Research Profiles / Projects
- Telegram Research Radar

It also supports switching between the two reference profiles to demonstrate that the same cockpit structure can be reused across domains.

## Run locally

Open `index.html` directly in a browser, or serve this folder with any simple static HTTP server.

No build step and no external dependency are required.

## J1 principles represented

- Dashboard is the place to work and think.
- Telegram is a radar, not canonical state.
- HUMAN retains scientific authority.
- No global research lock.
- Evidence-backed claims remain traceable.
- Existing solutions are examined before novelty.
- Coverage limitations remain visible.
- Historical assessments and Human Decisions are not silently overwritten.
- Profile A and Profile B use the same core UX.

## Boundary

All numbers, papers, claims, scores, coverage percentages, ChangeEvents, and Human Decisions in the prototype are dummy illustrative data.

The prototype intentionally does not implement crawling, PostgreSQL, authentication, source adapters, real scoring, Telegram integration, or J2 schema decisions.
