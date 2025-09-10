# 🚀 Quick Start - Simplified WebCurso

This guide will help you run the simplified version of WebCurso with a single command.

## 📋 Prerequisites

Before starting, make sure you have these installed:
- Python 3.8 or higher
- Node.js 16 or higher
- Git (optional, but recommended)

## 🎯 One-Command Setup

Run this single command from the project root directory:

```bash
python start.py
```

This will automatically:
1. Set up Python virtual environment
2. Install all backend dependencies
3. Initialize the SQLite database
4. Install all frontend dependencies (Node.js packages)
5. Start both the backend API (port 5000) and frontend app (port 5173)
6. Open your browser to the application

## 🔧 Manual Setup (Alternative)

If you prefer to run components separately:

### Backend Setup:
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
python init_db.py
python app.py
```

### Frontend Setup:
```bash
cd frontend
npm install
npm run dev
```

## 🌐 Access the Application

After starting:
- **Main Application**: http://localhost:5173
- **API Endpoints**: http://localhost:5000/api

## 🛠️ Troubleshooting

### Common Issues:

1. **Port already in use**:
   - Stop any existing servers
   - Or modify ports in the respective config files

2. **Permission errors**:
   - Run the command prompt as Administrator (Windows)
   - Or use sudo (macOS/Linux)

3. **Missing dependencies**:
   - Ensure Python and Node.js are properly installed
   - Check versions with `python --version` and `node --version`

### Reset Database:
To start fresh with a clean database:
```bash
# Delete the existing database
rm backend/instance/database.sqlite
# Or on Windows:
# del backend\instance\database.sqlite

# Reinitialize
cd backend
python init_db.py
```

## 📁 Project Structure

```
WebCurso/
├── backend/           # Flask API server
│   ├── app.py         # Main Flask application
│   ├── init_db.py     # Database initialization
│   ├── requirements.txt # Python dependencies
│   └── instance/      # SQLite database storage
├── frontend/          # Vue.js frontend application
│   ├── src/           # Vue components and views
│   ├── package.json   # Node.js dependencies
│   └── vite.config.js # Vite configuration
├── start.py          # Simplified startup script
└── README.md         # This file
```

## 🔄 Development Workflow

1. Make backend changes in `backend/app.py`
2. Make frontend changes in `frontend/src/`
3. Both servers support hot-reloading
4. No build step needed for development

## 📚 API Endpoints

All endpoints are available at `http://localhost:5000/api/`:

- `GET /api/cursos` - List all courses
- `POST /api/cursos` - Create a new course
- `GET /api/cursos/<id>` - Get course details
- `PUT /api/cursos/<id>` - Update a course
- `DELETE /api/cursos/<id>` - Delete a course
- `POST /api/cursos/<id>/aula` - Mark lesson as completed
- `GET /api/health` - Health check
- `GET /api/stats` - Statistics

## 🎨 Frontend Routes

- `/` - Dashboard with all courses
- `/curso/:id` - Detailed view of a specific course