# Changelog

## [1.0.0] - 2026-07-21
### Added
- T5-Small model fine-tuned on attendance schema (`attendance-t5-small-v1.0`).
- FastAPI server handling `POST /predict` endpoints.
- Strict SQL validation (`app.sql_validator`) blocking destructive DML/DDL.
- Frozen training/testing dataset chunks in `/dataset_v1`.
- Database schema scripts (`schema.sql`, `seed.sql`).
- Docker compose configuration for simplified deployment.
- Initial project structure (`/app`, `/docs`, `/tests`).
