-- Q03: Seller contribution
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
WITH s AS (SELECT seller, SUM(gmv) gmv, SUM(platform_revenue) platform_revenue, SUM(orders) orders FROM marketplace GROUP BY seller) SELECT *, 1.0*gmv/NULLIF(SUM(gmv) OVER(),0) gmv_share, 1.0*platform_revenue/NULLIF(gmv,0) weighted_take_rate FROM s ORDER BY gmv DESC, seller;
