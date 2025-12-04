from src.utils.db import engine
import pandas as pd

def write_table(df: pd.DataFrame, table_name: str, if_exists='append'):
    df.to_sql(table_name, con=engine, if_exists=if_exists, index=False, method='multi')

def load_customers(df):
    write_table(df, 'customers', if_exists='replace')

def load_products(df):
    write_table(df, 'products', if_exists='replace')

def load_orders(df):
    write_table(df, 'orders', if_exists='append')

def load_order_items(df):
    write_table(df, 'order_items', if_exists='append')

def load_events(df):
    write_table(df, 'events', if_exists='append')

