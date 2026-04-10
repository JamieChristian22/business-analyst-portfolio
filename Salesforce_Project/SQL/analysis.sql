SELECT Stage,
COUNT(*) AS deals,
SUM(Amount) AS total_amount,
AVG(Probability) AS avg_probability,
SUM(Amount*Probability) AS weighted_pipeline
FROM pipeline
GROUP BY Stage;