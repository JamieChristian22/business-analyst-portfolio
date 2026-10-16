# DEC-001 — Employee Onboarding Validation Decision
**Status:** Proposed / pending approval (not an approved production decision)
**Date:** 2026-10-15
**Decision owner:** Business / Product Owner — to be assigned

## Context
Positive POST assertions passed against a fake REST API, but no validation-capable onboarding application has been tested for malformed email behavior.

## Options
1. **Proceed without negative tests:** fastest, unacceptable unquantified data-quality risk.
2. **Require field validation and negative UAT before go-live (recommended):** more upfront work, stronger controls.
3. **Manual HR verification only:** fallback but inconsistent and labor-intensive.

## Recommendation
Adopt option 2, subject to owner approval: define email policy, implement validation in the real target system, and require evidence from negative UAT before release.

## Evidence
AS-IS mapping exercise; Postman mock GET 200 and POST 201; four passing positive assertions; Jira KAN-4 Done; KAN-5 simulated issue related to KAN-4.

## Consequences
Adds design/test effort and a release gate; reduces risk of invalid identity records and downstream provisioning failures.

## Actions
- Product owner approve validation policy.
- BA define acceptance criteria and update traceability.
- Engineering implement validation in sandbox.
- QA/HR execute negative tests and record evidence.
- Release owner confirm exit criteria and signoff.

**Approval:** Pending. **Actual production change:** None.
