import requests
import json

# Test the batch endpoint
url = 'http://localhost:5000/api/cursos/10/aulas/batch'
headers = {'Content-Type': 'application/json'}

# Test data - mark lessons 1-3 as completed
data = {
    'aulas': [
        {'numero_aula': 1, 'concluida': True},
        {'numero_aula': 2, 'concluida': True},
        {'numero_aula': 3, 'concluida': True}
    ]
}

try:
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test data - unmark lessons 1-3 as completed
data = {
    'aulas': [
        {'numero_aula': 1, 'concluida': False},
        {'numero_aula': 2, 'concluida': False},
        {'numero_aula': 3, 'concluida': False}
    ]
}

try:
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")