-- Q03: Department revenue variance
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
WITH d AS (SELECT department,SUM(CASE WHEN scenario='Actual' AND account_category='Revenue' THEN amount ELSE 0 END) revenue_actual,SUM(CASE WHEN scenario='Budget' AND account_category='Revenue' THEN amount ELSE 0 END) revenue_budget FROM finance GROUP BY department) SELECT *,revenue_actual-revenue_budget revenue_variance,1.0*(revenue_actual-revenue_budget)/NULLIF(revenue_budget,0) revenue_variance_rate FROM d ORDER BY revenue_variance,department;
