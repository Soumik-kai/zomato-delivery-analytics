WITH MonthlyRevenue AS (
    SELECT
        TO_CHAR(order_date::DATE, 'YYYY-MM') AS order_month,
        SUM(sales_amount) AS monthly_revenue
    FROM orders
    GROUP BY order_month
)
SELECT
    order_month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY order_month) AS prev_month_revenue,
    ROUND(
        100.0 * (monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY order_month))
        / NULLIF(LAG(monthly_revenue) OVER (ORDER BY order_month), 0),
        2
    ) AS mom_growth_pct
FROM MonthlyRevenue
ORDER BY order_month ASC
LIMIT 5;