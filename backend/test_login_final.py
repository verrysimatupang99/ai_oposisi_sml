import requests
import sys

try:
    response = requests.post(
        "http://localhost:8000/api/v1/auth/login",
        data={"username": "testuser2", "password": "Test123!@"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Login SUCCESS!")
        print(response.json())
    else:
        print("Login FAILED")
        print(response.text)

except Exception as e:
    print(f"Error: {e}")
