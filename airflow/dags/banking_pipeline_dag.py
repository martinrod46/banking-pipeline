from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import psycopg2
from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/opt/airflow/gcp-credentials.json"

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def load_customers():
    pg = psycopg2.connect(
        host="banking_postgres",
        port="5432",
        database="banking_db",
        user="banking_user",
        password="banking_pass"
    )
    cursor = pg.cursor()
    cursor.execute("SELECT * FROM customers;")
    rows = cursor.fetchall()
    cursor.close()
    pg.close()

    # Added empty rows guard — prevents crashing on empty tables
    if not rows:
        print("No rows to insert, skipping!")
        return

    client = bigquery.Client(project="banking-pipeline-499102")
    table_id = "banking-pipeline-499102.banking_raw.customers"

    # Added LoadJobConfig with schema — tells BigQuery exactly what data types to expect
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        schema=[
            bigquery.SchemaField("customer_id", "INTEGER"),
            bigquery.SchemaField("first_name", "STRING"),
            bigquery.SchemaField("last_name", "STRING"),
            bigquery.SchemaField("email", "STRING"),
            bigquery.SchemaField("phone", "STRING"),
            bigquery.SchemaField("address", "STRING"),
            bigquery.SchemaField("city", "STRING"),
            bigquery.SchemaField("country", "STRING"),
            bigquery.SchemaField("date_of_birth", "DATE"),
            bigquery.SchemaField("created_at", "TIMESTAMP"),
            bigquery.SchemaField("updated_at", "TIMESTAMP"),
        ]
    )

    bq_rows = []
    for row in rows:
        bq_rows.append({
            "customer_id":   row[0],
            "first_name":    row[1],
            "last_name":     row[2],
            "email":         row[3],
            "phone":         row[4],
            "address":       row[5],
            "city":          row[6],
            "country":       row[7],
            "date_of_birth": str(row[8]) if row[8] else None,
            "created_at":    str(row[9]) if row[9] else None,
            "updated_at":    str(row[10]) if row[10] else None,
        })

    job = client.load_table_from_json(bq_rows, table_id, job_config=job_config)
    job.result()
    print(f"Loaded {len(bq_rows)} customers into BigQuery!")

def load_transactions():
    pg = psycopg2.connect(
        host="banking_postgres",
        port="5432",
        database="banking_db",
        user="banking_user",
        password="banking_pass"
    )
    cursor = pg.cursor()
    cursor.execute("SELECT * FROM transactions;")
    rows = cursor.fetchall()
    cursor.close()
    pg.close()

    if not rows:
        print("No rows to insert, skipping!")
        return

    client = bigquery.Client(project="banking-pipeline-499102")
    table_id = "banking-pipeline-499102.banking_raw.transactions"

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        schema=[
            bigquery.SchemaField("transaction_id", "INTEGER"),
            bigquery.SchemaField("account_id", "INTEGER"),
            bigquery.SchemaField("transaction_type", "STRING"),
            bigquery.SchemaField("amount", "FLOAT"),
            bigquery.SchemaField("currency", "STRING"),
            bigquery.SchemaField("description", "STRING"),
            bigquery.SchemaField("status", "STRING"),
            bigquery.SchemaField("created_at", "TIMESTAMP"),
        ]
    )

    bq_rows = []
    for row in rows:
        bq_rows.append({
            "transaction_id":   row[0],
            "account_id":       row[1],
            "transaction_type": row[2],
            "amount":           float(row[3]) if row[3] else None,
            "currency":         row[4],
            "description":      row[5],
            "status":           row[6],
            "created_at":       str(row[7]) if row[7] else None,
        })

    job = client.load_table_from_json(bq_rows, table_id, job_config=job_config)
    job.result()
    print(f"Loaded {len(bq_rows)} transactions into BigQuery!")

def load_fraud_flags():
    pg = psycopg2.connect(
        host="banking_postgres",
        port="5432",
        database="banking_db",
        user="banking_user",
        password="banking_pass"
    )
    cursor = pg.cursor()
    cursor.execute("SELECT * FROM fraud_flags;")
    rows = cursor.fetchall()
    cursor.close()
    pg.close()

    if not rows:
        print("No rows to insert, skipping!")
        return

    client = bigquery.Client(project="banking-pipeline-499102")
    table_id = "banking-pipeline-499102.banking_raw.fraud_flags"

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        schema=[
            bigquery.SchemaField("flag_id", "INTEGER"),
            bigquery.SchemaField("transaction_id", "INTEGER"),
            bigquery.SchemaField("flag_reason", "STRING"),
            bigquery.SchemaField("flagged_at", "TIMESTAMP"),
            bigquery.SchemaField("resolved", "BOOLEAN"),
        ]
    )

    bq_rows = []
    for row in rows:
        bq_rows.append({
            "flag_id":        row[0],
            "transaction_id": row[1],
            "flag_reason":    row[2],
            "flagged_at":     str(row[3]) if row[3] else None,
            "resolved":       row[4],
        })

    job = client.load_table_from_json(bq_rows, table_id, job_config=job_config)
    job.result()
    print(f"Loaded {len(bq_rows)} fraud flags into BigQuery!")

with DAG(
    'banking_pipeline',
    default_args=default_args,
    description='Load banking data from PostgreSQL to BigQuery',
    schedule_interval='@hourly',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id='load_customers',
        python_callable=load_customers,
    )

    t2 = PythonOperator(
        task_id='load_transactions',
        python_callable=load_transactions,
    )

    t3 = PythonOperator(
        task_id='load_fraud_flags',
        python_callable=load_fraud_flags,
    )

    t1 >> t2 >> t3