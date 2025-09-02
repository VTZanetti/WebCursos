#!/usr/bin/env python3
"""
Database initialization script for WebCursos application.

This script creates the SQLite database and the required tables:
- cursos: stores course information
- aulas_concluidas: tracks completed lessons for each course

Usage:
    python init_db.py
"""

import sqlite3
import os

def init_database():
    """Initialize the database with required tables."""
    # Database file path
    db_path = 'webcursos.db'
    
    # Remove existing database if it exists (for fresh start)
    if os.path.exists(db_path):
        print(f"Removing existing database: {db_path}")
        os.remove(db_path)
    
    # Create connection to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create cursos table
        cursor.execute('''
            CREATE TABLE cursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                link TEXT,
                total_aulas INTEGER NOT NULL,
                descricao TEXT
            )
        ''')
        print("✓ Table 'cursos' created successfully")
        
        # Create aulas_concluidas table
        cursor.execute('''
            CREATE TABLE aulas_concluidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                curso_id INTEGER NOT NULL,
                numero_aula INTEGER NOT NULL,
                FOREIGN KEY (curso_id) REFERENCES cursos (id) ON DELETE CASCADE,
                UNIQUE(curso_id, numero_aula)
            )
        ''')
        print("✓ Table 'aulas_concluidas' created successfully")
        
        # Insert some sample data for testing
        sample_courses = [
            ("Python Fundamentals", "https://example.com/python", 20, "Learn Python from basics to advanced"),
            ("Web Development with Flask", "https://example.com/flask", 15, "Build web applications with Flask framework"),
            ("Database Design", "https://example.com/database", 12, "Learn database design principles")
        ]
        
        cursor.executemany('''
            INSERT INTO cursos (titulo, link, total_aulas, descricao)
            VALUES (?, ?, ?, ?)
        ''', sample_courses)
        
        # Add some completed lessons for sample data
        sample_completed = [
            (1, 1), (1, 2), (1, 3),  # Python course: lessons 1, 2, 3 completed
            (2, 1), (2, 2),          # Flask course: lessons 1, 2 completed
            (3, 1)                   # Database course: lesson 1 completed
        ]
        
        cursor.executemany('''
            INSERT INTO aulas_concluidas (curso_id, numero_aula)
            VALUES (?, ?)
        ''', sample_completed)
        
        # Commit changes
        conn.commit()
        print("✓ Sample data inserted successfully")
        print(f"\n✅ Database '{db_path}' initialized successfully!")
        print("\nSample courses added:")
        print("- Python Fundamentals (3/20 lessons completed)")
        print("- Web Development with Flask (2/15 lessons completed)")
        print("- Database Design (1/12 lessons completed)")
        
    except sqlite3.Error as e:
        print(f"❌ Error creating database: {e}")
        conn.rollback()
    finally:
        conn.close()

def verify_database():
    """Verify that the database was created correctly."""
    try:
        conn = sqlite3.connect('webcursos.db')
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"\n📋 Tables created: {[table[0] for table in tables]}")
        
        # Check courses count
        cursor.execute("SELECT COUNT(*) FROM cursos")
        course_count = cursor.fetchone()[0]
        print(f"📚 Total courses: {course_count}")
        
        # Check completed lessons count
        cursor.execute("SELECT COUNT(*) FROM aulas_concluidas")
        completed_count = cursor.fetchone()[0]
        print(f"✅ Total completed lessons: {completed_count}")
        
        conn.close()
    except sqlite3.Error as e:
        print(f"❌ Error verifying database: {e}")

if __name__ == "__main__":
    print("🚀 Initializing WebCursos database...")
    init_database()
    verify_database()
    print("\n📝 You can now run 'python app.py' to start the Flask application!")