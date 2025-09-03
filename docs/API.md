# API Documentation

This document provides detailed information about the WebCurso RESTful API endpoints.

## Base URL

All API endpoints are prefixed with `/api`. When running locally, the base URL is:
```
http://localhost:5000/api
```

## Authentication

The current version of WebCurso does not implement authentication. All endpoints are publicly accessible.

## CORS Configuration

The API is configured to accept requests from the following origins:
- http://localhost:5173 (Vite development server)
- http://127.0.0.1:5173
- http://localhost:3000
- http://127.0.0.1:3000

## Error Handling

All API responses follow a consistent format:

### Success Response
```json
{
  "success": true,
  "data": {},
  "timestamp": "2023-01-01T00:00:00.000000"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "timestamp": "2023-01-01T00:00:00.000000"
}
```

## Endpoints

### Courses

#### GET /cursos
Returns a list of all courses with their completion statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "cursos": [
      {
        "id": 1,
        "titulo": "Course Title",
        "link": "https://example.com",
        "total_aulas": 10,
        "anotacoes": "Course notes",
        "created_at": "2023-01-01 00:00:00",
        "updated_at": "2023-01-01 00:00:00",
        "aulas_concluidas": 5,
        "progresso": 50.0
      }
    ],
    "count": 1
  }
}
```

#### POST /cursos
Creates a new course.

**Request Body:**
```json
{
  "titulo": "Course Title",
  "link": "https://example.com",
  "total_aulas": 10,
  "anotacoes": "Course notes"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "titulo": "Course Title",
    "link": "https://example.com",
    "total_aulas": 10,
    "anotacoes": "Course notes",
    "created_at": "2023-01-01 00:00:00",
    "updated_at": "2023-01-01 00:00:00",
    "aulas_concluidas": 0,
    "progresso": 0.0
  },
  "message": "Curso criado com sucesso"
}
```

#### GET /cursos/{id}
Returns details of a specific course.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "titulo": "Course Title",
    "link": "https://example.com",
    "total_aulas": 10,
    "anotacoes": "Course notes",
    "created_at": "2023-01-01 00:00:00",
    "updated_at": "2023-01-01 00:00:00",
    "aulas_concluidas": 5,
    "aulas_concluidas_list": [1, 2, 3, 4, 5],
    "progresso": 50.0
  }
}
```

#### PUT /cursos/{id}
Updates a course.

**Request Body:**
```json
{
  "titulo": "Updated Course Title",
  "link": "https://example.com/updated",
  "total_aulas": 15,
  "anotacoes": "Updated course notes"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "titulo": "Updated Course Title",
    "link": "https://example.com/updated",
    "total_aulas": 15,
    "anotacoes": "Updated course notes",
    "created_at": "2023-01-01 00:00:00",
    "updated_at": "2023-01-02 00:00:00",
    "aulas_concluidas": 5,
    "aulas_concluidas_list": [1, 2, 3, 4, 5],
    "progresso": 33.3
  },
  "message": "Curso atualizado com sucesso"
}
```

#### DELETE /cursos/{id}
Deletes a course and all its associated lesson completions.

**Response:**
```json
{
  "success": true,
  "message": "Curso \"Course Title\" deletado com sucesso"
}
```

### Lessons

#### POST /cursos/{id}/aula
Marks or unmarks a single lesson as completed.

**Request Body:**
```json
{
  "numero_aula": 1,
  "concluida": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "curso_id": 1,
    "numero_aula": 1,
    "concluida": true,
    "total_aulas_concluidas": 6,
    "aulas_concluidas_list": [1, 2, 3, 4, 5, 6],
    "progresso": 60.0
  },
  "message": "Aula 1 marcada como concluída"
}
```

#### POST /cursos/{id}/aulas/batch
Marks or unmarks multiple lessons as completed in a single request (batch processing).

**Request Body:**
```json
{
  "aulas": [
    {
      "numero_aula": 1,
      "concluida": true
    },
    {
      "numero_aula": 2,
      "concluida": true
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "curso_id": 1,
    "updated_aulas": [
      {
        "numero_aula": 1,
        "concluida": true,
        "message": "Aula 1 marcada como concluída"
      },
      {
        "numero_aula": 2,
        "concluida": true,
        "message": "Aula 2 marcada como concluída"
      }
    ],
    "total_aulas_concluidas": 7,
    "aulas_concluidas_list": [1, 2, 3, 4, 5, 6, 7],
    "progresso": 70.0
  },
  "message": "Aulas atualizadas com sucesso"
}
```

### Utility Endpoints

#### GET /health
Checks the API health status.

**Response:**
```json
{
  "success": true,
  "message": "API funcionando corretamente",
  "database_type": "sqlite",
  "timestamp": "2023-01-01T00:00:00.000000"
}
```

#### GET /stats
Returns general statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_cursos": 5,
    "total_aulas_concluidas": 25,
    "total_aulas_disponiveis": 50,
    "progresso_geral": 50.0
  }
}
```