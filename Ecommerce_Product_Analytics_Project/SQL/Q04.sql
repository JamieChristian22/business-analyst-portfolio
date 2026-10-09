-- Q04: Monthly ecommerce metrics
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
WITH m AS (SELECT month,SUM(views) views,SUM(purchases) purchases,SUM(revenue) revenue FROM ecommerce GROUP BY month),p AS (SELECT *,LAG(revenue) OVER(ORDER BY month) prior_revenue FROM m) SELECT *,1.0*purchases/NULLIF(views,0) view_purchase_rate,1.0*(revenue-prior_revenue)/NULLIF(prior_revenue,0) mom_revenue_change FROM p ORDER BY month;
