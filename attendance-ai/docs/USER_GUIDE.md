# User Guide

Welcome to the Attendance AI! This tool allows you to type natural language questions and instantly query the university attendance database.

## How to use

Send a `POST` request to the `/predict` endpoint with your natural language question.
For example:
- "How many students were absent yesterday?"
- "What is the attendance percentage for Computer Science?"
- "Show me all records for student ID 12345."

The AI will parse your question, generate the corresponding SQL, execute it against the attendance database, and return the exact rows and statistics you requested.

## Limitations
- The AI can only read data. You cannot add, update, or delete records through this interface.
- You must ask questions related to the attendance domain. Unrelated questions will generate invalid SQL and be rejected.
