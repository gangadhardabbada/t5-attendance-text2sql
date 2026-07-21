import requests
import sys
import psycopg2
import os
from dotenv import load_dotenv

def main():
    print("========================================")
    print("SMOKE TEST")
    print("========================================")
    
    # 1. Check DB connectivity
    load_dotenv('.env', override=True)
    db_url = os.getenv('DATABASE_URL')
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
        conn.close()
        print("[OK] Database connectivity verified.")
    except Exception as e:
        print(f"[FAIL] Database connection failed: {e}")
        sys.exit(1)
        
    # 2. Check API
    try:
        resp = requests.post("http://127.0.0.1:8000/predict", json={"question": "student lookup"})
        if resp.status_code == 200:
            print("[OK] API is running and responding.")
            print("[OK] Inference successful.")
        else:
            print(f"[FAIL] API returned {resp.status_code}: {resp.text}")
            sys.exit(1)
    except Exception as e:
        print(f"[FAIL] API connection failed: {e}")
        sys.exit(1)
        
    print("\\nSmoke test passed successfully!")

if __name__ == '__main__':
    main()
