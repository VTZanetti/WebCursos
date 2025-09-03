import requests
import json

def test_create_course():
    url = "http://localhost:5000/api/cursos"
    headers = {"Content-Type": "application/json"}
    data = {
        "titulo": "Test Course",
        "total_aulas": 10
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_create_course()