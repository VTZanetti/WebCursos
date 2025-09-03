// Test to verify the frontend fix
const mockCursosResponse = {
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
  "success": true,
  "timestamp": "2025-09-03T10:23:08.880000"
};

// This is how we're now accessing the data in the fixed code:
const cursos = mockCursosResponse.data?.cursos || [];
console.log("Number of courses:", cursos.length);
console.log("First course title:", cursos[0]?.titulo || "No courses found");

// This should output:
// Number of courses: 1
// First course title: teste