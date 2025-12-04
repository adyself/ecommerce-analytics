import pandas as pd
from src.etl.transform import transform_orders

def test_transform_orders_basic():
    df = pd.DataFrame([
        {"order_id":"o1","customer_id":"c1","order_date":"2023-01-01 10:00:00","product_id":"p1","quantity":2,"price":10.0},
        {"order_id":"o1","customer_id":"c1","order_date":"2023-01-01 10:01:00","product_id":"p2","quantity":1,"price":5.0},
        {"order_id":"o2","customer_id":"c2","order_date":"2023-01-02 12:00:00","product_id":"p1","quantity":1,"price":10.0},
    ])
    orders, items = transform_orders(df)
    assert len(orders) == 2
    total_o1 = orders.loc[orders['order_id']=='o1','total'].iloc[0]
    assert total_o1 == 25.0
    assert len(items) == 3
