SELECT
    f.veg_or_non_veg AS order_type,
    COUNT(*) AS total_orders,
    SUM(o.sales_amount) AS total_revenue,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS order_share_pct
FROM orders o
JOIN menu m ON o.r_id = m.r_id
JOIN food f ON m.f_id = f.f_id
GROUP BY f.veg_or_non_veg
ORDER BY total_orders DESC;