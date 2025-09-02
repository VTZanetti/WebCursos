#!/usr/bin/env python3
"""
WebCursos - Flask Application for Course Progress Management

This application provides a web interface for managing personal course progress.
Features:
- Dashboard with course overview and progress tracking
- Add new courses functionality
- Detailed course view with lesson tracking

Author: Flask Backend Developer
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from typing import List, Dict, Optional, Tuple

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Database configuration
DATABASE = 'webcursos.db'

def get_db_connection() -> sqlite3.Connection:
    """
    Create and return a database connection.
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
    return conn

def calculate_course_progress(curso_id: int, total_aulas: int) -> float:
    """
    Calculate the progress percentage for a specific course.
    
    Args:
        curso_id (int): Course ID
        total_aulas (int): Total number of lessons in the course
        
    Returns:
        float: Progress percentage (0-100)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Count completed lessons for this course
    cursor.execute('''
        SELECT COUNT(*) FROM aulas_concluidas 
        WHERE curso_id = ?
    ''', (curso_id,))
    
    completed_lessons = cursor.fetchone()[0]
    conn.close()
    
    if total_aulas == 0:
        return 0.0
    
    return round((completed_lessons / total_aulas) * 100, 1)

def get_completed_lessons(curso_id: int) -> List[int]:
    """
    Get list of completed lesson numbers for a specific course.
    
    Args:
        curso_id (int): Course ID
        
    Returns:
        List[int]: List of completed lesson numbers
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT numero_aula FROM aulas_concluidas 
        WHERE curso_id = ? 
        ORDER BY numero_aula
    ''', (curso_id,))
    
    completed = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return completed

@app.route('/')
def dashboard():
    """
    Dashboard route - displays all courses with their progress.
    
    Returns:
        str: Rendered HTML template with courses data
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all courses from database
    cursor.execute('''
        SELECT id, titulo, link, total_aulas, descricao 
        FROM cursos 
        ORDER BY titulo
    ''')
    
    courses_data = cursor.fetchall()
    conn.close()
    
    # Calculate progress for each course
    courses = []
    for course in courses_data:
        progress = calculate_course_progress(course['id'], course['total_aulas'])
        completed_count = int((progress / 100) * course['total_aulas'])
        
        courses.append({
            'id': course['id'],
            'titulo': course['titulo'],
            'link': course['link'],
            'total_aulas': course['total_aulas'],
            'descricao': course['descricao'],
            'progress': progress,
            'completed_count': completed_count
        })
    
    return render_template('index.html', courses=courses)

@app.route('/adicionar_curso', methods=['POST'])
def adicionar_curso():
    """
    Add new course route - handles course creation form submission.
    
    Returns:
        redirect: Redirects to dashboard after adding course
    """
    # Get form data
    titulo = request.form.get('titulo', '').strip()
    link = request.form.get('link', '').strip()
    total_aulas = request.form.get('total_aulas', '').strip()
    descricao = request.form.get('descricao', '').strip()
    
    # Validate required fields
    if not titulo:
        flash('Título do curso é obrigatório!', 'error')
        return redirect(url_for('dashboard'))
    
    if not total_aulas or not total_aulas.isdigit() or int(total_aulas) <= 0:
        flash('Número total de aulas deve ser um número positivo!', 'error')
        return redirect(url_for('dashboard'))
    
    total_aulas = int(total_aulas)
    
    # Insert new course into database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO cursos (titulo, link, total_aulas, descricao)
            VALUES (?, ?, ?, ?)
        ''', (titulo, link, total_aulas, descricao))
        
        conn.commit()
        conn.close()
        
        flash(f'Curso "{titulo}" adicionado com sucesso!', 'success')
        
    except sqlite3.Error as e:
        flash(f'Erro ao adicionar curso: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/curso/<int:curso_id>')
def curso_detalhes(curso_id: int):
    """
    Course details route - displays detailed view of a specific course.
    
    Args:
        curso_id (int): Course ID from URL parameter
        
    Returns:
        str: Rendered HTML template with course details
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get course information
    cursor.execute('''
        SELECT id, titulo, link, total_aulas, descricao 
        FROM cursos 
        WHERE id = ?
    ''', (curso_id,))
    
    course_data = cursor.fetchone()
    conn.close()
    
    if not course_data:
        flash('Curso não encontrado!', 'error')
        return redirect(url_for('dashboard'))
    
    # Get completed lessons for this course
    completed_lessons = get_completed_lessons(curso_id)
    progress = calculate_course_progress(curso_id, course_data['total_aulas'])
    
    # Prepare course object for template
    course = {
        'id': course_data['id'],
        'titulo': course_data['titulo'],
        'link': course_data['link'],
        'total_aulas': course_data['total_aulas'],
        'descricao': course_data['descricao'],
        'progress': progress,
        'completed_lessons': completed_lessons,
        'completed_count': len(completed_lessons)
    }
    
    # Create list of all lessons with completion status
    lessons = []
    for lesson_num in range(1, course['total_aulas'] + 1):
        lessons.append({
            'numero': lesson_num,
            'completed': lesson_num in completed_lessons
        })
    
    return render_template('curso_detalhes.html', course=course, lessons=lessons)

@app.route('/toggle_lesson/<int:curso_id>/<int:numero_aula>', methods=['POST'])
def toggle_lesson(curso_id: int, numero_aula: int):
    """
    Toggle lesson completion status.
    
    Args:
        curso_id (int): Course ID
        numero_aula (int): Lesson number
        
    Returns:
        redirect: Redirects back to course details page
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if lesson is already completed
        cursor.execute('''
            SELECT id FROM aulas_concluidas 
            WHERE curso_id = ? AND numero_aula = ?
        ''', (curso_id, numero_aula))
        
        existing = cursor.fetchone()
        
        if existing:
            # Remove completion (mark as incomplete)
            cursor.execute('''
                DELETE FROM aulas_concluidas 
                WHERE curso_id = ? AND numero_aula = ?
            ''', (curso_id, numero_aula))
            flash(f'Aula {numero_aula} marcada como não concluída', 'info')
        else:
            # Add completion (mark as complete)
            cursor.execute('''
                INSERT INTO aulas_concluidas (curso_id, numero_aula)
                VALUES (?, ?)
            ''', (curso_id, numero_aula))
            flash(f'Aula {numero_aula} marcada como concluída!', 'success')
        
        conn.commit()
        
    except sqlite3.Error as e:
        flash(f'Erro ao atualizar aula: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('curso_detalhes', curso_id=curso_id))

@app.route('/atualizar_aula', methods=['POST'])
def atualizar_aula():
    """
    AJAX route to update lesson completion status.
    
    Expected JSON payload:
    {
        "curso_id": int,
        "numero_aula": int,
        "completed": bool
    }
    
    Returns:
        JSON response with success status and updated progress
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados inválidos'
            }), 400
        
        curso_id = data.get('curso_id')
        numero_aula = data.get('numero_aula')
        completed = data.get('completed')
        
        # Validate required fields
        if not all([curso_id, numero_aula]) or completed is None:
            return jsonify({
                'success': False,
                'message': 'Dados obrigatórios faltando'
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify course exists
        cursor.execute('SELECT titulo, total_aulas FROM cursos WHERE id = ?', (curso_id,))
        course = cursor.fetchone()
        
        if not course:
            return jsonify({
                'success': False,
                'message': 'Curso não encontrado'
            }), 404
        
        # Validate lesson number
        if numero_aula < 1 or numero_aula > course['total_aulas']:
            return jsonify({
                'success': False,
                'message': 'Número da aula inválido'
            }), 400
        
        if completed:
            # Add lesson completion
            cursor.execute('''
                INSERT OR IGNORE INTO aulas_concluidas (curso_id, numero_aula)
                VALUES (?, ?)
            ''', (curso_id, numero_aula))
            message = f'Aula {numero_aula} marcada como concluída!'
        else:
            # Remove lesson completion
            cursor.execute('''
                DELETE FROM aulas_concluidas 
                WHERE curso_id = ? AND numero_aula = ?
            ''', (curso_id, numero_aula))
            message = f'Aula {numero_aula} marcada como não concluída'
        
        conn.commit()
        
        # Calculate updated progress
        progress = calculate_course_progress(curso_id, course['total_aulas'])
        completed_count = int((progress / 100) * course['total_aulas'])
        
        conn.close()
        
        return jsonify({
            'success': True,
            'message': message,
            'progress': progress,
            'completed_count': completed_count,
            'total_aulas': course['total_aulas']
        })
        
    except sqlite3.Error as e:
        return jsonify({
            'success': False,
            'message': f'Erro no banco de dados: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@app.route('/deletar_curso/<int:curso_id>', methods=['POST'])
def deletar_curso(curso_id: int):
    """
    Delete a course and all its completed lessons.
    
    Args:
        curso_id (int): Course ID to delete
        
    Returns:
        redirect: Redirects to dashboard
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get course title for confirmation message
        cursor.execute('SELECT titulo FROM cursos WHERE id = ?', (curso_id,))
        course = cursor.fetchone()
        
        if not course:
            flash('Curso não encontrado!', 'error')
            return redirect(url_for('dashboard'))
        
        # Delete completed lessons first (due to foreign key constraint)
        cursor.execute('DELETE FROM aulas_concluidas WHERE curso_id = ?', (curso_id,))
        
        # Delete the course
        cursor.execute('DELETE FROM cursos WHERE id = ?', (curso_id,))
        
        conn.commit()
        flash(f'Curso "{course["titulo"]}" deletado com sucesso!', 'success')
        
    except sqlite3.Error as e:
        flash(f'Erro ao deletar curso: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('dashboard'))

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Check if database exists
    import os
    if not os.path.exists(DATABASE):
        print("❌ Database not found!")
        print("🔧 Please run 'python init_db.py' first to create the database.")
        exit(1)
    
    print("🚀 Starting WebCursos application...")
    print("📊 Dashboard available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)