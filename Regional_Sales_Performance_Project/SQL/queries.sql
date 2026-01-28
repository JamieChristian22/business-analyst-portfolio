-- Tableau Regional Sales Performance dashboard-aligned query pack
-- Table: sales (Month, Zone, City, [Restaurant ID], Sales)

-- Q1: Sales by Zone and Month
SELECT Month, Zone, SUM(Sales) AS Sales
FROM sales
GROUP BY Month, Zone
ORDER BY Month, Zone;

-- Q2: Top Restaurants (last 6 months)
SELECT [Restaurant ID], City, Zone, SUM(Sales) AS Sales
FROM sales
GROUP BY [Restaurant ID], City, Zone
ORDER BY Sales DESC
LIMIT 25;
