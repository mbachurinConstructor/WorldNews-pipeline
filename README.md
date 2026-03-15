# WorldNews Pipeline

An automated, production-deployed data pipeline that ingests news articles from NewsAPI,
stores raw data in AWS S3, transforms it, and loads it into a PostgreSQL data warehouse.
Orchestrated with Apache Airflow and deployed with Docker Compose on a live VPS.

---

## Architecture

```
NewsAPI (3 categories × 100 articles)
        ↓
  Airflow DAG (every 12 hours)
        ↓
  Extract → raw JSON → S3 (raw/)
        ↓
  Transform → cleaned JSON → S3 (transformed/)
        ↓
  Load → PostgreSQL warehouse
        ↓
  Analytics SQL queries
```

---

## Pipeline

The DAG runs every 12 hours and executes 3 tasks in sequence:

1. **Extract** — fetches top headlines across `technology`, `business`, and `science`
   categories via NewsAPI. Adds `fetchedAt` timestamp and `category` tag to each article.
   Uploads raw JSON to S3 with ISO timestamp key (`raw/YYYY-MM-DDTHH:MM:SS.json`).

2. **Transform** — downloads latest raw file from S3. Flattens nested `source` object,
   normalizes timestamps to PostgreSQL-compatible format, replaces null fields with
   `"unknown"`, removes unused fields (`content`, `urlToImage`). Uploads cleaned JSON
   to S3 (`transformed/`).

3. **Load** — downloads latest transformed file from S3. Initializes DB schema if not
   exists. Inserts articles using `ON CONFLICT (url) DO NOTHING` to prevent duplicates
   across runs.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | Apache Airflow 2.9 (LocalExecutor) |
| Data Source | NewsAPI REST API |
| Raw Storage | AWS S3 (boto3) |
| Transformation | Python 3.12 |
| Data Warehouse | PostgreSQL 15 |
| Containerization | Docker Compose |
| Deployment | VPS (live, running 24/7) |

---

## Database Schema

```sql
CREATE TABLE articles (
    id            SERIAL PRIMARY KEY,
    author        TEXT,
    title         TEXT,
    description   TEXT,
    url           TEXT UNIQUE NOT NULL,   -- deduplication key
    category      TEXT,
    source_id     TEXT,
    source_name   TEXT,
    published_at  TIMESTAMP,
    fetched_at    TIMESTAMP
);
```

Deduplication is enforced at the database level via `UNIQUE` constraint on `url`,
with `ON CONFLICT DO NOTHING` in the insert logic.

---

## S3 Structure

```
s3://bucket-name/
├── raw/
│   ├── 2026-03-14T04:00:00.json
│   ├── 2026-03-14T16:00:00.json
│   └── ...
└── transformed/
    ├── 2026-03-14T04:00:01.json
    ├── 2026-03-14T16:00:01.json
    └── ...
```

Each pipeline run produces two timestamped files — one raw, one transformed.
The load step always picks the latest file in the `transformed/` prefix.

---

## Analytics Queries

```bash
bash bash_scripts/analytics.sh
```

| Query | Description |
|---|---|
| Top 10 sources | Which outlets publish most |
| Articles per category | Volume breakdown by topic |
| Top 10 authors | Most prolific authors (nulls excluded) |
| Latest 5 articles | Most recently published |

---

## Running Locally

### Prerequisites
- Docker Desktop
- AWS account with S3 bucket and IAM credentials
- NewsAPI key (free at newsapi.org)

### Setup

```bash
git clone https://github.com/mbachurinConstructor/WorldNews-pipeline
cd WorldNews-pipeline
nano .env   # fill in your credentials
bash bash_scripts/start.sh
```

Open Airflow UI at `http://localhost:8080` — login `admin` / `admin`

### Environment Variables

```
NEWS_API_KEY=
AWS_ACCESS_KEY=
AWS_SECRET_ACCESS_KEY=
AWS_BUCKET_NAME=
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

### Utility Scripts

| Script | Description |
|---|---|
| `bash_scripts/start.sh` | Start all services |
| `bash_scripts/stop.sh` | Stop all services |
| `bash_scripts/restart.sh` | Full nuke and restart |
| `bash_scripts/analytics.sh` | Run analytics queries |
| `bash_scripts/open_db_container_terminal.sh` | Open psql shell |
| `bash_scripts/nuke.sh` | Remove all containers, images, logs |

---

## Project Structure

```
WorldNews-pipeline/
├── dags/
│   └── news_pipeline_dag.py     # Airflow DAG definition
├── scripts/
│   ├── extract.py               # Fetch from NewsAPI → S3
│   ├── transform.py             # Clean and restructure data
│   ├── load.py                  # S3 → PostgreSQL
│   └── db.py                    # DB connection and schema
├── aws/
│   ├── aws_s3_client.py         # boto3 client factory
│   ├── aws_s3_upload.py         # Upload JSON to S3
│   └── aws_download_from_s3.py  # Download latest JSON from S3
├── news_api/
│   └── get_articles.py          # NewsAPI HTTP client
├── sql/
│   └── analytics.py             # Analytics queries
├── consts/
│   └── consts.py                # Env var loading and validation
├── bash_scripts/                # Operational shell scripts
├── Dockerfile                   # Airflow image with dependencies
├── docker-compose.yml           # 4-service stack definition
└── requirements.txt
```

---

## Deployment

The pipeline runs on a live VPS using Docker Compose with 4 services:
- `airflow-webserver` — Airflow UI
- `airflow-scheduler` — DAG scheduling
- `airflow-postgres` — Airflow metadata database
- `news-postgres` — News article warehouse

Deployment is git-based: push to `main`, pull on server, restart scheduler.