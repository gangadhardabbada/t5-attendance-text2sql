import os
import psycopg2
from dotenv import load_dotenv
import sys
sys.path.append('C:/games/t5/reals')
from predict import T5SQLPredictor

load_dotenv('C:/games/t5/.env', override=True)
db_url = os.getenv('DATABASE_URL')

queries = [
    "Show attendance of John.",
    "List students absent today.",
    "Which subject has the highest attendance percentage?",
    "Show attendance percentage semester-wise.",
    "Count students absent yesterday."
]

def main():
    predictor = T5SQLPredictor()
    conn = psycopg2.connect(db_url, sslmode='require')
    
    print("========================================")
    print("STEP 3 INFERENCE TEST")
    print("========================================")
    
    for idx, q in enumerate(queries, 1):
        print(f"\\n{idx}.\\n{q}")
        print("->")
        sql = predictor.predict(q)
        print(sql)
        print("->")
        
        try:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            print("Execution Status: SUCCESS")
            print("->")
            print(f"Returned Rows: {rows}")
            cur.close()
        except Exception as e:
            print(f"Execution Status: FAILED ({e})")
            print("->")
            print("Returned Rows: None")
            conn.rollback()

    conn.close()

if __name__ == "__main__":
    main()
