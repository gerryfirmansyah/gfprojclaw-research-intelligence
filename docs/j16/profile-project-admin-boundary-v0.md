# J16 Profile/Project Admin Boundary v0

- Research Copilot displays active Profile and Project context read-only.
- Admin Copilot owns Profile/Project configuration mutation.
- Admin form requires HUMAN/admin actor and a reason, validates structured required fields and JSON, and shows a preview before confirmation.
- Profile and Project versions are created together by one database transaction; linked rows are locked before version creation and canonical pointers advance together or roll back together.
- Configuration mutation returns `scientific_decision=false`; administrative configuration never establishes a scientific conclusion.
- Authentication/authorization for entry to Admin Copilot remains a J16 acceptance item and is not implied by the actor text field.
- Research Journey stage guidance is illustrative/non-canonical. Today uses short methodological descriptions; the full R0-R16 view uses expanded descriptions. Research is explicitly iterative.
