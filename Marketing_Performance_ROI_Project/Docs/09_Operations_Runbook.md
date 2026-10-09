# Operations runbook and handoff

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Scope and prerequisites

This runbook supports the dependency-free local analysis and specifies production handoff responsibilities. Install Python 3.10+ with SQLite 3.25+ window functions. No paid services are needed. A real deployment needs confirmed source authorization, business definitions, identity/access policy, and approved monitoring.

## Shared application operation

Run `python3 Local_System/server.py` from the portfolio root. SQLite persists local workflow edits and refresh history. Admin refresh validates sources in staging and preserves workflow records when source hashes are unchanged. Changed source hashes invalidate affected Passed UAT cases and prior approvals. Stop the server before backing up/restoring Runtime. Read the shared system guide for role and backup details.

## Normal standalone analysis run

1. Extract the entire ZIP. Keep the root scripts folder and project folders together.
2. Retain original CSV bytes. Inspect `Analysis/data_profile.json` for the expected source hash and schema.
3. From the root run `python3 scripts/run_analysis.py`. This loads all six sources, writes Analysis query CSVs and data profiles, and records Quality/analysis_run.json.
4. Run `python3 scripts/validate.py`. Inspect Quality/VALIDATION_REPORT.md and validation_report.json. Any failed validation must be investigated.
5. Review project outputs and interpretation limits. A technical pass does not approve a production report or clear an unresolved Finance reconciliation.
6. If sources change, update definitions and expected controls, repeat discovery as necessary, and rebuild the static previews with the documented builder workflow. The included HTML previews are saved snapshots; the analysis script refreshes CSV/JSON, not their HTML narrative.

## Failure diagnosis

| Symptom | Likely cause | Action | Owner |
| --- | --- | --- | --- |
| Source schema changed | Renamed/added columns or changed export version | Stop ingestion; compare source contract; update mapping through change control | BA / source owner |
| Required value missing | Upstream extract incomplete | Preserve source; record row/field error; obtain corrected extract | Source owner |
| Control total differs | Filter mismatch, new rows, numeric parsing, or wrong source | Compare hash, count, grain, and independent total before publication | Analyst / engineer |
| Undefined ratio | No denominator records | Show undefined; inspect population; do not coerce to zero | Analyst |
| Source mismatch remains | Different scope/definition in independent extracts | Preserve both values and unresolved disposition | Business owner / control reviewer |
| Permission test fails | Missing/incorrect user-scope assignment | Disable publication/export path; correct mapping; retest | Administrator / control reviewer |

## Proposed incident handling

Detect and record the incident with input/build version, affected metric, reporting population, and severity. Contain by withdrawing the affected current report or retaining the prior approved version with a stale notice. Notify the accountable business and control owners through the organization's established process. Diagnose using lineage and independent totals. Correct the source/mapping/query through review, rerun affected tests, then obtain an explicit republish decision. Preserve root cause and prevention action in the defect/change log.

## Rollback

Use the last approved source, mapping, and output version. Verify hashes and reconcile the restored controls. Confirm access mappings are correct independently of data rollback. Record the rollback decision, time, reason, and remaining user impact. The portfolio contains only local versions; no hosted rollback is configured.

## Handoff checklist

- [ ] Source provenance, currency, grain, and keys confirmed.
- [ ] KPI definitions and labels approved by the business owner.
- [ ] SQL/BI results reconciled and unresolved exceptions dispositioned.
- [ ] UAT actually executed with evidence and approver identity.
- [ ] Role/export controls configured and positive/negative cases tested.
- [ ] Refresh schedule, monitoring owner, retention, and incident channel agreed.
- [ ] Prior approved version and rollback procedure tested.
- [ ] Pilot baseline and benefit measurement plan agreed.

All production checklist items remain pending in this portfolio simulation. Executed local analysis evidence is separately recorded in Quality.
