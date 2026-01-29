-- FP&A dashboard-aligned query pack (names match dashboard measures)
-- Tables: finance_fact (Scenario, AccountCategory, Amount), date_dim (MonthYear)

-- Q1: Revenue Actual vs Budget by MonthYear
SELECT MonthYear,
       SUM(CASE WHEN Scenario='Actual' AND AccountCategory='Revenue' THEN Amount ELSE 0 END) AS [Revenue Actual],
       SUM(CASE WHEN Scenario='Budget' AND AccountCategory='Revenue' THEN Amount ELSE 0 END) AS [Revenue Budget],
       SUM(CASE WHEN Scenario='Actual' AND AccountCategory='Revenue' THEN Amount ELSE 0 END)
       - SUM(CASE WHEN Scenario='Budget' AND AccountCategory='Revenue' THEN Amount ELSE 0 END) AS [Revenue Variance]
FROM finance_fact
GROUP BY MonthYear
ORDER BY MonthYear;

-- Q2: Revenue Variance %
SELECT MonthYear,
       ([Revenue Actual]-[Revenue Budget]) / NULLIF([Revenue Budget],0) AS [Revenue Variance %]
FROM (
  SELECT MonthYear,
         SUM(CASE WHEN Scenario='Actual' AND AccountCategory='Revenue' THEN Amount ELSE 0 END) AS [Revenue Actual],
         SUM(CASE WHEN Scenario='Budget' AND AccountCategory='Revenue' THEN Amount ELSE 0 END) AS [Revenue Budget]
  FROM finance_fact
  GROUP BY MonthYear
) x
ORDER BY MonthYear;
