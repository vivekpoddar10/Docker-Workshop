# NYC Taxi Ingestion Workshop

This repository contains a Python data ingestion pipeline for NYC Yellow Taxi data. The project builds a Docker image with dependencies installed by `uv`, then runs `pipeline/ingest_data.py` to download taxi data and load it into PostgreSQL.

## Repository structure

- `Dockerfile` - builds the container image and installs dependencies.
- `pyproject.toml` / `uv.lock` - dependency definitions.
- `pipeline/ingest_data.py` - ingestion script using `click`, `pandas`, `sqlalchemy`, and `tqdm`.
- `main.py` - a small local example script that writes a sample Parquet file.
- `insert_data.txt` - example `docker run` command for ingesting data.

## What it does

The ingestion script downloads a compressed NYC taxi CSV for a specific year and month, reads it in chunks, and inserts the data into a PostgreSQL table.

## Quick commands

```bash
# create project using uv
uv init workshop --python-3.13

# add packages
uv add pandas pyarrow

# build image
docker build -t test:pandas .

# run image with an interactive shell
docker run -it --entrypoint=bash --rm test:pandas

# connect to postgres with pgcli
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

## Dependencies

- Python 3.13+
- Docker
- Postgres reachable from the container
- `uv` for dependency installation inside Docker

Python packages required by the project:

- `pandas`
- `psycopg2-binary`
- `pyarrow`
- `sqlalchemy`
- `tqdm`

## Build the Docker image

From the repository root:

```bash
docker build -t taxi_ingest:v001 .
```

## Run the ingestion container

Example command:

```bash
docker run -it --rm \
  --network=pg_network \
  taxi_ingest:v001 \
  --pg-user=root \
  --pg-password=root \
  --pg-host=pgdatabase \
  --pg-port=5433 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips_2021_2 \
  --year=2021 \
  --month=2 \
  --chunk-size=100000
```

## Script options

- `--year` - dataset year (default: `2021`)
- `--month` - month number (default: `1`)
- `--pg-user` - Postgres username (default: `root`)
- `--pg-password` - Postgres password (default: `root`)
- `--pg-host` - Postgres host (default: `localhost`)
- `--pg-port` - Postgres port (default: `5433`)
- `--pg-db` - Postgres database name (default: `ny_taxi`)
- `--chunk-size` - number of rows per CSV chunk (default: `100000`)
- `--target-table` - target Postgres table name (default: `yellow_taxi_data`)

## Debugging

If the container exits immediately or reports a missing file:

```bash
docker run --rm -it --entrypoint=bash taxi_ingest:v001
```

Then inspect the image contents:

```bash
ls -la /app
ls -la /app/.venv
python --version
python ingest_data.py --help
```

## Notes

- `main.py` is a standalone demo and is not used by the Docker entrypoint.
- `pipeline/ingest_data.py` is the actual ingestion script run by Docker.
- Ensure PostgreSQL is reachable from the container network and the target database exists before running ingestion.
