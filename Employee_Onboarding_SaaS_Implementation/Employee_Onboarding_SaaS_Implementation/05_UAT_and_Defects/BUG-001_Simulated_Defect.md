# BUG-001 — Invalid email accepted (SIMULATED)
**Jira:** KAN-5 | **Priority:** High | **Status:** To Do at last verified screenshot | **Label:** `bug` | **Issue type:** Task in screenshot

## Scenario
Hypothetical onboarding SaaS application accepts invalid email `jordan.smith-invalid` and proceeds to the next stage. This behavior was **not reproduced in a real application**.

## Expected
Invalid email is rejected before submission, with actionable feedback and no provisioning request.

## Simulated actual
Invalid email is accepted and onboarding proceeds (scenario assumption, not measured behavior).

## Reproduction procedure for future real test
1. Open a validation-capable onboarding sandbox.
2. Enter otherwise valid synthetic employee fields.
3. Set email to `jordan.smith-invalid`.
4. Submit and capture response, logs, and UI feedback.
5. Verify no provisioning request was dispatched.

## Business impact
Potential bounced communications, identity mismatch, failed provisioning and manual rework.

## Triage
Severity: Major (proposed); Priority: High; Reproducibility: Unknown; Environment: Hypothetical; Owner: To be assigned; Evidence: None; Fix status: Not implemented.

## Resolution criteria
Defined email policy approved; invalid format rejected; error visible; negative test passes; regression and audit checks complete.
