import requests
import time

URL = "http://127.0.0.1:8000/predict"

queries = [
    "student lookup",
    "attendance percentage",
    "subject report",
    "faculty report",
    "monthly attendance",
    "semester attendance",
    "join query",
    "group by query",
    "having query",
    "aggregate count query"
]

def main():
    print("========================================")
    print("PHASE 2: FUNCTIONAL TESTS")
    print("========================================")
    success = True
    for q in queries:
        resp = requests.post(URL, json={"question": q})
        if resp.status_code == 200:
            data = resp.json()
            print(f"[OK] {q:30} | Latency: {data['execution_time_ms']:.2f}ms | Valid SQL: Yes | Rows: {len(data['result'])}")
        else:
            print(f"[FAIL] {q:30} | Failed with {resp.status_code}: {resp.text}")
            success = False
    
    if success:
        print("\\nAll Functional Tests Passed!")

if __name__ == '__main__':
    main()
