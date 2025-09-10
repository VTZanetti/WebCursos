import requests
import json

base_url = 'http://localhost:5000/api/cursos/10/aula'
headers = {'Content-Type': 'application/json'}

for i in range(1, 4):
    data = {'numero_aula': i, 'concluida': True}
    response = requests.post(base_url, data=json.dumps(data), headers=headers)
    print(f'Aula {i} - Status Code: {response.status_code}')
    print(f'Aula {i} - Response: {response.json()}')