-- Reference query pack. Run scripts/run_analysis.py to export each query separately.

-- Q01: Funnel control totals
SELECT COUNT(*) records,SUM(views) views,SUM(carts) carts,SUM(checkouts) checkouts,SUM(purchases) purchases,SUM(orders) orders,SUM(revenue) revenue,SUM(profit) profit FROM ecommerce;

-- Q02: Device funnel
SELECT device,SUM(views) views,SUM(carts) carts,SUM(checkouts) checkouts,SUM(purchases) purchases,1.0*SUM(carts)/NULLIF(SUM(views),0) view_cart_rate,1.0*SUM(checkouts)/NULLIF(SUM(carts),0) cart_checkout_rate,1.0*SUM(purchases)/NULLIF(SUM(checkouts),0) checkout_purchase_rate,1.0*SUM(purchases)/NULLIF(SUM(views),0) view_purchase_rate FROM ecommerce GROUP BY device ORDER BY views DESC,device;

-- Q03: Channel economics
SELECT channel,SUM(views) views,SUM(purchases) purchases,SUM(orders) orders,SUM(revenue) revenue,SUM(profit) profit,1.0*SUM(profit)/NULLIF(SUM(revenue),0) profit_margin,1.0*SUM(revenue)/NULLIF(SUM(orders),0) aov FROM ecommerce GROUP BY channel ORDER BY revenue DESC,channel;

-- Q04: Monthly ecommerce metrics
WITH m AS (SELECT month,SUM(views) views,SUM(purchases) purchases,SUM(revenue) revenue FROM ecommerce GROUP BY month),p AS (SELECT *,LAG(revenue) OVER(ORDER BY month) prior_revenue FROM m) SELECT *,1.0*purchases/NULLIF(views,0) view_purchase_rate,1.0*(revenue-prior_revenue)/NULLIF(prior_revenue,0) mom_revenue_change FROM p ORDER BY month;

-- Q05: Funnel validity exceptions
SELECT source_row,views,carts,checkouts,purchases FROM ecommerce WHERE views<carts OR carts<checkouts OR checkouts<purchases OR purchases<0 ORDER BY source_row;
