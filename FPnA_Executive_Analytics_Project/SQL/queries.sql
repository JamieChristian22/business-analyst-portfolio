-- Reference query pack. Run scripts/run_analysis.py to export each query separately.

-- Q01: Finance controls
SELECT scenario,account_category,COUNT(*) records,SUM(amount) amount FROM finance GROUP BY scenario,account_category ORDER BY scenario,account_category;

-- Q02: Monthly actual budget bridge
WITH m AS (SELECT month,SUM(CASE WHEN scenario='Actual' AND account_category='Revenue' THEN amount ELSE 0 END) revenue_actual,SUM(CASE WHEN scenario='Budget' AND account_category='Revenue' THEN amount ELSE 0 END) revenue_budget,SUM(CASE WHEN scenario='Actual' AND account_category='COGS' THEN amount ELSE 0 END) cogs_actual,SUM(CASE WHEN scenario='Actual' AND account_category='OpEx' THEN amount ELSE 0 END) opex_actual FROM finance GROUP BY month) SELECT *,revenue_actual-revenue_budget revenue_variance,1.0*(revenue_actual-revenue_budget)/NULLIF(revenue_budget,0) revenue_variance_rate,revenue_actual-cogs_actual-opex_actual operating_income,1.0*(revenue_actual-cogs_actual)/NULLIF(revenue_actual,0) gross_margin FROM m ORDER BY month;

-- Q03: Department revenue variance
WITH d AS (SELECT department,SUM(CASE WHEN scenario='Actual' AND account_category='Revenue' THEN amount ELSE 0 END) revenue_actual,SUM(CASE WHEN scenario='Budget' AND account_category='Revenue' THEN amount ELSE 0 END) revenue_budget FROM finance GROUP BY department) SELECT *,revenue_actual-revenue_budget revenue_variance,1.0*(revenue_actual-revenue_budget)/NULLIF(revenue_budget,0) revenue_variance_rate FROM d ORDER BY revenue_variance,department;

-- Q04: Fact versus dashboard reconciliation
WITH f AS (SELECT month,department,SUM(amount) fact_revenue FROM finance WHERE scenario='Actual' AND account_category='Revenue' GROUP BY month,department),k AS (SELECT month,department FROM f UNION SELECT month,department FROM finance_summary) SELECT k.month,k.department,f.fact_revenue,s.revenue_actual dashboard_revenue,f.fact_revenue-s.revenue_actual difference,CASE WHEN f.fact_revenue IS NULL OR s.revenue_actual IS NULL THEN 'MISSING SOURCE' WHEN ABS(f.fact_revenue-s.revenue_actual)>0.01 THEN 'UNRESOLVED DIFFERENCE' ELSE 'MATCH' END disposition FROM k LEFT JOIN f ON k.month=f.month AND k.department=f.department LEFT JOIN finance_summary s ON k.month=s.month AND k.department=s.department ORDER BY k.month,k.department;

-- Q05: Budget completeness
SELECT month,department,account_category,SUM(CASE WHEN scenario='Actual' THEN 1 ELSE 0 END) actual_records,SUM(CASE WHEN scenario='Budget' THEN 1 ELSE 0 END) budget_records FROM finance GROUP BY month,department,account_category HAVING SUM(CASE WHEN scenario='Actual' THEN 1 ELSE 0 END)=0 OR SUM(CASE WHEN scenario='Budget' THEN 1 ELSE 0 END)=0;
