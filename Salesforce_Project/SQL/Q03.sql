-- Q03: Stage concentration
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT stage,COUNT(*) opportunities,SUM(amount) amount,SUM(amount*probability) weighted_amount FROM pipeline GROUP BY stage ORDER BY amount DESC,stage;
