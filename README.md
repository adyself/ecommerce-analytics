E-Commerce Analytics (ETL + Dashboard)

Учебный проект по построению аналитической системы для интернет-магазина.
Включает полный ETL-конвейер, генерацию данных, витрины и Streamlit-дашборд.

Возможности
- Генерация синтетических данных (заказы, клиенты, товары)
- Полный ETL-процесс: Extract → Transform → Load
- Создание витрин (daily_metrics, funnel, cohorts и др.)
- Streamlit-дашборд: KPI Overview, воронка, когортный анализ, сегментация, заказы
- Контейнеризация через Docker


Запуск
1. Создать файл .env:
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=ecomm
   POSTGRES_PORT=5432

2. Запуск контейнеров:
   docker compose up -d

3. Запуск ETL:
   docker compose run --rm etl

4. Dashboard:
   http://localhost:8501
