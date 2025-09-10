import requests
import json

# Test creating a course
url = "http://localhost:5000/api/cursos"
data = {
    "titulo": "Test Course from Python",
    "total_aulas": 10,
    "anotacoes": "Test notes from Python"
}

headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")