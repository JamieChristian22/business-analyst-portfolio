# Proposed integration architecture
```mermaid
flowchart LR
 HR[HR SaaS intake] --> V[Validation and duplicate checks]
 V --> AP[Manager approval workflow]
 AP --> EV[Event queue / integration service]
 EV --> MAP[Schema mapping and policy checks]
 MAP --> IAM[Identity provisioning adapter]
 IAM --> DIR[(Directory / SaaS apps)]
 EV --> LOG[(Audit and correlation logs)]
 IAM --> LOG
 IAM --> IT[IT exception queue]
```

## Integration patterns
- **Synchronous:** validate fields and provide immediate errors to HR.
- **Asynchronous:** process approved provisioning through durable queue with retry/dead-letter behavior.
- **Idempotency:** use `onboardingRequestId` to deduplicate repeated requests.
- **Observability:** attach `correlationId` and stage timestamps to all events.
- **Security:** scoped machine identity, encrypted transport, redacted logging, least-privilege roles.

## Boundary note
This is an architecture proposal. JSONPlaceholder GET/POST calls are isolated mock exercises and are **not connected** to HR, manager approval, or IAM systems.
