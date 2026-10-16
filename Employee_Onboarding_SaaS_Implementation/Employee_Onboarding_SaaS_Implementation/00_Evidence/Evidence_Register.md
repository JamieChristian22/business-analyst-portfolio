# Evidence register
| ID | Artifact | Evidence status | Verification / limitations |
|---|---|---|---|
| EV-01 | Lucidchart AS-IS employee onboarding diagram | User screenshot observed; original export not provided | Diagram exists in user's workspace; export and sanitize before publication |
| EV-02 | Lucidchart TO-BE diagram | Not independently verified | Earlier generation attempt showed an error; included TO-BE Mermaid is a **proposed design** |
| EV-03 | Postman GET `/users` | Observed in screenshot | HTTP 200 on JSONPlaceholder mock endpoint |
| EV-04 | Postman POST `/users` | Observed in screenshot | HTTP 201; response echoed mock employee fields and generated ID |
| EV-05 | Postman assertions | Observed in screenshot | 4/4 passed: status, name, email, ID |
| EV-06 | Jira KAN-4 UAT | Observed in screenshot | Marked Done, medium priority, `uat` label |
| EV-07 | Jira KAN-5 simulated defect | Observed in screenshot | High priority, `bug` label; simulated issue, not observed application bug |
| EV-08 | Jira issue link | Observed in screenshot | KAN-5 **relates to** KAN-4 |
| EV-09 | Jira decision record | User reported created | Exact Jira issue key and saved description not independently verified |

## Evidence collection procedure
1. Export diagrams as PDF or PNG from Lucidchart and verify readability.
2. Export the actual Postman collection with scripts and capture test-result screenshots.
3. Capture sanitized Jira ticket views showing ID, status, acceptance criteria, and issue link.
4. Name files `EV-01_AS_IS.png`, `EV-05_Postman_4of4.png`, etc.; record capture dates.
5. Redact names, emails, organization URLs, user handles, tokens, and browser chrome where unnecessary.
6. Never label designed scenarios as production execution evidence.
