-- schema.sql
CREATE TABLE IF NOT EXISTS students_master (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    enrollment_date DATE
);

CREATE TABLE IF NOT EXISTS subjects_master (
    subject_id SERIAL PRIMARY KEY,
    subject_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS consolidated_attendance_records (
    record_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students_master(student_id),
    subject_id INT REFERENCES subjects_master(subject_id),
    attendance_date DATE,
    status VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS transaction_logs (
    log_id SERIAL PRIMARY KEY,
    action VARCHAR(255),
    log_date TIMESTAMP
);
