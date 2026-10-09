-- Q02: Monthly marketplace metrics
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
WITH m AS (SELECT month, SUM(gmv) gmv, SUM(platform_revenue) platform_revenue, SUM(orders) orders FROM marketplace GROUP BY month), p AS (SELECT *, LAG(gmv) OVER(ORDER BY month) prior_gmv FROM m) SELECT *, 1.0*platform_revenue/NULLIF(gmv,0) weighted_take_rate, 1.0*gmv/NULLIF(orders,0) aov, 1.0*(gmv-prior_gmv)/NULLIF(prior_gmv,0) mom_gmv_change FROM p ORDER BY month;
