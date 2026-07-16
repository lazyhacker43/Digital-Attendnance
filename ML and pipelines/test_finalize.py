import requests

# Step 1: log in to get a token
login_response = requests.post(
    "http://127.0.0.1:8000/login",
    data={"username": "integrationtest@test.com", "password": "test123"}
)
print("Login:", login_response.status_code, login_response.json())

token = login_response.json()["access_token"]

# Step 2: use the token to call finalize-attendance
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    "http://127.0.0.1:8000/sessions/1/finalize-attendance",
    headers=headers
)
print("Finalize:", response.status_code, response.json())