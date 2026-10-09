-- Q02: Zone and city sales
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT zone,city,SUM(sales) sales,COUNT(DISTINCT restaurant_id) restaurants,1.0*SUM(sales)/NULLIF(SUM(SUM(sales)) OVER(),0) sales_share FROM restaurant_sales GROUP BY zone,city ORDER BY sales DESC,zone,city;
