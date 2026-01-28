-- E-commerce Product Analytics dashboard-aligned query pack
-- Table: sessions (YearMonth, device_type, acquisition_channel, country, category,
--                 [Viewed Customers],[Cart Customers],[Checkout Customers],[Purchased Customers],
--                 [Total Revenue],[Total Orders], Profit)

-- Q1: Funnel rates by device_type
SELECT device_type,
       SUM([Viewed Customers]) AS Viewed,
       SUM([Cart Customers]) AS Cart,
       SUM([Checkout Customers]) AS Checkout,
       SUM([Purchased Customers]) AS Purchased,
       SUM([Purchased Customers])*1.0/NULLIF(SUM([Viewed Customers]),0) AS PurchaseConversion
FROM sessions
GROUP BY device_type;

-- Q2: Profit Margin by category
SELECT category,
       SUM(Profit) AS Profit,
       SUM([Total Revenue]) AS [Total Revenue],
       SUM(Profit)/NULLIF(SUM([Total Revenue]),0) AS [Profit Margin]
FROM sessions
GROUP BY category
ORDER BY Profit DESC;
