import sqlite3
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.config import SQLITE_DATABASE_PATH

print(f"Database path: {SQLITE_DATABASE_PATH}")

try:
    conn = sqlite3.connect(SQLITE_DATABASE_PATH)
    cursor = conn.cursor()
    
    print("Connected to database successfully")
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Tables: {tables}")
    
    # Check cursos table structure
    cursor.execute("PRAGMA table_info(cursos)")
    cursos_info = cursor.fetchall()
    print(f"cursos table structure: {cursos_info}")
    
    # Check aulas_concluidas table structure
    cursor.execute("PRAGMA table_info(aulas_concluidas)")
    aulas_info = cursor.fetchall()
    print(f"aulas_concluidas table structure: {aulas_info}")
    
    # Check if we can insert a test record
    cursor.execute("INSERT INTO cursos (titulo, link, total_aulas, anotacoes) VALUES (?, ?, ?, ?)", 
                  ("Test Course", "http://test.com", 10, "Test notes"))
    conn.commit()
    print("Test insert successful")
    
    # Check if record was inserted
    cursor.execute("SELECT * FROM cursos WHERE titulo = ?", ("Test Course",))
    result = cursor.fetchone()
    print(f"Inserted record: {result}")
    
    # Clean up test record
    cursor.execute("DELETE FROM cursos WHERE titulo = ?", ("Test Course",))
    conn.commit()
    print("Test record cleaned up")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()