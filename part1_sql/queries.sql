-- Part 1: Meesho reseller business queries
-- Run against data/meesho_reseller.db

-- Q1. Monthly revenue by category
SELECT month,
       category,
       ROUND(SUM(quantity * unit_price), 2) AS revenue,
       COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END,
         category;

-- Q2. Region-wise total revenue and order count
SELECT r.region,
       ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
       COUNT(*) AS n_orders
FROM orders o
JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY revenue DESC;

-- Q3. Top resellers by total spend
SELECT r.reseller_id,
       r.reseller_name,
       ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

-- Q4a. Resellers who never placed an order
SELECT r.reseller_id, r.reseller_name, r.region
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;

-- Q4b. Demonstrate COUNT(*) vs COUNT(order_id) for RS024
SELECT r.reseller_id,
       r.reseller_name,
       COUNT(*) AS row_count,
       COUNT(o.order_id) AS order_id_count
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id, r.reseller_name;

-- Q5. June Delivered AOV
SELECT ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
