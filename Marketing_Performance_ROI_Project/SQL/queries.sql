-- Tableau Marketing Performance dashboard-aligned query pack
-- Table: marketing (Month, [Ad Group], Device, Impressions, Clicks, CTR, CPC, [Conv Rate], Conversions, Cost, Revenue, [Sale Amount], [P&L])

-- Q1: Month trend for Cost, Revenue, P&L
SELECT Month,
       SUM(Cost) AS Cost,
       SUM(Revenue) AS Revenue,
       SUM([P&L]) AS [P&L]
FROM marketing
GROUP BY Month
ORDER BY Month;

-- Q2: Ad Group performance (Efficiency)
SELECT [Ad Group],
       SUM(Impressions) AS Impressions,
       SUM(Clicks) AS Clicks,
       AVG(CTR) AS CTR,
       AVG(CPC) AS CPC,
       AVG([Conv Rate]) AS [Conv Rate],
       SUM(Conversions) AS Conversions,
       SUM(Cost) AS Cost,
       SUM(Revenue) AS Revenue,
       SUM([P&L]) AS [P&L]
FROM marketing
GROUP BY [Ad Group]
ORDER BY [P&L] DESC;
