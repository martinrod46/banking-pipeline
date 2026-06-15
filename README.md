# 🏦 Banking Data Pipeline

End-to-end real-time data pipeline that captures banking transactions from PostgreSQL, streams changes through Kafka, orchestrates data movement with Airflow, loads data into BigQuery, and transforms it into analytics-ready models using dbt.

---

## Architecture

```text
PostgreSQL
    ↓
Debezium (CDC)
    ↓
Apache Kafka
    ↓
Apache Airflow
    ↓
Google BigQuery
    ↓
dbt
```

---

## Project Overview

This project simulates a modern banking environment where transaction data is continuously generated and processed in real time.

The pipeline captures database changes using Change Data Capture (CDC), streams events through Kafka, loads data into BigQuery, and builds dimensional models for reporting and analytics.

---

## Tech Stack

| Layer | Technology |
|---------|------------|
| Source Database | PostgreSQL 15 |
| CDC | Debezium |
| Streaming Platform | Apache Kafka |
| Workflow Orchestration | Apache Airflow |
| Data Warehouse | Google BigQuery |
| Transformations | dbt |
| Containerization | Docker Compose |

---

## Data Layers

### Raw

Unmodified CDC events captured directly from PostgreSQL.

### Staging

Cleaned and standardized datasets used as the foundation for downstream transformations.

### Marts

Business-ready analytical models designed for reporting and dashboard consumption.

---

## Features

- Real-time Change Data Capture (CDC)
- Event-driven architecture using Kafka
- Automated data ingestion via Airflow
- SCD Type 2 customer history tracking
- Fraud detection and transaction monitoring marts
- Cloud-based analytics with BigQuery
- Fully containerized local development environment

---

## Project Structure

```text
banking-pipeline/
│
├── airflow/
│   └── dags/
│
├── postgres/
│   └── init.sql
│
├── data_generator/
│   └── generate.py
│
├── dbt/
│   └── banking_dbt/
│       └── models/
│           ├── staging/
│           └── marts/
│
├── docker-compose.yml
└── README.md
```

---

## Analytical Models

### mart_customer_summary

Customer-level KPIs including:

- Total transaction amount
- Transaction count
- Failed transaction count
- Average transaction value

### mart_fraud_summary

Fraud monitoring metrics including:

- High-risk transactions
- Transaction categories
- Amount thresholds
- Fraud indicators

---

## Quick Start

### Prerequisites

- Docker Desktop
- Python 3.10+
- Google Cloud Project
- BigQuery Dataset

### Run Locally

```bash
git clone https://github.com/yourusername/banking-pipeline.git

cd banking-pipeline

docker-compose up -d

python data_generator/generate.py

cd dbt/banking_dbt

dbt run
```

---

## Learning Objectives

This project demonstrates practical experience with:

- Change Data Capture (CDC)
- Event Streaming
- Data Warehouse Design
- Dimensional Modeling
- SCD Type 2 Implementation
- Workflow Orchestration
- Containerized Data Platforms

---

## Future Improvements

- Streaming analytics with Spark Structured Streaming
- Data quality testing with Great Expectations
- CI/CD deployment pipeline
- Kafka schema management using Schema Registry
- Infrastructure as Code with Terraform

---

## Screenshots

### Airflow DAG

![Airflow DAG](images/airflow_dag.png)

### BigQuery Tables

![BigQuery Tables](images/bigquery_tables.png)

### Analytics Dashboard

![Analytics Dashboard](images/dashboard.png)

---

Built to showcase modern Data Engineering and Analytics Engineering practices.