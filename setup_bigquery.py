from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-credentials.json"

client = bigquery.Client(project="banking-pipeline-499102")

# Create dataset
dataset_id = "banking-pipeline-499102.banking_raw"
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"

dataset = client.create_dataset(dataset, exists_ok=True)
print(f"Dataset created: {dataset.dataset_id}")

# Create tables
tables = {
    "customers": [
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
    ],
    "accounts": [
        bigquery.SchemaField("account_id", "INTEGER"),
        bigquery.SchemaField("customer_id", "INTEGER"),
        bigquery.SchemaField("account_type", "STRING"),
        bigquery.SchemaField("account_status", "STRING"),
        bigquery.SchemaField("balance", "FLOAT"),
        bigquery.SchemaField("currency", "STRING"),
        bigquery.SchemaField("opened_at", "TIMESTAMP"),
        bigquery.SchemaField("updated_at", "TIMESTAMP"),
    ],
    "transactions": [
        bigquery.SchemaField("transaction_id", "INTEGER"),
        bigquery.SchemaField("account_id", "INTEGER"),
        bigquery.SchemaField("transaction_type", "STRING"),
        bigquery.SchemaField("amount", "FLOAT"),
        bigquery.SchemaField("currency", "STRING"),
        bigquery.SchemaField("description", "STRING"),
        bigquery.SchemaField("status", "STRING"),
        bigquery.SchemaField("created_at", "TIMESTAMP"),
    ],
    "fraud_flags": [
        bigquery.SchemaField("flag_id", "INTEGER"),
        bigquery.SchemaField("transaction_id", "INTEGER"),
        bigquery.SchemaField("flag_reason", "STRING"),
        bigquery.SchemaField("flagged_at", "TIMESTAMP"),
        bigquery.SchemaField("resolved", "BOOLEAN"),
    ],
}

for table_name, schema in tables.items():
    table_id = f"banking-pipeline-499102.banking_raw.{table_name}"
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table, exists_ok=True)
    print(f"  [OK] Table created: {table_name}")

print("\nBigQuery setup complete!")