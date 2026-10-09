-- Q01: Restaurant controls
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT COUNT(*) records,COUNT(DISTINCT restaurant_id) restaurants,COUNT(DISTINCT month) months,SUM(sales) sales FROM restaurant_sales;
