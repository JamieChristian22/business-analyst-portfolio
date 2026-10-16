# API test plan and execution evidence
## Purpose
Practice HTTP, JSON request bodies, response codes, and scripted assertions in Postman using JSONPlaceholder.

## Execution log (based on user-shared screenshots)
| ID | Endpoint | Observation | Result |
|---|---|---|---|
| API-GET-01 | GET `https://jsonplaceholder.typicode.com/users` | HTTP 200, JSON array returned | Observed success |
| API-POST-01 | POST `https://jsonplaceholder.typicode.com/users` | HTTP 201; synthetic Jordan Smith record echoed, ID returned | Observed success |
| API-POST-T1 | POST `/users` | Status 201 | PASS |
| API-POST-T2 | POST `/users` | Name equals request | PASS |
| API-POST-T3 | POST `/users` | Email equals request | PASS |
| API-POST-T4 | POST `/users` | ID returned | PASS |

## Limitations
This public fake API does not provide evidence of input validation, identity uniqueness, durable persistence, provisioning, access controls, or HR integration. Response times vary and are not used as production benchmarks. Collection supplied here is a reproducible reconstruction, not the user's exported original.

## Test design expansion (not executed)
- Invalid email should be rejected by **a real target implementation**, not inferred from JSONPlaceholder.
- Duplicate external ID should be rejected or reconciled.
- Missing approval should prevent provisioning.
- Timeout should produce bounded retries and an IT escalation.
- Repeated request ID should not create duplicate accounts.

## How to run
Import collection in Postman; send GET and POST; open **Test Results**; capture only sanitized screenshots. If behavior differs, record the actual result rather than changing the expected observation retroactively.
