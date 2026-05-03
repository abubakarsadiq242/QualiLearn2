import requests
import json
import os

BASE_URL = "http://127.0.0.1:5000/api"

def verify_sync():
    print(">>> STARTING DASHBOARD SYNC VERIFICATION")
    
    # 1. Login
    login_res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "test@test.com",
        "password": "password123"
    })
    token = login_res.json()['data']['token']
    headers = {"Authorization": f"Bearer {token}"}
    print(">>> LOGIN SUCCESS")

    # 2. Fetch High-Precision Analytics
    analytics_res = requests.get(f"{BASE_URL}/analytics/dashboard-stats", headers=headers)
    stats = analytics_res.json()['data']
    
    print(">>> ANALYTICS RESPONSE CHECK:")
    required_keys = ['overall_progress', 'study_time', 'daily_time', 'assessments_passed', 'accuracy', 'current_streak', 'resume_topic']
    for key in required_keys:
        status = "OK" if key in stats else "MISSING"
        print(f"    - {key}: {status} (Value: {stats.get(key)})")

    # 3. Fetch Dashboard Route (Redundancy check)
    dash_res = requests.get(f"{BASE_URL}/dashboard/", headers=headers)
    dash_stats = dash_res.json()['data']
    print(">>> DASHBOARD RESPONSE CHECK:")
    for key in required_keys:
        status = "OK" if key in dash_stats else "MISSING"
        print(f"    - {key}: {status} (Value: {dash_stats.get(key)})")

    if all(key in stats for key in required_keys):
        print(">>> SUCCESS: API SYNC VERIFIED")
    else:
        print("!!! FAIL: Missing critical keys in response")

if __name__ == '__main__':
    verify_sync()
