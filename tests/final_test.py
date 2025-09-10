import requests
import json

def test_batch_endpoint():
    """Test the batch endpoint for marking/unmarking lessons"""
    base_url = 'http://localhost:5000/api/cursos/10/aulas/batch'
    headers = {'Content-Type': 'application/json'}
    
    # Test data - mark lessons 1-5 as completed
    data = {
        'aulas': [
            {'numero_aula': 1, 'concluida': True},
            {'numero_aula': 2, 'concluida': True},
            {'numero_aula': 3, 'concluida': True},
            {'numero_aula': 4, 'concluida': True},
            {'numero_aula': 5, 'concluida': True}
        ]
    }
    
    try:
        response = requests.post(base_url, data=json.dumps(data), headers=headers)
        print(f"Mark lessons as completed - Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('message', 'No message')}")
            print(f"Total completed: {result['data']['total_aulas_concluidas']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception when marking lessons: {e}")
    
    # Test data - unmark lessons 1-5 as completed
    data = {
        'aulas': [
            {'numero_aula': 1, 'concluida': False},
            {'numero_aula': 2, 'concluida': False},
            {'numero_aula': 3, 'concluida': False},
            {'numero_aula': 4, 'concluida': False},
            {'numero_aula': 5, 'concluida': False}
        ]
    }
    
    try:
        response = requests.post(base_url, data=json.dumps(data), headers=headers)
        print(f"\nUnmark lessons as completed - Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('message', 'No message')}")
            print(f"Total completed: {result['data']['total_aulas_concluidas']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception when unmarking lessons: {e}")

if __name__ == "__main__":
    print("Testing batch endpoint for lesson management...")
    test_batch_endpoint()