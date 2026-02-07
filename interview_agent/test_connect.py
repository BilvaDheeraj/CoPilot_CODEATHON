import requests
import json
import time

print("Waiting for server to be ready...")
time.sleep(2)

try:
    print("Testing GET / ...")
    r = requests.get("http://127.0.0.1:8000/", timeout=5)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")

    print("\nTesting POST /start-interview ...")
    r = requests.post("http://127.0.0.1:8000/start-interview", json={"candidate_name": "TestUser"}, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
except Exception as e:
    print(f"Failed: {e}")
