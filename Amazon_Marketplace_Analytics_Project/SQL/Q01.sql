-- Q01: Control totals
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT COUNT(*) records, SUM(orders) orders, SUM(units) units, SUM(gmv) gmv, SUM(platform_revenue) platform_revenue, 1.0*SUM(platform_revenue)/NULLIF(SUM(gmv),0) weighted_take_rate, 1.0*SUM(gmv)/NULLIF(SUM(orders),0) aov FROM marketplace;
