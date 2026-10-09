-- Q05: Contribution exceptions
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT source_row,revenue,cost,source_pnl,revenue-cost-source_pnl difference FROM advertising WHERE ABS(revenue-cost-source_pnl)>0.01 ORDER BY source_row;
