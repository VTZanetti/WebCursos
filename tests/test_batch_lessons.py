import requests
import json

base_url = 'http://localhost:5000/api/cursos/10/aulas/batch'
headers = {'Content-Type': 'application/json'}

# Test data - mark all lessons 1-5 as completed
data = {
    'aulas': [
        {'numero_aula': 1, 'concluida': True},
        {'numero_aula': 2, 'concluida': True},
        {'numero_aula': 3, 'concluida': True},
        {'numero_aula': 4, 'concluida': True},
        {'numero_aula': 5, 'concluida': True}
    ]
}

response = requests.post(base_url, data=json.dumps(data), headers=headers)
print(f'Status Code: {response.status_code}')
print(f'Response: {response.json()}')

# Test data - unmark all lessons 1-5 as completed
data = {
    'aulas': [
        {'numero_aula': 1, 'concluida': False},
        {'numero_aula': 2, 'concluida': False},
        {'numero_aula': 3, 'concluida': False},
        {'numero_aula': 4, 'concluida': False},
        {'numero_aula': 5, 'concluida': False}
    ]
}

response = requests.post(base_url, data=json.dumps(data), headers=headers)
print(f'Status Code: {response.status_code}')
print(f'Response: {response.json()}')