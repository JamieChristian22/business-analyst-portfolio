-- Reference query pack. Run scripts/run_analysis.py to export each query separately.

-- Q01: Advertising controls
SELECT COUNT(*) records,SUM(impressions) impressions,SUM(clicks) clicks,SUM(conversions) conversions,SUM(cost) cost,SUM(revenue) revenue,SUM(revenue)-SUM(cost) ad_only_contribution FROM advertising;

-- Q02: Ad group efficiency
SELECT ad_group,SUM(cost) cost,SUM(revenue) revenue,SUM(conversions) conversions,SUM(clicks) clicks,SUM(impressions) impressions,1.0*SUM(revenue)/NULLIF(SUM(cost),0) roas,1.0*SUM(clicks)/NULLIF(SUM(impressions),0) ctr,1.0*SUM(cost)/NULLIF(SUM(clicks),0) cpc,1.0*SUM(conversions)/NULLIF(SUM(clicks),0) conversion_rate,SUM(revenue)-SUM(cost) ad_only_contribution FROM advertising GROUP BY ad_group ORDER BY roas DESC,ad_group;

-- Q03: Device efficiency
SELECT device,SUM(cost) cost,SUM(revenue) revenue,SUM(clicks) clicks,SUM(conversions) conversions,1.0*SUM(revenue)/NULLIF(SUM(cost),0) roas,1.0*SUM(conversions)/NULLIF(SUM(clicks),0) conversion_rate FROM advertising GROUP BY device ORDER BY device;

-- Q04: Monthly advertising trend
WITH m AS (SELECT month,SUM(cost) cost,SUM(revenue) revenue FROM advertising GROUP BY month),p AS (SELECT *,LAG(cost) OVER(ORDER BY month) prior_cost FROM m) SELECT *,1.0*revenue/NULLIF(cost,0) roas,1.0*(cost-prior_cost)/NULLIF(prior_cost,0) mom_cost_change FROM p ORDER BY month;

-- Q05: Contribution exceptions
SELECT source_row,revenue,cost,source_pnl,revenue-cost-source_pnl difference FROM advertising WHERE ABS(revenue-cost-source_pnl)>0.01 ORDER BY source_row;
