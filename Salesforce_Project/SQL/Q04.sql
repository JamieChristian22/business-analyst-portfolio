-- Q04: Open opportunity review queue
-- SQLite 3.25+; canonical schema loaded by scripts/run_analysis.py.
-- Complete supplied extract; amounts USD by portfolio assumption.
SELECT opportunity_id,stage,amount,probability,amount*probability weighted_amount,ROW_NUMBER() OVER(ORDER BY amount*probability DESC,opportunity_id) review_rank FROM pipeline WHERE stage NOT IN ('Closed Won','Closed Lost') ORDER BY weighted_amount DESC,opportunity_id;
