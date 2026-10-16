# Jira traceability record
| Jira key | Artifact | Observed status | Relationship |
|---|---|---|---|
| KAN-4 | UAT-001 Validate Employee Onboarding API | Done | Related to KAN-5 |
| KAN-5 | BUG-001 Employee Email Validation Failure | To Do | **relates to** KAN-4 |
| Not provided | DEC-001 Employee Onboarding Validation Decision | User reported created | No exact Jira key independently verified |

**Interpretation:** KAN-4 covers four positive mock API assertions. KAN-5 is a simulated negative-case defect for a scenario not validated by those assertions. Link is traceability, **not** evidence of a failed KAN-4 test.

## Jira evidence checklist
- [x] KAN-4 created and marked Done (observed)
- [x] KAN-5 created with High priority and `bug` label (observed)
- [x] KAN-5 relates to KAN-4 (observed)
- [ ] Real negative-case reproduction captured
- [ ] Real defect fix deployed and retested
- [ ] Decision approval captured
