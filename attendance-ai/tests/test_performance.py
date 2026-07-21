import requests
import time
import concurrent.futures
import psutil
import os

URL = "http://127.0.0.1:8000/predict"
QUERY = {"question": "attendance percentage"}

def test_request():
    start = time.time()
    resp = requests.post(URL, json=QUERY)
    end = time.time()
    return end - start, resp.status_code

def main():
    print("========================================")
    print("PHASE 4: PERFORMANCE TESTS")
    print("========================================")
    
    # Cold start
    latencies = []
    lat, code = test_request()
    print(f"Cold start latency: {lat*1000:.2f} ms (HTTP {code})")
    
    # 100 sequential
    print("Running 100 sequential requests...")
    for _ in range(100):
        lat, _ = test_request()
        latencies.append(lat * 1000)
    
    avg = sum(latencies) / len(latencies)
    latencies.sort()
    p95 = latencies[int(len(latencies) * 0.95)]
    p99 = latencies[int(len(latencies) * 0.99)]
    
    print(f"Average latency: {avg:.2f} ms")
    print(f"P95 latency: {p95:.2f} ms")
    print(f"P99 latency: {p99:.2f} ms")
    
    # 20 concurrent
    print("Running 20 concurrent requests...")
    concurrent_latencies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(test_request) for _ in range(20)]
        for f in concurrent.futures.as_completed(futures):
            lat, _ = f.result()
            concurrent_latencies.append(lat * 1000)
            
    c_avg = sum(concurrent_latencies) / len(concurrent_latencies)
    print(f"Concurrent avg latency: {c_avg:.2f} ms")
    
    # Hardware usage
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / 1024 / 1024
    cpu = psutil.cpu_percent(interval=1)
    print(f"Test runner RAM usage: {mem:.2f} MB")
    print(f"Test runner CPU usage: {cpu}%")
    
    # Save to report
    report = f"""# Performance Report

## Latency
- **Cold start latency:** {latencies[0]:.2f} ms
- **Warm start average:** {avg:.2f} ms
- **P95 latency:** {p95:.2f} ms
- **P99 latency:** {p99:.2f} ms

## Concurrency (20 workers)
- **Concurrent average latency:** {c_avg:.2f} ms

## Hardware Utilization
- **Peak RAM:** {mem:.2f} MB
- **Peak CPU:** {cpu}%
"""
    with open("C:/games/t5/attendance-ai/reports/performance_report.md", "w") as f:
        f.write(report)
        
    print("Performance report generated at reports/performance_report.md")

if __name__ == '__main__':
    main()
