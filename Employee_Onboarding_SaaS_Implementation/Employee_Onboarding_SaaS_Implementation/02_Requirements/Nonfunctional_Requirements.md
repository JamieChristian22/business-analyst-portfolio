# Nonfunctional requirements (proposed)
| ID | Category | Proposed criterion | Validation approach |
|---|---|---|---|
| NFR-01 | Security | TLS in transit; scoped service credentials; no secrets in logs | Security review |
| NFR-02 | Privacy | Synthetic data in testing; minimize PII; retention policy approved | Privacy review |
| NFR-03 | Availability | Agree uptime and recovery targets with service owners | Operational readiness review |
| NFR-04 | Performance | Intake validation p95 ≤2 s under agreed test load | Load test (not run) |
| NFR-05 | Observability | Correlation ID across every integration step | Trace sampling |
| NFR-06 | Accessibility | Form supports keyboard navigation and accessible errors | Accessibility testing |
| NFR-07 | Resilience | Exponential backoff and dead-letter escalation for transient errors | Failure injection (not run) |
| NFR-08 | Audit | Record approval and provisioning events with restricted access | Audit walkthrough |
