# SQLite Permanent Configuration

This document describes the changes made to permanently configure SQLite as the database for WebCurso, eliminating the need for constant reconfiguration.

## Changes Made

### 1. Configuration Files

**config.py** - Permanently set to use SQLite:
- DATABASE_TYPE is now hardcoded to 'sqlite'
- SQLITE_DATABASE_PATH points to a permanent location: `instance/database.sqlite`
- Removed all MySQL configuration

### 2. Database Manager

**database.py** - Simplified for SQLite only:
- Removed all MySQL connection code
- Permanently uses SQLite connections
- Properly converts sqlite3.Row objects to dictionaries

### 3. Application Code

**app.py** - Updated to work with SQLite exclusively:
- Removed all MySQL-specific query variations
- Simplified database queries to use SQLite parameter binding (?)
- Fixed dictionary handling issues

### 4. Startup Scripts

**start_server.bat** - Ensures SQLite is always used:
- Automatically checks for and initializes the database
- Sets DATABASE_TYPE environment variable to 'sqlite'

**start_sqlite_server.bat** - Dedicated SQLite startup script:
- Simplified to only work with SQLite
- Automatically initializes database if it doesn't exist

**setup_sqlite.bat** - Simplified setup process:
- Streamlined database initialization
- Clear instructions for starting the server

### 5. Environment Configuration

**.env** - Default environment configuration:
- Sets DATABASE_TYPE=sqlite
- Points to the permanent SQLite database file

## Benefits

1. **No More Configuration**: The application will always use SQLite without any additional setup
2. **Persistent Data**: Database is stored in `instance/database.sqlite` and persists between sessions
3. **Simplified Codebase**: Removed all MySQL-specific code, making the application lighter and easier to maintain
4. **Easier Deployment**: No need to configure database connections or install MySQL

## Database Location

The SQLite database is permanently stored at:
```
c:\Dev\WebCurso\backend\instance\database.sqlite
```

This file will persist all data between application restarts.

## How to Use

1. **First-time setup**:
   ```
   cd c:\Dev\WebCurso\backend
   setup_sqlite.bat
   ```

2. **Starting the server**:
   ```
   cd c:\Dev\WebCurso\backend
   start_server.bat
   ```

   Or simply:
   ```
   cd c:\Dev\WebCurso\backend
   python app.py
   ```

The database will automatically be created and initialized if it doesn't exist.