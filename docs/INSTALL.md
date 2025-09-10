# Installation Guide

This guide provides step-by-step instructions for setting up the WebCurso application on your local machine.

## Prerequisites

- Python 3.7 or higher
- Node.js 14 or higher
- npm (Node Package Manager)

## Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Initialize the database:
   ```
   python init_db.py
   ```

## Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install Node.js dependencies:
   ```
   npm install
   ```

## Running the Application

### Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Activate the virtual environment (if not already activated):
   ```
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   ```

3. Run the Flask application:
   ```
   python app.py
   ```

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Run the development server:
   ```
   npm run dev
   ```

## Accessing the Application

- Backend API: http://localhost:5000
- Frontend Application: http://localhost:5173

## Troubleshooting

### Common Issues

1. **Port conflicts**: If ports 5000 or 5173 are already in use, you can change them in the configuration files.

2. **Missing dependencies**: Ensure all dependencies are installed by running `pip install -r requirements.txt` and `npm install`.

3. **Database errors**: If you encounter database errors, try deleting the `instance/database.sqlite` file and reinitializing the database with `python init_db.py`.

### Windows-Specific Issues

1. **Execution policy errors**: If you encounter execution policy errors on Windows, run PowerShell as administrator and execute:
   ```
   Set-ExecutionPolicy RemoteSigned
   ```

2. **Path issues**: Use forward slashes (/) or double backslashes (\\) in file paths to avoid issues.

## Additional Resources

- [API Documentation](API.md)
- [Development Guidelines](DEVELOPMENT.md)
- [Testing Guide](TESTING.md)
- [Deployment Instructions](DEPLOYMENT.md)