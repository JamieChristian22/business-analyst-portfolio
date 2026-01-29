-- Amazon Marketplace dashboard-aligned query pack
-- Table: orders (YearMonth, Category, ProductID, Orders, [Units Sold], GMV, [Marketplace Revenue], [Take Rate %])

-- Q1: GMV, Orders, Units Sold by Category
SELECT Category,
       SUM(GMV) AS GMV,
       SUM(Orders) AS Orders,
       SUM([Units Sold]) AS [Units Sold],
       SUM(GMV)/NULLIF(SUM(Orders),0) AS AOV
FROM orders
GROUP BY Category
ORDER BY GMV DESC;

-- Q2: Take Rate % and Marketplace Revenue trend
SELECT YearMonth,
       SUM([Marketplace Revenue]) AS [Marketplace Revenue],
       SUM([Marketplace Revenue]) / NULLIF(SUM(GMV),0) AS [Take Rate %]
FROM orders
GROUP BY YearMonth
ORDER BY YearMonth;
