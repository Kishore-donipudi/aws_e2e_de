# AWS Data Engineering Project

An end-to-end data engineering pipeline built on **AWS S3** and **Databricks (Lakehouse)** — from raw CSV ingestion on S3, through a medallion (multi-hop) Lakeflow pipeline, to a live dashboard embedded in a public **Streamlit** app.

- [Recording](#live-dashboard-recording)
## Project Steps

### 1. Store datasets in AWS S3
Uploaded the datasets (CSV files) to an AWS S3 bucket and made the bucket public so the files are directly reachable.

### 2. Configure AWS credentials in Databricks
In the Databricks console, configured the AWS access key ID and secret access key for the account.

### 3. Download files into UC Volumes manually (boto3)
Used **boto3** to list the files in the S3 bucket and manually download the CSV files into **Unity Catalog Volumes**.

### 4. Lakeflow Connect data ingestion via external location
Linked the AWS account in Databricks and granted Databricks permission to access the S3 bucket for **12 hours** using an **external location**. Using that external location, ingested the data and created a **managed table** in Unity Catalog.

### 5. Lakeflow pipeline — medallion (multi-hop) architecture
Created a **Lakeflow Spark Declarative Pipeline** with a multi-hop architecture:

* **Bronze** (`aws-pipeline/raw_tables.py`) — raw ingestion of the source CSV files (streaming tables via Auto Loader)
* **Silver** (`aws-pipeline/silver_tables.py`) — cleaned and validated data
* **Gold** (`aws-pipeline/gold_tables.py`) — business-level aggregates ready for analytics

### 6. Dashboard on gold tables
Built a **Databricks AI/BI dashboard** on top of the gold tables.

### 7. Lakeflow job (DLT pipeline + dashboard, 3 retries)
Created a **Lakeflow Job** that runs the DLT pipeline and then the dashboard task (which depends on the DLT pipeline), configured with **3 retries**.

### 8. Streamlit app with embedded live dashboard
Finally, created a **Streamlit** app and embedded the live dashboard in it, making it accessible to the public.

## Tech Stack

| Layer | Tools |
| --- | --- |
| Storage | AWS S3, Unity Catalog Volumes, Unity Catalog managed tables |
| Ingestion | boto3, external locations, Auto Loader |
| Transformation | Lakeflow Spark Declarative Pipeline (medallion architecture) |
| Orchestration | Lakeflow Jobs (DLT pipeline + dashboard, 3 retries) |
| Analytics / Serving | Databricks AI/BI dashboard, Streamlit app (public) |

## Project Structure

```
aws_data_engineering_project/
├── aws-pipeline/                  # Lakeflow SDP pipeline sources (medallion layers)
│   ├── raw_tables.py              # Bronze — raw streaming tables (Auto Loader)
│   ├── silver_tables.py           # Silver — cleaned and validated tables
│   └── gold_tables.py             # Gold — business-level aggregates
├── aws_manual_ingestion            # Notebook — manual S3 → UC Volume ingestion with boto3
├── aws_files_cleaning             # Notebook — cleaning the raw files
└── project_readme.md              # This file
```

## Related Workspace Assets

* **Food Delivery Analytics** — AI/BI dashboard built on the gold tables (workspace root)
* **streamlit-hello-world-app** — Streamlit app (`app.py`, `app.yaml`, `requirements.txt`) in `databricks_apps/` that embeds the live dashboard and makes it publicly accessible


## Live-Dashboard Recording

https://github.com/user-attachments/assets/5fdba6ca-845d-4fe5-b6c9-3c635d8a90bb

## Architecture Diagram

```text
┌──────────────────────────────────────────────┐
│                AWS S3 Bucket                 │
│                 s3://de-prj/                 │
│            csv_files/ json_files/            │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                 Boto3 Access                 │
│           AWS Key + Secret Config            │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│            Unity Catalog Volumes             │
│             Manual File Download             │
│              (Proof of Concept)              │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│              External Location               │
│             IAM Temporary Access             │
│             (12-hour permission)             │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│             Databricks Ingestion             │
│            Managed Table Creation            │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│     Lakeflow Spark Declarative Pipeline      │
│                                              │
│  ┌────────────┐  ┌────────────┐  ┌──────┐    │
│  │   Bronze   │─►│   Silver   │─►│ Gold │    │
│  │  Raw data  │  │Cleaned data│  │ KPIs │    │
│  └────────────┘  └────────────┘  └──────┘    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│          Databricks AI/BI Dashboard          │
│         KPI Visualizations / Reports         │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                 Lakeflow Job                 │
│       Pipeline + Dashboard (3 retries)       │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│            Streamlit Application             │
│           Embedded Live Dashboard            │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
            Public Dashboard Access
```
