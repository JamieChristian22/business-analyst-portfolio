-- Reference query pack. Run scripts/run_analysis.py to export each query separately.

-- Q01: Opportunity controls
SELECT COUNT(*) records,COUNT(DISTINCT opportunity_id) unique_opportunities,SUM(amount) all_record_amount,SUM(amount*probability) all_record_weighted_amount FROM pipeline;

-- Q02: Open and closed bridge
SELECT SUM(CASE WHEN stage NOT IN ('Closed Won','Closed Lost') THEN amount ELSE 0 END) open_pipeline,SUM(CASE WHEN stage NOT IN ('Closed Won','Closed Lost') THEN amount*probability ELSE 0 END) weighted_open_pipeline,SUM(CASE WHEN stage='Closed Won' THEN amount ELSE 0 END) closed_won,SUM(CASE WHEN stage='Closed Lost' THEN amount ELSE 0 END) closed_lost FROM pipeline;

-- Q03: Stage concentration
SELECT stage,COUNT(*) opportunities,SUM(amount) amount,SUM(amount*probability) weighted_amount FROM pipeline GROUP BY stage ORDER BY amount DESC,stage;

-- Q04: Open opportunity review queue
SELECT opportunity_id,stage,amount,probability,amount*probability weighted_amount,ROW_NUMBER() OVER(ORDER BY amount*probability DESC,opportunity_id) review_rank FROM pipeline WHERE stage NOT IN ('Closed Won','Closed Lost') ORDER BY weighted_amount DESC,opportunity_id;

-- Q05: Stage probability exceptions
SELECT source_row,opportunity_id,stage,probability FROM pipeline WHERE probability<0 OR probability>1 OR (stage='Closed Won' AND probability<>1) OR (stage='Closed Lost' AND probability<>0);
