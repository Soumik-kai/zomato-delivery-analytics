-- Query 3: Most ordered cuisines per country and city
-- Determines the popularity of cuisines by counting orders per country and city.
SELECT r.country, r.city, r.cuisine, COUNT(*) AS order_count
FROM orders o
JOIN restaurants r ON o.r_id = r.id
WHERE r.cuisine IS NOT NULL
GROUP BY r.country, r.city, r.cuisine
ORDER BY order_count DESC;