# Deployment Guide

## Prerequisites
- Docker & Docker Compose
- PostgreSQL (Supabase or self-hosted)
- Python 3.12 (For bare-metal deployment)

## Environment Setup
Copy the configuration template:
```bash
cp .env.example .env
```
Edit `.env` to include your Supabase `DATABASE_URL`.

## Docker Deployment (Recommended)
1. Build and start the container:
```bash
docker-compose up -d --build
```
2. The API will be available at `http://localhost:8000`.

## Bare-Metal Deployment
1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the server:
```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000
```
