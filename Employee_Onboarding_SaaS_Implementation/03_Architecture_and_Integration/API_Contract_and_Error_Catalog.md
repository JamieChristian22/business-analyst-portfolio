# Proposed production API contract (not implemented)
## POST /v1/onboarding-requests
**Headers:** `Authorization: Bearer <redacted>`; `Content-Type: application/json`; `Idempotency-Key: <uuid>`

Example request (synthetic):
```json
{"employeeId":"EMP-1001","fullName":"Jordan Example","email":"jordan.example@example.org","department":"IT","managerId":"MGR-2001","startDate":"2026-11-02","roleCode":"BA-STD"}
```

Example accepted response (proposed):
```json
{"requestId":"ONB-000123","status":"PENDING_APPROVAL","correlationId":"demo-correlation-123"}
```

## Expected response codes
| Code | Meaning | Required behavior |
|---|---|---|
| 202 | Accepted for approval | Return request and correlation IDs |
| 400 | Malformed payload | Return safe validation error |
| 401/403 | Missing or insufficient authorization | Deny and audit |
| 409 | Duplicate employee/request | Return conflict with reference |
| 422 | Valid JSON but invalid business fields | Return field errors; no dispatch |
| 429 | Rate limited | Respect retry-after |
| 500/503 | Server/downstream unavailable | Alert, bounded retry and escalation |

## Negative-path tests
Invalid email, missing manager ID, duplicate employee ID, unauthorized caller, invalid role code, expired approval, network timeout, repeated idempotency key.

**Contrast with mock:** JSONPlaceholder `POST /users` commonly responds 201 with echoed fields and an ID. This is not evidence that any validation rules above are enforced.
