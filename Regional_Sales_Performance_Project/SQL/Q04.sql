-- Q04: Restaurant rank and coverage
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT restaurant_id,MIN(city) city,MIN(zone) zone,SUM(sales) sales,COUNT(DISTINCT month) months_reported,ROW_NUMBER() OVER(ORDER BY SUM(sales) DESC,restaurant_id) sales_rank FROM restaurant_sales GROUP BY restaurant_id ORDER BY sales DESC,restaurant_id;
