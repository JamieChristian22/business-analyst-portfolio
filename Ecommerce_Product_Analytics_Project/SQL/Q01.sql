-- Q01: Funnel control totals
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT COUNT(*) records,SUM(views) views,SUM(carts) carts,SUM(checkouts) checkouts,SUM(purchases) purchases,SUM(orders) orders,SUM(revenue) revenue,SUM(profit) profit FROM ecommerce;
