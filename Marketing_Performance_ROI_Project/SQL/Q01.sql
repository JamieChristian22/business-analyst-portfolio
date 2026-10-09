-- Q01: Advertising controls
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT COUNT(*) records,SUM(impressions) impressions,SUM(clicks) clicks,SUM(conversions) conversions,SUM(cost) cost,SUM(revenue) revenue,SUM(revenue)-SUM(cost) ad_only_contribution FROM advertising;
