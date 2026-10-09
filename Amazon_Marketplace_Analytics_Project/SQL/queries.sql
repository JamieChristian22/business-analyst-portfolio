-- Reference query pack. Run scripts/run_analysis.py to export each query separately.

-- Q01: Control totals
SELECT COUNT(*) records, SUM(orders) orders, SUM(units) units, SUM(gmv) gmv, SUM(platform_revenue) platform_revenue, 1.0*SUM(platform_revenue)/NULLIF(SUM(gmv),0) weighted_take_rate, 1.0*SUM(gmv)/NULLIF(SUM(orders),0) aov FROM marketplace;

-- Q02: Monthly marketplace metrics
WITH m AS (SELECT month, SUM(gmv) gmv, SUM(platform_revenue) platform_revenue, SUM(orders) orders FROM marketplace GROUP BY month), p AS (SELECT *, LAG(gmv) OVER(ORDER BY month) prior_gmv FROM m) SELECT *, 1.0*platform_revenue/NULLIF(gmv,0) weighted_take_rate, 1.0*gmv/NULLIF(orders,0) aov, 1.0*(gmv-prior_gmv)/NULLIF(prior_gmv,0) mom_gmv_change FROM p ORDER BY month;

-- Q03: Seller contribution
WITH s AS (SELECT seller, SUM(gmv) gmv, SUM(platform_revenue) platform_revenue, SUM(orders) orders FROM marketplace GROUP BY seller) SELECT *, 1.0*gmv/NULLIF(SUM(gmv) OVER(),0) gmv_share, 1.0*platform_revenue/NULLIF(gmv,0) weighted_take_rate FROM s ORDER BY gmv DESC, seller;

-- Q04: Product Pareto contribution
WITH p AS (SELECT product_id, SUM(gmv) gmv FROM marketplace GROUP BY product_id) SELECT product_id, gmv, ROW_NUMBER() OVER(ORDER BY gmv DESC,product_id) product_rank, 1.0*SUM(gmv) OVER(ORDER BY gmv DESC,product_id ROWS UNBOUNDED PRECEDING)/NULLIF(SUM(gmv) OVER(),0) cumulative_gmv_share FROM p ORDER BY gmv DESC,product_id;

-- Q05: Category and seller drilldown
SELECT category,seller,SUM(gmv) gmv,SUM(platform_revenue) platform_revenue,SUM(orders) orders,1.0*SUM(platform_revenue)/NULLIF(SUM(gmv),0) weighted_take_rate FROM marketplace GROUP BY category,seller ORDER BY gmv DESC,category,seller;
