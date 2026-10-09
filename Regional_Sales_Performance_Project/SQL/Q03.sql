-- Q03: Adjacent-month sales change
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
WITH m AS (SELECT month,SUM(sales) sales FROM restaurant_sales GROUP BY month),p AS (SELECT *,LAG(month) OVER(ORDER BY month) prior_month,LAG(sales) OVER(ORDER BY month) prior_sales FROM m) SELECT *,CASE WHEN date(month||'-01')=date(prior_month||'-01','+1 month') THEN 1.0*(sales-prior_sales)/NULLIF(prior_sales,0) ELSE NULL END mom_sales_change FROM p ORDER BY month;
