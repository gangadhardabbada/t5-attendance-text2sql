# Architecture Overview

## Components

1. **FastAPI Application (`app/api.py`)**
   - Serves as the high-throughput HTTP ingress layer.
   - Parses incoming JSON and coordinates the AI inference and database execution.

2. **Model Inference (`app/predict.py`)**
   - Loads the `attendance-t5-small-v1.0` weights.
   - Encodes the user's natural language question and decodes the resulting SQL sequence using greedy search or beam search.

3. **Security Validator (`app/sql_validator.py`)**
   - Parses the generated SQL string using `sqlparse`.
   - Validates that the AST root is a `SELECT` statement and strictly blocks any write operations (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`).

4. **Database Execution (`app/database.py`)**
   - Connects to the PostgreSQL instance using `psycopg2`.
   - Executes the validated SQL and maps the cursor response back into an array of dictionaries for JSON serialization.
