import click
from pathlib import Path
import os

from src.etl.extract import load_csv
from src.etl.transform import (
    transform_customers,
    transform_products,
    transform_orders,
    transform_events,
)
from src.etl.load import (
    load_customers,
    load_products,
    load_orders,
    load_order_items,
    load_events,
)


@click.command()
@click.option('--stage', default='all', help='stage to run: extract, transform, load, all')
def main(stage: str):
    # Корень проекта: .../ecommerce-analytics
    project_root = Path(__file__).resolve().parents[2]

    # Папка с сырыми данными
    base = project_root / "data" / "raw"

    # Если raw пуст — генерируем синтетические данные
    if not base.exists() or not any(base.iterdir()):
        gen = project_root / "data" / "synthetic" / "generate_data.py"
        if gen.exists():
            print("No raw data found — generating synthetic data")
            os.system(f"python {gen}")
        else:
            print("No data found. Please add raw CSVs to data/raw")
            return

    print("=== EXTRACT ===")
    customers = load_csv('customers.csv')
    products = load_csv('products.csv')
    orders_raw = load_csv('orders.csv')

    order_items_exists = (base / 'order_items.csv').exists()
    if order_items_exists:
        order_items_raw = load_csv('order_items.csv')
        orders_df = orders_raw.merge(order_items_raw, on='order_id', how='left')
    else:
        orders_df = orders_raw

    try:
        events = load_csv('events.csv')
    except FileNotFoundError:
        events = None

    print("=== TRANSFORM ===")
    customers_t = transform_customers(customers)
    products_t = transform_products(products)
    orders_t, order_items_t = transform_orders(orders_df)
    events_t = transform_events(events) if events is not None else None

    if stage in ['load', 'all']:
        print("=== LOAD ===")
        load_customers(customers_t)
        load_products(products_t)
        load_orders(orders_t)
        load_order_items(order_items_t)
        if events_t is not None:
            load_events(events_t)
        print("=== DONE LOADING ===")


if __name__ == "__main__":
    main()
