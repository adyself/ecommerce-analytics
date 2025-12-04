from src.etl.extract import load_csv
from src.etl.transform import transform_customers
from src.etl.load import load_customers

def run_etl():
    customers = load_csv('customers.csv')
    customers_t = transform_customers(customers)
    load_customers(customers_t)
    print("ETL for customers finished.")

if __name__ == "__main__":
    run_etl()
