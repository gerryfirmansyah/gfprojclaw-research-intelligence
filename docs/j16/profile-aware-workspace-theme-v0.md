# Profile-aware Workspace Theme v0

J16 separates three concepts: Research Profile canonical context, its administrative preferred workspace theme, and a HUMAN browser-local override.

Supported presentation choices are System / Auto, Light, Dark, Research Blue, Scholar Green, and Executive Indigo. The three named workspace themes are orientation cues only; they are not scientific classifications and never alter evidence, claims, reasoning, ranking, or decisions.

`profile_configuration_jsonb.workspace_theme` stores the Profile preference through the existing atomic Admin Profile+Project version workflow. Changing it therefore requires Preview and Confirm and preserves version history.

A browser-local selection takes precedence and is stored in `gfprojclaw-theme`. “Use Profile Preference” removes that local override. Research Copilot applies the active Profile preference only when no local override exists.

Semantic status meaning must remain independent from workspace theme. Error, warning/attention, success/active, UNKNOWN/NOT_AVAILABLE/NOT_RUN and HUMAN scientific boundaries retain their meaning across themes.
