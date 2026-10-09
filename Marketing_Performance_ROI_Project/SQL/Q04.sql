-- Q04: Monthly advertising trend
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
WITH m AS (SELECT month,SUM(cost) cost,SUM(revenue) revenue FROM advertising GROUP BY month),p AS (SELECT *,LAG(cost) OVER(ORDER BY month) prior_cost FROM m) SELECT *,1.0*revenue/NULLIF(cost,0) roas,1.0*(cost-prior_cost)/NULLIF(prior_cost,0) mom_cost_change FROM p ORDER BY month;
