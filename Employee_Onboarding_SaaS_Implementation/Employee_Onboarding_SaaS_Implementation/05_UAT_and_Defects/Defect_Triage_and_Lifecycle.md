# Defect triage SOP
**States:** New/To Do → Triage → In Progress → In Review → Retest → Done; Blocked is an exception state, not necessarily a sequential stage.

**Minimum ticket fields:** title, environment, build, steps, test data (synthetic), expected, actual, screenshots/logs, severity, priority, owner, related requirement/test, root cause, retest evidence.

**Priority rubric:** Critical = security/data loss or widespread outage; High = core flow blocked or severe business risk; Medium = workaround exists; Low = cosmetic/nonblocking. Confirm with business owner.

**Triage meeting:** review reproducibility and evidence; distinguish defect vs requirement change; assess blast radius; assign owner; choose fix or documented exception; record decision.

**Closure gate:** fix deployed to correct environment, original case passes, related regression tests pass, evidence attached, stakeholder accepts.

**Lab caveat:** KAN-5 is a hypothetical case and should remain unverified until tested against an actual application.
