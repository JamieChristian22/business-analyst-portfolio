-- Q02: Ad group efficiency
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT ad_group,SUM(cost) cost,SUM(revenue) revenue,SUM(conversions) conversions,SUM(clicks) clicks,SUM(impressions) impressions,1.0*SUM(revenue)/NULLIF(SUM(cost),0) roas,1.0*SUM(clicks)/NULLIF(SUM(impressions),0) ctr,1.0*SUM(cost)/NULLIF(SUM(clicks),0) cpc,1.0*SUM(conversions)/NULLIF(SUM(clicks),0) conversion_rate,SUM(revenue)-SUM(cost) ad_only_contribution FROM advertising GROUP BY ad_group ORDER BY roas DESC,ad_group;
