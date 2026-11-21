SELECT
    r.city,
    COUNT(*) AS total_orders,
    SUM(o.sales_amount) AS total_revenue,
    ROUND(AVG(o.sales_amount), 2) AS avg_order_value
FROM orders o
JOIN restaurants r ON o.r_id = r.id
GROUP BY r.city
ORDER BY total_revenue DESC
LIMIT 10;