# ETL articles Extract from Database, Transform and Load into Bigquery
This project is ETL project to extract from postgresql, transform and load to bigquery

## Note
- This ETL extract data from database and save it into CSV
- Transform to make sure the data type is correct
- And then Load into BigQuery (make sure already has Table in BigQuery
  
## Tools and Technologies
Database: PostgreSQL (SQL database)
Data Warehouse: Google BigQuery
ETL Tool: Apache Airflow
Scripting Language: Python (for data extraction and transformation)

## Step
1. Extract: Extract data from the PostgreSQL database.
2. Transform: Transform to make sure right data type for the data warehouse.
3. Load: Insert the transformed data into Google BigQuery

## Preparation
- **Clone repo** :
  ```
  # Clone
  git clone https://github.com/farizaarifah/etl_articles.git
  ```
- **Initialize Data source in postgresql**
  - in folder queries, run `create_table.sql` to create articles table
  - and then run `insert_data.sql` to insert dummy data

- **Docker**:
  ```docker compose up```
  
- **Run airflow DAG in docker**
  with name `etl_articles` DAG. this DAG run every hour

