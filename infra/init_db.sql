CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    signup_date DATE,
    country TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    category TEXT,
    price NUMERIC
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT REFERENCES customers(customer_id),
    order_date TIMESTAMP,
    total NUMERIC
);

CREATE TABLE IF NOT EXISTS order_items (
    item_id SERIAL PRIMARY KEY,
    order_id TEXT REFERENCES orders(order_id),
    product_id TEXT REFERENCES products(product_id),
    quantity INT,
    price NUMERIC
);

CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    customer_id TEXT,
    event_time TIMESTAMP,
    event_type TEXT,
    product_id TEXT,
    session_id TEXT
);


