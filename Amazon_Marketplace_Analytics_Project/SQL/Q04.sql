-- Q04: Product Pareto contribution
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
WITH p AS (SELECT product_id, SUM(gmv) gmv FROM marketplace GROUP BY product_id) SELECT product_id, gmv, ROW_NUMBER() OVER(ORDER BY gmv DESC,product_id) product_rank, 1.0*SUM(gmv) OVER(ORDER BY gmv DESC,product_id ROWS UNBOUNDED PRECEDING)/NULLIF(SUM(gmv) OVER(),0) cumulative_gmv_share FROM p ORDER BY gmv DESC,product_id;
