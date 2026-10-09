-- Q05: Duplicate key exceptions
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT restaurant_id,month,COUNT(*) records FROM restaurant_sales GROUP BY restaurant_id,month HAVING COUNT(*)>1;
