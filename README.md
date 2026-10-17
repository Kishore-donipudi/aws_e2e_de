# AWS Data Engineering Project

An end-to-end data engineering pipeline built on **AWS S3** and **Databricks (Lakehouse)** — from raw CSV ingestion on S3, through a medallion (multi-hop) Lakeflow pipeline, to a live dashboard embedded in a public **Streamlit** app.

- [Pipeline-Graph](#lakeflow-declarative-pipelines)

- [LDP](#lakeflow-job)

- [Live-Dashboard-Recording](#live-dashboard-recording)

- [App-Deployment-Setup](#app-setup)

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
aws_e2e_de/
├── Data_ingestion/                     # Ingestion notebooks
│   ├── aws_manual_ingestion.ipynb      # Manual S3 → UC Volume download with boto3
│   └── aws_files_cleaning.ipynb        # Registering & cleaning the raw files
├── aws-pipeline/                        # Lakeflow SDP sources (medallion architecture)
│   ├── raw_tables.py                   # Bronze — raw streaming tables (Auto Loader)
│   ├── silver_tables.py                # Silver — cleaned and validated tables
│   └── gold_tables.py                  # Gold — business-level aggregates
├── app/                                # Streamlit app (Databricks App)
│   ├── app.py                          # App embedding the live dashboard
│   ├── app.yaml / manifest.yaml        # Databricks App configuration
│   └── requirements.txt
└── README.md                           # This file
```

## Dashboard & App

* **Food Delivery Analytics** — AI/BI dashboard built on the gold tables (Overview, Delivery Agents, Restaurants, Customers & Locations)
* `app/` — Streamlit app deployed as a Databricks App, publicly serving the embedded live dashboard


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
## LakeFlow-Declarative-Pipelines

<img width="1622" height="800" alt="image" src="https://github.com/user-attachments/assets/4934993a-0be6-4aa5-9e0a-c35d2a3f8680" />

## LakeFlow-Job
<img width="1622" height="807" alt="Screenshot 2026-10-16 214721" src="https://github.com/user-attachments/assets/a92366f2-a6f4-41f7-a274-3ec0654895d1" />

## Live-Dashboard-Recording

https://github.com/user-attachments/assets/5fdba6ca-845d-4fe5-b6c9-3c635d8a90bb

## App-Setup

<img width="1901" height="871" alt="image" src="https://github.com/user-attachments/assets/678b5f94-3214-4fd9-b629-989d8328b6eb" />

This is My Linkedin profile - Yet to update !!! :)  [Linkedin](https://www.linkedin.com/in/kishore-donipudi-2a9009307/) <br>
This is My professional Mail-Id  - kishoredonipudi921@gmail.com
