# Attendance-AI (T5 Text-to-SQL)

This repository contains a production-ready Text-to-SQL system designed for university attendance management. It translates natural language questions into valid PostgreSQL syntax, allowing seamless, natural querying of the attendance records.

## Features
- **Model**: `t5-small` fine-tuned specifically for attendance schemas.
- **Performance**: The fine-tuned model achieved 94.2% Exact Match and 96.5% Execution Accuracy on the project test set.
- **Query Capabilities**: The model is capable of generating JOIN, GROUP BY, ORDER BY, HAVING, and aggregate queries when these query patterns are sufficiently represented in the fine-tuning dataset.
- **API**: FastAPI server with strict SQL parsing to prevent destructive operations.
- **Security**: Validates all generated SQL to guarantee only `SELECT` operations are permitted.

## Project Structure
- `/model`: Contains the `attendance-t5-small-v1.0` model weights and configs.
- `/tokenizer`: The tokenizer files.
- `/dataset_v1`: The frozen, versioned CSV datasets used for training and testing.
- `/reports`: Evaluation and validation reports.

## Running the API Locally
1. Copy `.env.example` to `.env` and fill in your Supabase `DATABASE_URL`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   uvicorn api:app --host 127.0.0.1 --port 8000
   ```

## Endpoints

### POST `/predict`
Translates a natural language question into SQL and executes it against the database.

**Request**:
```json
{
  "question": "Show attendance percentage for CSE students."
}
```

**Response**:
```json
{
  "sql": "SELECT ...",
  "rows": [
    {"subject_code": "CS101", "percentage": 85.0}
  ],
  "execution_time_ms": 148,
  "confidence": 0.95
}
```

## Security Guardrails
The API includes a validation layer (`sqlparse`) that ensures:
1. The generated SQL parses as a valid query.
2. The root command is strictly `SELECT`.
3. Forbidden keywords (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `CREATE`) trigger an immediate HTTP 403 Forbidden rejection.
