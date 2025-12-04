E-commerce Analytics (ETL + Dashboard)

Проект для демонстрации аналитического пайплайна: генерация данных → ETL → PostgreSQL → Streamlit-дашборд.

Стек

-Python
-PostgreSQL (Docker)
-SQLAlchemy + Pandas
-Streamlit
-Docker Compose

Возможности

Генерация синтетических данных (customers, products, orders, events).

ETL: extract → transform → load в PostgreSQL.

Дашборд с аналитикой:

-KPI (revenue, AOV, orders)
-Воронка (session funnel)
-Когорты
-RFM-сегментация
-Последние заказы

Запуск проекта
1. Запуск БД + дашборда
docker compose up -d

2. Запуск ETL
docker compose run --rm etl


Данные загрузятся в PostgreSQL автоматически.

3. Дашборд

Открой в браузере:

http://localhost:8501

Структура
src/
  etl/
  dashboard/
  utils/
data/
docker-compose.yml
Dockerfile
README.md

Описание

Проект создан как демонстрация навыков Data Engineering + Analytics: построение витрин, метрик и визуализации данных.