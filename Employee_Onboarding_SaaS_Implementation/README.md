# Employee Onboarding SaaS Implementation | Business & Systems Analysis Case Study

**Portfolio case study • October 15, 2026 • Training / simulated environment**

## Executive summary
This case study examines an employee onboarding workflow from manual handoffs through a proposed SaaS-enabled future state. It demonstrates process discovery, requirements definition, integration planning, API validation, user acceptance testing, defect traceability, and decision governance. It is intended for Business Analyst, Systems Analyst, and Implementation Analyst interviews.

**Scenario:** HR submits new-hire information, a hiring manager approves it, and IT provisions access. Manual handoffs introduce rework, latency, unclear ownership, and inconsistent validation. The proposed future state introduces structured intake, approval routing, validated integration payloads, provisioning orchestration, and auditable status updates.

## Evidence integrity (read first)
- **Actually practiced:** Lucidchart AS-IS process-mapping exercise; Postman GET `/users` returned HTTP 200; Postman POST `/users` returned HTTP 201; four Postman assertions passed; Jira KAN-4 UAT task marked Done; Jira KAN-5 simulated defect created and linked to KAN-4; decision-record task created (final Jira ID not supplied).
- **Mock API caveat:** JSONPlaceholder is a public fake REST API. Its POST response does not prove persistent employee creation, authentication, validation enforcement, provisioning, or production integration.
- **Simulated or proposed:** TO-BE process, requirements, data mapping, controls, negative UAT, rollout plan, risk assessment, decision approval, and architecture are designed artifacts, not implemented or verified production features.
- **Not included:** Original Lucidchart exports, actual Postman screenshots, Jira screenshots, or Jira export, because source exports were not supplied. See `00_Evidence/` for an evidence intake checklist; replace placeholders only with real sanitized exports.

## Navigation
| Folder | Purpose |
|---|---|
| `00_Evidence/` | Evidence register, source verification, sanitization checklist |
| `01_Discovery_and_Process/` | Problem framing, AS-IS and TO-BE flow, BPMN-like lanes, gap analysis |
| `02_Requirements/` | BRD, FRD, user stories, acceptance criteria, NFRs, traceability |
| `03_Architecture_and_Integration/` | Architecture, API contract, field mapping, error handling |
| `04_API_Testing/` | Importable Postman collection, test plan, mock API caveats |
| `05_UAT_and_Defects/` | UAT plan/cases, Jira case notes, defect record, triage workflow |
| `06_Implementation_and_Change/` | Checklist, rollout, RACI, training and support handoff |
| `07_Governance/` | Decision log, RAID register, metrics, stakeholder signoff |
| `08_Interview_and_Portfolio/` | STAR walkthrough, portfolio resume bullets, honest claims |

## Business problem and outcome
**Current state:** Candidate/new-hire data is transferred between HR, manager, and IT using manual handoffs; approval loops and incomplete fields may delay provisioning. **Proposed outcome:** A controlled onboarding workflow with validation before submission, clear approvals, retryable integrations, least-privilege access, and operational visibility.

### Scope
In scope: employee intake, manager approval, data validation, integration orchestration design, IT provisioning request, exception handling, audit trail, UAT, change management. Out of scope: real payroll, background checks, production IAM changes, live HRIS vendor integration, and real employee data.

## Reproducible practice
1. Open `01_Discovery_and_Process/AS_IS_Process.mmd` and `TO_BE_Process.mmd` in a Mermaid-compatible editor; compare with your own Lucidchart exports.
2. Import `04_API_Testing/Employee_Onboarding_Mock_API.postman_collection.json` into Postman. Run GET and POST requests against JSONPlaceholder; read the test scripts and inspect response codes. Network access is required.
3. Review `05_UAT_and_Defects/UAT_Test_Cases.csv`. **Only the positive POST assertion set was observed as passed**; other cases are unexecuted designs.
4. Compare `05_UAT_and_Defects/Jira_Traceability.md` with your actual Jira tickets KAN-4 and KAN-5.
5. Use the implementation checklist, risk register, and decision record to explain how you would move from proof of concept to production.

## Measurable success criteria (proposed, not observed)
- ≥ 98% required-field completeness before provisioning request.
- ≥ 95% standard onboarding requests provisioned within agreed SLA (example target: 1 business day after approval).
- 100% high-risk access requests require documented approval.
- 0 critical open defects at go-live; signed UAT acceptance.
- 100% integration errors logged with correlation IDs and an owner.

## Portfolio evidence and publication safety
Place only sanitized real exports in `00_Evidence/Actual_Exports/` (not shipped). Do not commit API keys, employee PII, internal hostnames, personal emails, browser address bars, cookies, or access tokens. Keep this training repository public only if comfortable with the sanitized content.

## Skills demonstrated
Stakeholder discovery • process mapping • functional/nonfunctional requirements • user stories • BPMN concepts • REST/JSON • Postman scripting • API contract review • data mapping • UAT • defect triage • Jira traceability • change control • implementation readiness • RACI • RAID • metrics.

## Suggested interview framing
“I mapped a manual employee onboarding scenario, designed a controlled target-state process, exercised GET/POST requests against a public mock API, validated four positive POST assertions, and documented UAT and a simulated negative-case defect in Jira. I then drafted the requirements, mappings, and release controls that a real implementation would need.”
