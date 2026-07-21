# API Documentation

## Base URL
`http://localhost:8000`

## Endpoints

### 1. Predict SQL
Transforms natural language into executable SQL and returns the dataset.

**URL**: `/predict`  
**Method**: `POST`  
**Auth**: None required (Internal VPC deployment recommended)

#### Request Body
```json
{
  "question": "Show attendance percentage for CSE students."
}
```

#### Response (Success - 200 OK)
```json
{
  "sql": "SELECT ...",
  "confidence": 0.95,
  "result": [
    { "subject_code": "CS101", "percentage": 85.0 }
  ],
  "execution_time_ms": 145.2
}
```

#### Response (Error - 403 Forbidden)
Occurs when the AI generates a DDL/DML query that modifies the database.
```json
{
  "detail": "Forbidden destructive keyword 'DROP' detected."
}
```
