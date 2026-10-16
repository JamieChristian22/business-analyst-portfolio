# User stories (proposed)
## US-01 — Validate employee intake
As an HR coordinator, I want missing or invalid required fields flagged before submission so that IT receives actionable onboarding requests.
**Given** an invalid email `jordan.smith-invalid`, **when** HR submits, **then** the system shows an error and does not create a provisioning request.
**Given** a valid request, **when** HR submits, **then** it enters Pending Approval with a traceable request ID.

## US-02 — Manager approval
As a hiring manager, I want to approve or reject onboarding requests so that only authorized new hires are provisioned.
**Given** an approval is pending, **when** I approve, **then** the platform stores approver identity and timestamp before dispatching downstream work.

## US-03 — IT exception ownership
As an IT analyst, I want failed provisioning requests assigned with error codes so that I can investigate and resolve them within SLA.
**Given** a downstream timeout, **when** bounded retries fail, **then** the request enters Exception with a correlation ID and assigned owner.

## US-04 — Audit reporting
As a compliance reviewer, I want approval and provisioning histories so that access decisions can be reconstructed without relying on email threads.
**Given** a completed onboarding, **when** I request its history, **then** I can see the event sequence and responsible actors.
