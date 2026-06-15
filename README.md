# Banking Data Pipeline 🏦

A streaming data pipeline built entirely with free and open-source tools.

<br>

## Architecture

```
PostgreSQL → Debezium → Kafka → Airflow → BigQuery → dbt
```
<br>

## What it does?

Simulates a real banking system with live transaction data, streams every database change in real time using CDC (Change Data Capture), loads it into a cloud data warehouse, and transforms it into business-ready models.

<br>

## Tech Stack

| Layer | Tool |
|---|---|
| Source Database | PostgreSQL 15 |
| Change Data Capture | Debezium |
| Message Streaming | Apache Kafka |
| Orchestration | Apache Airflow |
| Data Warehouse | Google BigQuery |
| Transformations | dbt |
| Infrastructure | Docker + Docker Compose |

<br>

## Pipeline Layers

- **Raw** — direct CDC events from PostgreSQL
- **Staging** — cleaned and validated data
- **Marts** — business-ready models including customer summaries and fraud analysis

<br>

## Key Features

- Real-time CDC streaming with Debezium watching every INSERT, UPDATE and DELETE
- Automated hourly loads into BigQuery via Airflow DAGs
- SCD2 customer tracking — full history of address and contact changes
- Fraud detection summary by transaction type and amount category
- Fully containerized — runs with a single `docker-compose up -d`

<br>

## Quick Start

**Prerequisites:** Docker Desktop, Python 3.10+, Google Cloud account

```bash
# Clone the repo
git clone https://github.com/yourusername/banking-pipeline.git
cd banking-pipeline

# Start all containers
docker-compose up -d

# Generate fake banking data
python data_generator/generate.py

# Run dbt transformations
cd dbt/banking_dbt
dbt run
```
<br>

## Project Structure

```
banking-pipeline/
├── docker-compose.yml                   # All containers defined here
├── postgres/
│   └── init.sql                         # Banking schema
├── data_generator/
│   └── generate.py                      # Fake banking data simulator
├── airflow/
│   └── dags/
│       └── banking_pipeline_dag.py      # PostgreSQL → BigQuery DAG
└── dbt/
    └── banking_dbt/
        └── models/
            ├── staging/                 # Cleaned source data
            └── marts/                  # Business models
```
<br>

## Data Models

**mart_customer_summary** — total spend, transaction count, and failed transactions per customer

**mart_fraud_summary** — fraud flags broken down by transaction type and amount category

<br>

## Author

Luis Martín Rodríguez Arias — Guadalajara, Mexico

