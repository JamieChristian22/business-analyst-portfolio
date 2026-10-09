-- Q05: Stage probability exceptions
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT source_row,opportunity_id,stage,probability FROM pipeline WHERE probability<0 OR probability>1 OR (stage='Closed Won' AND probability<>1) OR (stage='Closed Lost' AND probability<>0);
