E-Commerce Analytics — End-to-End Data Pipeline (ETL + Dashboard)

Полный учебный проект Data Engineer / Analyst, включающий:

автоматическую генерацию синтетических e-commerce данных

полноценный ETL-конвейер (extract → transform → load)

PostgreSQL как DWH

Metabase-подобный Streamlit-дашборд

Docker-оркестрацию

SQL модели (KPI, воронка, когортный анализ, LTV)

Проект полностью контейнеризирован и запускается в один командой.

 Стек

Backend / ETL: Python, Pandas, SQLAlchemy, psycopg
Database: PostgreSQL
Dashboard: Streamlit
Containerization: Docker, Docker Compose
Other: Click CLI, synthetic data generator

 Структура проекта
ecommerce-analytics/
│
├── src/
│   ├── etl/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   ├── load.py
│   │   └── run.py                # главный ETL скрипт
│   ├── dashboard/
│   │   └── app.py                # Streamlit дашборд
│   └── utils/
│       └── db.py                 # engine + подключение к БД
│
├── infra/
│   └── sql/                      # SQL модели: daily_metrics, funnel, cohort, ltv …
│
├── data/
│   └── synthetic/                # генератор данных (если нет сырых файлов)
│
├── notebooks/                    # EDA, Cohort, Funnel (Jupyter)
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md

⚙️ Установка и запуск
1️⃣ Клонировать репозиторий
git clone https://github.com/adyself/ecommerce-analytics.git
cd ecommerce-analytics

2️⃣ Создать .env
cp .env.example .env


При необходимости поменяйте порт и креды.

3️⃣ Запустить инфраструктуру (Postgres + ETL + Dashboard)
docker compose up -d --build


Это поднимет:

Postgres (с таблицами и SQL-видами)

ETL-контейнер, который загрузит данные

Streamlit-дашборд

4️⃣ (Опционально) Прогнать ETL вручную
docker compose run --rm etl

5️⃣ Открыть дашборд

Перейдите в браузере:

http://localhost:8501

 Дашборд

Включает ключевые разделы:

Overview: выручка, AOV, количество заказов, графики

Funnel: просмотры → корзина → checkout → покупка

Cohorts: когортный retention по неделям

Segments: RFM сегментация (recency, frequency, monetary)

Orders: последние 200 заказов

Скриншоты (можешь добавить свои 👇):

![Dashboard Screenshot](docs/dashboard.png)

 SQL модели (в папке /infra/sql)

daily_metrics.sql — дневные метрики KPI

funnel_by_session.sql — воронка конверсии

weekly_cohort.sql — когортный анализ

user_ltv_30.sql — LTV (30 дней)

🔧 ETL Pipeline

Extract
Загружает CSV из data/raw или генерирует синтетические данные.

Transform
Очистка, нормализация, подготовка таблиц:
customers, products, orders, order_items, events

Load
Запись в PostgreSQL.

Запуск:

python -m src.etl.run --stage all

❗ Возможные проблемы

Если БД уже содержит данные, ETL может выбросить ошибку duplicate key.
Решения:

docker compose down -v       # удалить volume и очистить базу
docker compose up --build

 Контакты

Если хотите обсудить проект, улучшения или вопросы — пишите 🙂
GitHub: https://github.com/adyself
