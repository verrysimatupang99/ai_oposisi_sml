import requests

url = "http://localhost:8000/api/v1/auth/login"
data = {
    "username": "testuser2",
    "password": "Test123!@"
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

try:
    response = requests.post(url, data=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
except Exception as e:
    print(f"Error: {e}")
