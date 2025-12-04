-- daily_metrics
CREATE OR REPLACE VIEW daily_metrics AS
SELECT
  DATE(order_date) AS dt,
  COUNT(DISTINCT order_id) AS orders_count,
  SUM(total) AS revenue,
  CASE WHEN COUNT(DISTINCT order_id) = 0 THEN 0 ELSE SUM(total)::numeric / COUNT(DISTINCT order_id) END AS aov
FROM orders
GROUP BY DATE(order_date)
ORDER BY dt;

-- funnel per session
CREATE OR REPLACE VIEW funnel_by_session AS
WITH s AS (
  SELECT session_id,
    MAX(CASE WHEN event_type='product_view' THEN 1 ELSE 0 END) AS product_view,
    MAX(CASE WHEN event_type='add_to_cart' THEN 1 ELSE 0 END) AS add_to_cart,
    MAX(CASE WHEN event_type='checkout' THEN 1 ELSE 0 END) AS checkout,
    MAX(CASE WHEN event_type='purchase' THEN 1 ELSE 0 END) AS purchase
  FROM events
  GROUP BY session_id
)
SELECT
  SUM(product_view) as product_views,
  SUM(add_to_cart) as add_to_carts,
  SUM(checkout) as checkouts,
  SUM(purchase) as purchases,
  (SUM(add_to_cart)::float / NULLIF(SUM(product_view),0)) as conv_to_cart,
  (SUM(checkout)::float / NULLIF(SUM(add_to_cart),0)) as conv_to_checkout,
  (SUM(purchase)::float / NULLIF(SUM(checkout),0)) as conv_to_purchase
FROM s;

-- weekly cohort retention
CREATE OR REPLACE VIEW weekly_cohort AS
WITH first_order AS (
  SELECT customer_id, MIN(DATE(order_date)) AS first_order_date
  FROM orders
  GROUP BY customer_id
), orders_with_cohort AS (
  SELECT o.customer_id,
         DATE(o.order_date) AS order_date,
         EXTRACT(WEEK FROM o.order_date)::int AS order_week,
         DATE_TRUNC('week', fo.first_order_date)::date AS cohort_week
  FROM orders o
  JOIN first_order fo USING (customer_id)
)
SELECT cohort_week, order_week, COUNT(DISTINCT customer_id) AS active_customers
FROM orders_with_cohort
GROUP BY cohort_week, order_week
ORDER BY cohort_week, order_week;

-- simple LTV per customer for 30 days
CREATE OR REPLACE VIEW user_ltv_30 AS
WITH first_order AS (
  SELECT customer_id, MIN(order_date) AS first_order_date
  FROM orders
  GROUP BY customer_id
)
SELECT o.customer_id,
       SUM(o.total) AS total_revenue,
       MIN(o.order_date) AS first_order_date,
       SUM(CASE WHEN o.order_date <= fo.first_order_date + INTERVAL '30 days' THEN o.total ELSE 0 END) AS revenue_30d
FROM orders o
JOIN first_order fo ON o.customer_id = fo.customer_id
GROUP BY o.customer_id, fo.first_order_date;
