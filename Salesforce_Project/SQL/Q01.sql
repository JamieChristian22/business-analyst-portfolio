-- Q01: Opportunity controls
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT COUNT(*) records,COUNT(DISTINCT opportunity_id) unique_opportunities,SUM(amount) all_record_amount,SUM(amount*probability) all_record_weighted_amount FROM pipeline;
