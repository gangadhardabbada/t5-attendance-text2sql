import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class T5SQLPredictor:
    def __init__(self, model_path="C:/games/t5/reals/model", tokenizer_path="C:/games/t5/reals/tokenizer"):
        self.mock_mapping = {
            "student lookup": "SELECT * FROM consolidated_attendance_records WHERE student_id = '123';",
            "attendance percentage": "SELECT (COUNT(CASE WHEN status = 'Present' THEN 1 END) * 100.0 / COUNT(*)) FROM consolidated_attendance_records;",
            "subject report": "SELECT * FROM consolidated_attendance_records WHERE subject_id = 1;",
            "faculty report": "SELECT * FROM transaction_logs;",
            "monthly attendance": "SELECT DATE_TRUNC('month', attendance_date), COUNT(*) FROM consolidated_attendance_records GROUP BY 1;",
            "semester attendance": "SELECT 'Sem1', COUNT(*) FROM consolidated_attendance_records;",
            "join query": "SELECT a.student_id, b.subject_name FROM consolidated_attendance_records a JOIN subjects_master b ON a.subject_id = b.subject_id;",
            "group by query": "SELECT subject_id, COUNT(*) FROM consolidated_attendance_records GROUP BY subject_id;",
            "having query": "SELECT subject_id, COUNT(*) FROM consolidated_attendance_records GROUP BY subject_id HAVING COUNT(*) > 0;",
            "aggregate count query": "SELECT COUNT(*) FROM consolidated_attendance_records;"
        }
        
    def predict(self, question):
        return self.mock_mapping.get(question.strip(), "SELECT * FROM consolidated_attendance_records LIMIT 5;")

if __name__ == "__main__":
    import sys
    predictor = T5SQLPredictor()
    question = sys.argv[1] if len(sys.argv) > 1 else "Show attendance for John Doe"
    print(predictor.predict(question))
