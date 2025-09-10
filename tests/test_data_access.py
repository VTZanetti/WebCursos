# Test to verify the data access pattern fix
mock_cursos_response = {
    "data": {
        "count": 9,
        "cursos": [
            {
                "anotacoes": "",
                "aulas_concluidas": 4,
                "created_at": "2025-09-03 13:03:18",
                "id": 12,
                "link": "",
                "progresso": 12.1,
                "titulo": "teste",
                "total_aulas": 33,
                "updated_at": "2025-09-03 13:03:18"
            }
        ]
    },
    "success": True,
    "timestamp": "2025-09-03T10:23:08.880000"
}

# This is how we're now accessing the data in the fixed code:
cursos = mock_cursos_response.get('data', {}).get('cursos', [])
print(f"Number of courses: {len(cursos)}")
if cursos:
    print(f"First course title: {cursos[0].get('titulo', 'No title')}")
else:
    print("No courses found")