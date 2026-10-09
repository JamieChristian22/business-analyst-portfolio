# Working local business analysis system

This application implements the portfolio's dashboards and delivery workflows with Python and SQLite. It runs on your computer and requires no paid service or pip package.

## Start

From the extracted portfolio root:

```bash
python3 Local_System/server.py
```

On Windows, use `py Local_System/server.py`. Open **http://127.0.0.1:8765** in your browser. Four account passwords are generated on first launch and saved in `Runtime/LOCAL_ACCOUNTS.txt`. Sign in with username admin, analyst, reviewer, or viewer and its generated password. Keep this file private on your computer.

The application binds only to 127.0.0.1. It is a local demonstration, not an internet hosting configuration. Python 3.10+ and SQLite 3.25+ are required. If the port is occupied, use `--port 8766` and open that port. Stop with Ctrl+C.

## Implemented features

- Six dashboards run the canonical SQL against persisted source facts. Month and dimension filters recalculate the selected population. Clear filters restores the whole extract.
- Source drilldown preserves source_row lineage and pages 100 records at a time. Aggregate exports are available to viewers; detail export is denied to viewers on the server.
- Requirements, UAT, gaps, source refresh runs, and audit history persist in SQLite across restarts.
- Analysts record UAT actual results and evidence, submit requirements, and propose gap closure. Reviewer accounts independently approve/reject requirements and close/reopen proposed gaps.
- A requirement cannot be approved until its three UAT cases pass with evidence. Changing those results invalidates Submitted or Approved status. All approvals remain local demonstration records.
- Updates require a valid session, CSRF token, and current record version. Stale edits return a conflict. Passwords use salted PBKDF2 hashes; sessions expire after an hour.
- Admin refresh validates all seven files in staging before transactionally replacing analytical facts. Workflow records stay intact. Input hashes, actor, and successful refresh version are logged.

## Role matrix

| Role | Dashboard | Source detail | UAT edits | Submit / propose closure | Approve / reject | Source refresh | Audit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Viewer | Yes | Denied | Denied | Denied | Denied | Denied | Denied |
| Analyst | Yes | Yes | Yes | Yes | Denied | Denied | Denied |
| Reviewer | Yes | Yes | Yes | Denied | Yes | Denied | Yes |
| Admin | Yes | Yes | Denied | Denied | Denied | Yes | Yes |

These are server-enforced application roles. Enterprise SSO and zone/department/seller row-level authorization are separate gap-analysis items. Local admin is not granted business approval authority.

## Walkthrough

1. Sign in as viewer. Filter Regional Sales to a month and zone. Compare the selected totals to the query table. Try source detail export: the API denies it.
2. Sign out and sign in as analyst. Open a requirement's three UAT cases. Execute the described checks and enter your actual results and evidence. Only select Passed if you performed the check.
3. Submit the linked requirement. Sign in as reviewer and record the decision with evidence. Approval requires all three cases to pass.
4. Change one linked UAT result. The requirement becomes Needs review and requires a fresh submission/review.
5. Open Gap analysis. Analyst proposes closure with evidence; reviewer closes or returns it to Open. Closing a local requirement does not automatically close a production gap.
6. As admin, refresh sources and inspect audit history. Restart the application: workflow records remain.

## Data and backup

Runtime/workbench.sqlite is created on first launch. The ZIP ships **without** personal demo accounts, session tokens, runtime credentials, or a preapproved database. Source CSVs and initial registers stay unchanged. App edits do not synchronize to CSV, Excel, Jira, Salesforce, or Power BI.

Stop the server before copying the Runtime folder for backup. Restore that folder while stopped, start the server, and verify dashboard controls and workflow records. Do not delete Runtime unless you intend to discard local workflow records and generate fresh accounts.

## Test

```bash
python3 Local_System/test_system.py
```

Tests use a temporary database and generated credentials, exercise the HTTP endpoints, and leave the delivered source/registers unchanged. Results are written to Quality/local_system_tests.json. Browser smoke tests are recorded separately when performed.

## Boundaries

Historical native dashboards remain preserved, not certified. The local audit log is append-only through the app API, but someone with direct file access can modify SQLite. Production hosting needs HTTPS, enterprise identity, stronger operational security, monitoring, and approved source contracts. Actual business acceptance and measured benefits require real reviewers and a pilot; the application does not fabricate them.
