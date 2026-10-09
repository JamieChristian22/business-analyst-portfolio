-- Q05: Category and seller drilldown
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT category,seller,SUM(gmv) gmv,SUM(platform_revenue) platform_revenue,SUM(orders) orders,1.0*SUM(platform_revenue)/NULLIF(SUM(gmv),0) weighted_take_rate FROM marketplace GROUP BY category,seller ORDER BY gmv DESC,category,seller;
