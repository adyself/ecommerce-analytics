import pandas as pd

def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['signup_date'] = pd.to_datetime(df['signup_date']).dt.date
    df['country'] = df['country'].fillna('Unknown')
    df['customer_id'] = df['customer_id'].astype(str)
    return df[['customer_id','signup_date','country']]

def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    df['product_id'] = df['product_id'].astype(str)
    return df[['product_id','category','price']]

def transform_orders(df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    df = df.copy()
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['order_id'] = df['order_id'].astype(str)
    df['customer_id'] = df['customer_id'].astype(str)
    if 'quantity' in df.columns and 'price' in df.columns:
        df['total'] = df['price'] * df['quantity']
    else:
        df['total'] = pd.to_numeric(df.get('total', 0), errors='coerce').fillna(0)
    orders = df.groupby('order_id').agg({
        'customer_id':'first',
        'order_date':'min',
        'total':'sum'
    }).reset_index()
    order_items = df[['order_id','product_id','quantity','price']].copy()
    return orders, order_items

def transform_events(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['event_time'] = pd.to_datetime(df['event_time'])
    df['customer_id'] = df['customer_id'].astype(str)
    df['product_id'] = df['product_id'].astype(str)
    df['session_id'] = df['session_id'].astype(str)
    return df[['customer_id','event_time','event_type','product_id','session_id']]
