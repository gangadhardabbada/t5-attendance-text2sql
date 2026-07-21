-- seed.sql
INSERT INTO students_master (name, enrollment_date) VALUES
('John Doe', '2023-09-01'),
('Jane Smith', '2023-09-01');

INSERT INTO subjects_master (subject_name) VALUES
('Mathematics'),
('Physics');

INSERT INTO consolidated_attendance_records (student_id, subject_id, attendance_date, status) VALUES
(1, 1, '2023-10-01', 'Present'),
(2, 1, '2023-10-01', 'Absent');

INSERT INTO transaction_logs (action, log_date) VALUES
('System startup', '2023-10-01 08:00:00');
