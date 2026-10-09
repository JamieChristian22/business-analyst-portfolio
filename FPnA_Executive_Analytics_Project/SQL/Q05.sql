-- Q05: Budget completeness
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT month,department,account_category,SUM(CASE WHEN scenario='Actual' THEN 1 ELSE 0 END) actual_records,SUM(CASE WHEN scenario='Budget' THEN 1 ELSE 0 END) budget_records FROM finance GROUP BY month,department,account_category HAVING SUM(CASE WHEN scenario='Actual' THEN 1 ELSE 0 END)=0 OR SUM(CASE WHEN scenario='Budget' THEN 1 ELSE 0 END)=0;
