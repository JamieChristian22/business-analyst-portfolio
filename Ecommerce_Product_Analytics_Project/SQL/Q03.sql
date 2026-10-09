-- Q03: Channel economics
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT channel,SUM(views) views,SUM(purchases) purchases,SUM(orders) orders,SUM(revenue) revenue,SUM(profit) profit,1.0*SUM(profit)/NULLIF(SUM(revenue),0) profit_margin,1.0*SUM(revenue)/NULLIF(SUM(orders),0) aov FROM ecommerce GROUP BY channel ORDER BY revenue DESC,channel;
