-- Q03: Device efficiency
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT device,SUM(cost) cost,SUM(revenue) revenue,SUM(clicks) clicks,SUM(conversions) conversions,1.0*SUM(revenue)/NULLIF(SUM(cost),0) roas,1.0*SUM(conversions)/NULLIF(SUM(clicks),0) conversion_rate FROM advertising GROUP BY device ORDER BY device;
