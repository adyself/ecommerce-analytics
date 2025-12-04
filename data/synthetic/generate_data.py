import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

# Папка проекта: .../ecommerce-analytics
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)

NUM_CUSTOMERS = 100
NUM_PRODUCTS = 30
NUM_ORDERS = 300
MAX_ITEMS_PER_ORDER = 5
NUM_EVENTS = 1000

COUNTRIES = ["US", "DE", "FR", "GB", "RU", "NL", "ES", "IT"]
CATEGORIES = ["electronics", "clothes", "books", "toys", "home"]
EVENT_TYPES = ["product_view", "add_to_cart", "checkout", "purchase"]

start_date = datetime(2024, 1, 1)


def gen_customers():
    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        cid = f"C{i:04d}"
        signup_offset = random.randint(0, 200)
        signup_date = (start_date + timedelta(days=signup_offset)).date()
        country = random.choice(COUNTRIES)
        customers.append((cid, signup_date.isoformat(), country))
    return customers


def gen_products():
    products = []
    for i in range(1, NUM_PRODUCTS + 1):
        pid = f"P{i:04d}"
        category = random.choice(CATEGORIES)
        price = round(random.uniform(5, 200), 2)
        products.append((pid, category, price))
    return products


def gen_orders_and_items(customers, products):
    orders = []
    order_items = []

    for i in range(1, NUM_ORDERS + 1):
        oid = f"O{i:05d}"
        customer_id = random.choice(customers)[0]
        order_date = start_date + timedelta(days=random.randint(0, 200),
                                            hours=random.randint(0, 23),
                                            minutes=random.randint(0, 59))
        num_items = random.randint(1, MAX_ITEMS_PER_ORDER)
        total = 0.0

        for _ in range(num_items):
            product_id, _, price = random.choice(products)
            quantity = random.randint(1, 3)
            line_total = price * quantity
            total += line_total
            order_items.append((oid, product_id, quantity, price))

        orders.append((oid, customer_id, order_date.isoformat(sep=" "), round(total, 2)))

    return orders, order_items


def gen_events(customers, products):
    events = []
    for i in range(NUM_EVENTS):
        customer_id = random.choice(customers)[0]
        product_id = random.choice(products)[0]
        event_time = start_date + timedelta(days=random.randint(0, 200),
                                            hours=random.randint(0, 23),
                                            minutes=random.randint(0, 59))
        event_type = random.choices(
            EVENT_TYPES,
            weights=[0.6, 0.2, 0.1, 0.1],
        )[0]
        session_id = f"S{random.randint(1, 500):05d}"
        events.append((customer_id, event_time.isoformat(sep=" "), event_type, product_id, session_id))
    return events


def write_csv(path, header, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    print(f"Generating synthetic data into {RAW_DIR}")

    customers = gen_customers()
    products = gen_products()
    orders, order_items = gen_orders_and_items(customers, products)
    events = gen_events(customers, products)

    write_csv(RAW_DIR / "customers.csv", ["customer_id", "signup_date", "country"], customers)
    write_csv(RAW_DIR / "products.csv", ["product_id", "category", "price"], products)
    write_csv(RAW_DIR / "orders.csv", ["order_id", "customer_id", "order_date", "total"], orders)
    write_csv(RAW_DIR / "order_items.csv", ["order_id", "product_id", "quantity", "price"], order_items)
    write_csv(RAW_DIR / "events.csv", ["customer_id", "event_time", "event_type", "product_id", "session_id"], events)

    print("Done generating synthetic data.")


if __name__ == "__main__":
    main()
