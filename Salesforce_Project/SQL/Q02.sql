-- Q02: Open and closed bridge
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT SUM(CASE WHEN stage NOT IN ('Closed Won','Closed Lost') THEN amount ELSE 0 END) open_pipeline,SUM(CASE WHEN stage NOT IN ('Closed Won','Closed Lost') THEN amount*probability ELSE 0 END) weighted_open_pipeline,SUM(CASE WHEN stage='Closed Won' THEN amount ELSE 0 END) closed_won,SUM(CASE WHEN stage='Closed Lost' THEN amount ELSE 0 END) closed_lost FROM pipeline;
