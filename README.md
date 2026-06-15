# 🏦 Banking Data Pipeline

End-to-end real-time data pipeline that captures banking transactions from PostgreSQL, streams changes through Kafka, orchestrates data movement with Airflow, loads data into BigQuery, transforms data with dbt, and delivers business insights through Looker Studio dashboards.

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
    ↓
Looker Studio
```

---

## Project Overview

This project simulates a modern banking environment where transaction data is continuously generated and processed in real time.

The pipeline captures database changes using Change Data Capture (CDC), streams events through Kafka, loads data into BigQuery, transforms raw data into analytics-ready models with dbt, and exposes business insights through interactive dashboards in Looker Studio.

---

## Tech Stack

| Layer                  | Technology      |
| ---------------------- | --------------- |
| Source Database        | PostgreSQL 15   |
| CDC                    | Debezium        |
| Streaming Platform     | Apache Kafka    |
| Workflow Orchestration | Apache Airflow  |
| Data Warehouse         | Google BigQuery |
| Transformations        | dbt             |
| BI & Reporting         | Looker Studio   |
| Containerization       | Docker Compose  |

---

## Data Layers

### Raw

Unmodified CDC events captured directly from PostgreSQL.

### Staging

Cleaned and standardized datasets used as the foundation for downstream transformations.

### Marts

Business-ready analytical models optimized for reporting and dashboard consumption.

---

## Features

* Real-time Change Data Capture (CDC) using Debezium
* Event-driven architecture powered by Kafka
* Automated data ingestion and orchestration with Airflow
* SCD Type 2 customer history tracking
* Fraud detection and transaction monitoring marts
* Analytics-ready dimensional models built with dbt
* Cloud-based analytics using BigQuery
* Interactive dashboards built in Looker Studio
* Fully containerized local development environment

---

## Project Structure

```text
banking-pipeline/
│
├── airflow/
│   └── dags/
│       └── banking_pipeline_dag.py
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

* Total transaction amount
* Transaction count
* Failed transaction count
* Average transaction value

### mart_fraud_summary

Fraud monitoring metrics including:

* High-risk transactions
* Transaction categories
* Amount thresholds
* Fraud indicators

---

## Reporting Layer

Business-facing dashboards are built in Looker Studio using curated dbt models stored in BigQuery.

### Example Dashboards

* Customer Performance Overview
* Transaction Monitoring Dashboard
* Fraud Detection Dashboard
* Banking Operations KPI Dashboard

---

## Quick Start

### Prerequisites

* Docker Desktop
* Python 3.10+
* Google Cloud Project
* BigQuery Dataset

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

## Skills Demonstrated

* Change Data Capture (CDC) with Debezium
* Event Streaming with Kafka
* Workflow Orchestration with Airflow
* BigQuery Data Warehousing
* Dimensional Modeling
* SCD Type 2 Implementation
* dbt Data Transformations
* Dashboard Development with Looker Studio
* Docker-Based Deployment
* End-to-End Analytics Engineering

---

## Future Improvements

* Streaming analytics with Spark Structured Streaming
* Data quality testing with Great Expectations
* CI/CD deployment pipeline
* Kafka Schema Registry integration
* Infrastructure as Code with Terraform
* Automated monitoring and alerting

---

## Screenshots

### Airflow DAG

![Airflow DAG](images/airflow_dag.png)

### BigQuery Tables

![BigQuery Tables](images/bigquery_tables.png)

### Looker Studio Dashboard

![Looker Studio Dashboard](images/looker_dashboard.png)

---

Built to showcase modern Data Engineering and Analytics Engineering practices, from data ingestion to business intelligence.
