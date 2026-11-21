SELECT
    u.occupation,
    u."Marital Status" AS marital_status,
    COUNT(*) AS total_orders,
    SUM(o.sales_amount) AS total_revenue,
    ROUND(AVG(o.sales_amount), 2) AS avg_order_value
FROM orders o
JOIN users u ON o.user_id = u.user_id
GROUP BY u.occupation, u."Marital Status"
ORDER BY total_revenue DESC
LIMIT 5;