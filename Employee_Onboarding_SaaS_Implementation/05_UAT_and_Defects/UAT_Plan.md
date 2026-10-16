# UAT plan
**Purpose:** Business owners confirm onboarding flow meets approved requirements before production release.

## Entry criteria
Requirements baseline approved; target environment available; synthetic identities provisioned; test cases reviewed; roles and approvals configured; defects triage owner assigned.

## Roles
Business owner approves acceptance; HR and manager execute process cases; IT validates exception handling; QA/BA records results; security reviews privileged access.

## Execution
For each case record: date, tester, environment, data set, steps, expected, actual, result, evidence, Jira key. Attach reproducible defect steps and impact to failures. Re-run fixed cases and relevant regressions.

## Exit criteria (proposed)
100% Must-have cases executed; 0 open Critical/High defects without approved exception; all approval/audit cases pass; data/privacy review completed; documented signoff.

## Current lab result
Only UAT-001 positive mock API checks were observed. This does **not** meet production UAT exit criteria. Remaining cases in CSV are planned, not passed.
