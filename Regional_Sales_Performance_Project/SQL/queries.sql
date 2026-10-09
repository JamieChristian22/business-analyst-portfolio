-- Reference query pack. Run scripts/run_analysis.py to export each query separately.

-- Q01: Restaurant controls
SELECT COUNT(*) records,COUNT(DISTINCT restaurant_id) restaurants,COUNT(DISTINCT month) months,SUM(sales) sales FROM restaurant_sales;

-- Q02: Zone and city sales
SELECT zone,city,SUM(sales) sales,COUNT(DISTINCT restaurant_id) restaurants,1.0*SUM(sales)/NULLIF(SUM(SUM(sales)) OVER(),0) sales_share FROM restaurant_sales GROUP BY zone,city ORDER BY sales DESC,zone,city;

-- Q03: Adjacent-month sales change
WITH m AS (SELECT month,SUM(sales) sales FROM restaurant_sales GROUP BY month),p AS (SELECT *,LAG(month) OVER(ORDER BY month) prior_month,LAG(sales) OVER(ORDER BY month) prior_sales FROM m) SELECT *,CASE WHEN date(month||'-01')=date(prior_month||'-01','+1 month') THEN 1.0*(sales-prior_sales)/NULLIF(prior_sales,0) ELSE NULL END mom_sales_change FROM p ORDER BY month;

-- Q04: Restaurant rank and coverage
SELECT restaurant_id,MIN(city) city,MIN(zone) zone,SUM(sales) sales,COUNT(DISTINCT month) months_reported,ROW_NUMBER() OVER(ORDER BY SUM(sales) DESC,restaurant_id) sales_rank FROM restaurant_sales GROUP BY restaurant_id ORDER BY sales DESC,restaurant_id;

-- Q05: Duplicate key exceptions
SELECT restaurant_id,month,COUNT(*) records FROM restaurant_sales GROUP BY restaurant_id,month HAVING COUNT(*)>1;
