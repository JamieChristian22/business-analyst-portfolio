-- Q01: Finance controls
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT scenario,account_category,COUNT(*) records,SUM(amount) amount FROM finance GROUP BY scenario,account_category ORDER BY scenario,account_category;
