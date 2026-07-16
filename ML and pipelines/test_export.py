import requests

login_response = requests.post(
    "http://127.0.0.1:8000/login",
    data={"username": "integrationtest@test.com", "password": "test123"}
)
token = login_response.json()["access_token"]

headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://127.0.0.1:8000/sessions/1/export",
    headers=headers
)
print("Export:", response.status_code, response.json())