import streamlit as st
import pandas as pd
from src.utils.db import engine

st.set_page_config(page_title="E-Commerce Analytics", layout="wide")

def load_view(sql):
    return pd.read_sql(sql, con=engine)

st.title("E-Commerce Analytics — Demo (Middle project)")

st.sidebar.header("Панель")
page = st.sidebar.radio("Раздел", ["Overview", "Funnel", "Cohorts", "Segments", "Orders"])

if page == "Overview":
    st.header("Overview — KPI")
    df_daily = load_view("SELECT * FROM daily_metrics ORDER BY dt DESC")
    if not df_daily.empty:
        df_daily = df_daily.set_index('dt')
        last = df_daily.iloc[-1]
        st.metric("Последняя дата", str(df_daily.index.max()))
        col1, col2, col3 = st.columns(3)
        col1.metric("Последний revenue", f"{last['revenue']:.2f}")
        col2.metric("AOV", f"{last['aov']:.2f}")
        col3.metric("Orders", int(last['orders_count']))
        st.line_chart(df_daily['revenue'])
    else:
        st.info("Нет данных. Запустите ETL.")

elif page == "Funnel":
    st.header("Funnel by session")
    funnel = load_view("SELECT * FROM funnel_by_session")
    st.write(funnel.T)

elif page == "Cohorts":
    st.header("Weekly Cohorts (sample)")
    cohorts = load_view("SELECT * FROM weekly_cohort LIMIT 200")
    st.dataframe(cohorts)

elif page == "Segments":
    st.header("RFM / Segmentation (sample)")
    rfm_sql = """
    WITH last AS (
      SELECT customer_id, MAX(order_date) as last_order
      FROM orders
      GROUP BY customer_id
    ), freq AS (
      SELECT customer_id, COUNT(order_id) as freq
      FROM orders
      GROUP BY customer_id
    ), mon AS (
      SELECT customer_id, SUM(total) as monetary
      FROM orders
      GROUP BY customer_id
    )
    SELECT l.customer_id,
           (CURRENT_DATE - DATE(l.last_order)) as recency,
           f.freq,
           m.monetary
    FROM last l
    LEFT JOIN freq f ON l.customer_id = f.customer_id
    LEFT JOIN mon m ON l.customer_id = m.customer_id
    LIMIT 200
    """
    rfm = load_view(rfm_sql)
    st.dataframe(rfm)

elif page == "Orders":
    st.header("Recent Orders (sample)")
    orders = load_view("SELECT * FROM orders ORDER BY order_date DESC LIMIT 200")
    st.dataframe(orders)
