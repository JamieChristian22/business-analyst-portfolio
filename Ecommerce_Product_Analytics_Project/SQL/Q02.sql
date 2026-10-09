-- Q02: Device funnel
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT device,SUM(views) views,SUM(carts) carts,SUM(checkouts) checkouts,SUM(purchases) purchases,1.0*SUM(carts)/NULLIF(SUM(views),0) view_cart_rate,1.0*SUM(checkouts)/NULLIF(SUM(carts),0) cart_checkout_rate,1.0*SUM(purchases)/NULLIF(SUM(checkouts),0) checkout_purchase_rate,1.0*SUM(purchases)/NULLIF(SUM(views),0) view_purchase_rate FROM ecommerce GROUP BY device ORDER BY views DESC,device;
