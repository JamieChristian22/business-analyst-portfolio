-- Q05: Funnel validity exceptions
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT source_row,views,carts,checkouts,purchases FROM ecommerce WHERE views<carts OR carts<checkouts OR checkouts<purchases OR purchases<0 ORDER BY source_row;
