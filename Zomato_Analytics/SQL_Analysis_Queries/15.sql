-- Query 15: Most popular cuisines across restaurant rating tiers
-- Identifies the most ordered cuisines categorized by restaurant rating (High, Medium, Low, Unrated).
SELECT
    CASE
        WHEN r.rating ~ '^[0-9]+(\.[0-9]+)?$' AND CAST(r.rating AS NUMERIC) >= 4.5 THEN 'High (4.5+)'
        WHEN r.rating ~ '^[0-9]+(\.[0-9]+)?$' AND CAST(r.rating AS NUMERIC) >= 3.5 THEN 'Medium (3.5-4.4)'
        WHEN r.rating ~ '^[0-9]+(\.[0-9]+)?$' AND CAST(r.rating AS NUMERIC) >= 0 THEN 'Low (<3.5)'
        ELSE 'Unrated'
    END AS rating_tier,
    r.cuisine,
    COUNT(*) AS total_orders
FROM orders o
JOIN restaurants r ON o.r_id = r.id
WHERE r.cuisine IS NOT NULL
GROUP BY rating_tier, r.cuisine
ORDER BY rating_tier, total_orders DESC;