import requests

URL = "http://127.0.0.1:8000/predict"

negative_payloads = [
    "DROP TABLE students;",
    "DELETE FROM consolidated_attendance_records;",
    "UPDATE students SET attendance = 100;",
    "INSERT INTO students (id) VALUES (1);",
    "ALTER TABLE students DROP COLUMN name;",
    "TRUNCATE TABLE students;",
    "CREATE TABLE hack (id INT);",
    "invalid sql blah blah",
    "SELECT * FROM students; DROP TABLE students;"
]

def main():
    print("========================================")
    print("PHASE 3: SECURITY TESTS")
    print("========================================")
    
    success = True
    for q in negative_payloads:
        # In our mock predict setup, we will just force the predictor to return the bad query directly if it's in the negative list
        pass
        
    # Since our mocked predict.py doesn't return the raw payload as SQL, we can't easily test injection via the API endpoint unless we modify predict.py to echo the input.
    # Instead, we will directly test the sql_validator.py to prove the logic holds.
    
    import sys
    sys.path.append('C:/games/t5/attendance-ai')
    from app.sql_validator import validate_sql
    from fastapi import HTTPException
    
    for q in negative_payloads:
        try:
            validate_sql(q)
            print(f"[FAIL] Security Failed! Allowed: {q}")
            success = False
        except HTTPException as e:
            if e.status_code in [400, 403]:
                print(f"[OK] Blocked successfully ({e.status_code}): {q[:30]}...")
            else:
                print(f"[FAIL] Unexpected status code {e.status_code} for {q}")
                success = False

    if success:
        print("\\nAll Security Tests Passed!")

if __name__ == '__main__':
    main()
