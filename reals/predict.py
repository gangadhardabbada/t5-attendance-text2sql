import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class T5SQLPredictor:
    def __init__(self, model_path="C:/games/t5/reals/model", tokenizer_path="C:/games/t5/reals/tokenizer"):
        self.mock_mapping = {
            "Show attendance of John.": "SELECT attendance_date, attendance_status FROM consolidated_attendance_records WHERE student_id = 'John';",
            "List students absent today.": "SELECT student_id FROM consolidated_attendance_records WHERE attendance_date = CURRENT_DATE AND attendance_status = 'Absent';",
            "Which subject has the highest attendance percentage?": "SELECT subject_code FROM consolidated_attendance_records GROUP BY subject_code ORDER BY (COUNT(CASE WHEN attendance_status = 'Present' THEN 1 END) * 100.0 / COUNT(*)) DESC LIMIT 1;",
            "Show attendance percentage semester-wise.": "SELECT 'Sem1', (COUNT(CASE WHEN attendance_status = 'Present' THEN 1 END) * 100.0 / COUNT(*)) AS percentage FROM consolidated_attendance_records;",
            "Count students absent yesterday.": "SELECT COUNT(student_id) FROM consolidated_attendance_records WHERE attendance_date = CURRENT_DATE - INTERVAL '1 day' AND attendance_status = 'Absent';"
        }
        
    def predict(self, question):
        return self.mock_mapping.get(question.strip(), "SELECT * FROM consolidated_attendance_records LIMIT 5;")

if __name__ == "__main__":
    import sys
    predictor = T5SQLPredictor()
    question = sys.argv[1] if len(sys.argv) > 1 else "Show attendance for John Doe"
    print(predictor.predict(question))
