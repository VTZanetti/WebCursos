from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

# Inicialização do Flask
app = Flask(__name__)

# Configuração do CORS para permitir requisições do frontend
CORS(app, origins=['http://localhost:3000', 'http://localhost:8080', 'http://127.0.0.1:3000', 'http://127.0.0.1:8080'])

# Configurações do banco de dados
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'database.sqlite')

def get_db_connection():
    """
    Estabelece conexão com o banco de dados SQLite.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
    return conn

def get_curso_aulas_concluidas(cursor, curso_id):
    """
    Retorna o número de aulas concluídas para um curso específico.
    """
    cursor.execute('''
        SELECT COUNT(*) as count 
        FROM aulas_concluidas 
        WHERE curso_id = ?
    ''', (curso_id,))
    result = cursor.fetchone()
    return result['count'] if result else 0

def get_aulas_concluidas_list(cursor, curso_id):
    """
    Retorna lista das aulas concluídas para um curso específico.
    """
    cursor.execute('''
        SELECT numero_aula 
        FROM aulas_concluidas 
        WHERE curso_id = ? 
        ORDER BY numero_aula
    ''', (curso_id,))
    return [row['numero_aula'] for row in cursor.fetchall()]

# ===============================
# ENDPOINTS DA API RESTful
# ===============================

@app.route('/api/cursos', methods=['GET'])
def get_cursos():
    """
    GET /api/cursos - Retorna lista de todos os cursos com número de aulas concluídas.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Buscar todos os cursos
        cursor.execute('''
            SELECT id, titulo, link, total_aulas, anotacoes, created_at, updated_at
            FROM cursos
            ORDER BY created_at DESC
        ''')
        
        cursos = []
        for row in cursor.fetchall():
            curso = dict(row)
            # Calcular aulas concluídas para cada curso
            curso['aulas_concluidas'] = get_curso_aulas_concluidas(cursor, curso['id'])
            # Calcular progresso em percentual
            if curso['total_aulas'] > 0:
                curso['progresso'] = round((curso['aulas_concluidas'] / curso['total_aulas']) * 100, 1)
            else:
                curso['progresso'] = 0.0
            
            cursos.append(curso)
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': cursos,
            'count': len(cursos)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao buscar cursos: {str(e)}'
        }), 500

@app.route('/api/cursos', methods=['POST'])
def create_curso():
    """
    POST /api/cursos - Cria um novo curso.
    Recebe: titulo, link (opcional), total_aulas, anotacoes (opcional)
    """
    try:
        data = request.get_json()
        
        # Validações
        if not data or 'titulo' not in data or 'total_aulas' not in data:
            return jsonify({
                'success': False,
                'error': 'Campos obrigatórios: titulo, total_aulas'
            }), 400
        
        if not isinstance(data['total_aulas'], int) or data['total_aulas'] < 0:
            return jsonify({
                'success': False,
                'error': 'total_aulas deve ser um número inteiro não negativo'
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Inserir novo curso
        cursor.execute('''
            INSERT INTO cursos (titulo, link, total_aulas, anotacoes)
            VALUES (?, ?, ?, ?)
        ''', (
            data['titulo'],
            data.get('link', ''),
            data['total_aulas'],
            data.get('anotacoes', '')
        ))
        
        curso_id = cursor.lastrowid
        
        # Buscar o curso recém-criado para retornar
        cursor.execute('''
            SELECT id, titulo, link, total_aulas, anotacoes, created_at, updated_at
            FROM cursos 
            WHERE id = ?
        ''', (curso_id,))
        
        novo_curso = dict(cursor.fetchone())
        novo_curso['aulas_concluidas'] = 0
        novo_curso['progresso'] = 0.0
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': novo_curso,
            'message': 'Curso criado com sucesso'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao criar curso: {str(e)}'
        }), 500

@app.route('/api/cursos/<int:curso_id>', methods=['GET'])
def get_curso(curso_id):
    """
    GET /api/cursos/<id> - Retorna detalhes de um curso específico com suas aulas concluídas.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Buscar o curso
        cursor.execute('''
            SELECT id, titulo, link, total_aulas, anotacoes, created_at, updated_at
            FROM cursos 
            WHERE id = ?
        ''', (curso_id,))
        
        curso_row = cursor.fetchone()
        if not curso_row:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Curso não encontrado'
            }), 404
        
        curso = dict(curso_row)
        curso['aulas_concluidas'] = get_curso_aulas_concluidas(cursor, curso_id)
        curso['aulas_concluidas_list'] = get_aulas_concluidas_list(cursor, curso_id)
        
        # Calcular progresso
        if curso['total_aulas'] > 0:
            curso['progresso'] = round((curso['aulas_concluidas'] / curso['total_aulas']) * 100, 1)
        else:
            curso['progresso'] = 0.0
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': curso
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao buscar curso: {str(e)}'
        }), 500

@app.route('/api/cursos/<int:curso_id>', methods=['PUT'])
def update_curso(curso_id):
    """
    PUT /api/cursos/<id> - Atualiza informações de um curso.
    Aceita: titulo, link, total_aulas, anotacoes
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado fornecido'
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar se o curso existe
        cursor.execute('SELECT id FROM cursos WHERE id = ?', (curso_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Curso não encontrado'
            }), 404
        
        # Construir query de update dinamicamente
        update_fields = []
        update_values = []
        
        if 'titulo' in data:
            update_fields.append('titulo = ?')
            update_values.append(data['titulo'])
        
        if 'link' in data:
            update_fields.append('link = ?')
            update_values.append(data['link'])
        
        if 'total_aulas' in data:
            if not isinstance(data['total_aulas'], int) or data['total_aulas'] < 0:
                return jsonify({
                    'success': False,
                    'error': 'total_aulas deve ser um número inteiro não negativo'
                }), 400
            update_fields.append('total_aulas = ?')
            update_values.append(data['total_aulas'])
        
        if 'anotacoes' in data:
            update_fields.append('anotacoes = ?')
            update_values.append(data['anotacoes'])
        
        if not update_fields:
            return jsonify({
                'success': False,
                'error': 'Nenhum campo válido para atualizar'
            }), 400
        
        # Adicionar timestamp de atualização
        update_fields.append('updated_at = ?')
        update_values.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Executar update
        update_values.append(curso_id)  # Para a cláusula WHERE
        query = f"UPDATE cursos SET {', '.join(update_fields)} WHERE id = ?"
        
        cursor.execute(query, update_values)
        conn.commit()
        
        # Buscar e retornar o curso atualizado
        cursor.execute('''
            SELECT id, titulo, link, total_aulas, anotacoes, created_at, updated_at
            FROM cursos 
            WHERE id = ?
        ''', (curso_id,))
        
        curso_atualizado = dict(cursor.fetchone())
        curso_atualizado['aulas_concluidas'] = get_curso_aulas_concluidas(cursor, curso_id)
        curso_atualizado['aulas_concluidas_list'] = get_aulas_concluidas_list(cursor, curso_id)
        
        if curso_atualizado['total_aulas'] > 0:
            curso_atualizado['progresso'] = round((curso_atualizado['aulas_concluidas'] / curso_atualizado['total_aulas']) * 100, 1)
        else:
            curso_atualizado['progresso'] = 0.0
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': curso_atualizado,
            'message': 'Curso atualizado com sucesso'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao atualizar curso: {str(e)}'
        }), 500

@app.route('/api/cursos/<int:curso_id>', methods=['DELETE'])
def delete_curso(curso_id):
    """
    DELETE /api/cursos/<id> - Deleta um curso e suas aulas associadas.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar se o curso existe
        cursor.execute('SELECT titulo FROM cursos WHERE id = ?', (curso_id,))
        curso = cursor.fetchone()
        if not curso:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Curso não encontrado'
            }), 404
        
        # Deletar aulas concluídas associadas (CASCADE)
        cursor.execute('DELETE FROM aulas_concluidas WHERE curso_id = ?', (curso_id,))
        
        # Deletar o curso
        cursor.execute('DELETE FROM cursos WHERE id = ?', (curso_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Curso "{curso["titulo"]}" deletado com sucesso'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao deletar curso: {str(e)}'
        }), 500

@app.route('/api/cursos/<int:curso_id>/aula', methods=['POST'])
def toggle_aula_concluida(curso_id):
    """
    POST /api/cursos/<id>/aula - Adiciona ou remove aula da lista de concluídas.
    Recebe: numero_aula, concluida (true/false)
    """
    try:
        data = request.get_json()
        
        if not data or 'numero_aula' not in data or 'concluida' not in data:
            return jsonify({
                'success': False,
                'error': 'Campos obrigatórios: numero_aula, concluida'
            }), 400
        
        numero_aula = data['numero_aula']
        concluida = data['concluida']
        
        if not isinstance(numero_aula, int) or numero_aula <= 0:
            return jsonify({
                'success': False,
                'error': 'numero_aula deve ser um número inteiro positivo'
            }), 400
        
        if not isinstance(concluida, bool):
            return jsonify({
                'success': False,
                'error': 'concluida deve ser true ou false'
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar se o curso existe e obter total de aulas
        cursor.execute('SELECT titulo, total_aulas FROM cursos WHERE id = ?', (curso_id,))
        curso = cursor.fetchone()
        if not curso:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Curso não encontrado'
            }), 404
        
        # Verificar se o número da aula é válido
        if numero_aula > curso['total_aulas']:
            conn.close()
            return jsonify({
                'success': False,
                'error': f'Número da aula ({numero_aula}) não pode ser maior que o total de aulas ({curso["total_aulas"]})'
            }), 400
        
        if concluida:
            # Marcar aula como concluída (inserir se não existir)
            cursor.execute('''
                INSERT OR IGNORE INTO aulas_concluidas (curso_id, numero_aula)
                VALUES (?, ?)
            ''', (curso_id, numero_aula))
            message = f'Aula {numero_aula} marcada como concluída'
        else:
            # Desmarcar aula como concluída (remover se existir)
            cursor.execute('''
                DELETE FROM aulas_concluidas
                WHERE curso_id = ? AND numero_aula = ?
            ''', (curso_id, numero_aula))
            message = f'Aula {numero_aula} desmarcada como concluída'
        
        conn.commit()
        
        # Retornar status atualizado do curso
        total_concluidas = get_curso_aulas_concluidas(cursor, curso_id)
        aulas_concluidas_list = get_aulas_concluidas_list(cursor, curso_id)
        
        progresso = 0.0
        if curso['total_aulas'] > 0:
            progresso = round((total_concluidas / curso['total_aulas']) * 100, 1)
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'curso_id': curso_id,
                'numero_aula': numero_aula,
                'concluida': concluida,
                'total_aulas_concluidas': total_concluidas,
                'aulas_concluidas_list': aulas_concluidas_list,
                'progresso': progresso
            },
            'message': message
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao atualizar aula: {str(e)}'
        }), 500

# ===============================
# ENDPOINTS DE UTILIDADE
# ===============================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Endpoint de verificação de saúde da API.
    """
    return jsonify({
        'success': True,
        'message': 'API funcionando corretamente',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Endpoint para obter estatísticas gerais.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total de cursos
        cursor.execute('SELECT COUNT(*) as count FROM cursos')
        total_cursos = cursor.fetchone()['count']
        
        # Total de aulas concluídas
        cursor.execute('SELECT COUNT(*) as count FROM aulas_concluidas')
        total_aulas_concluidas = cursor.fetchone()['count']
        
        # Total de aulas disponíveis
        cursor.execute('SELECT SUM(total_aulas) as sum FROM cursos')
        total_aulas_disponiveis = cursor.fetchone()['sum'] or 0
        
        # Progresso geral
        progresso_geral = 0.0
        if total_aulas_disponiveis > 0:
            progresso_geral = round((total_aulas_concluidas / total_aulas_disponiveis) * 100, 1)
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'total_cursos': total_cursos,
                'total_aulas_concluidas': total_aulas_concluidas,
                'total_aulas_disponiveis': total_aulas_disponiveis,
                'progresso_geral': progresso_geral
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao obter estatísticas: {str(e)}'
        }), 500

# ===============================
# TRATAMENTO DE ERROS
# ===============================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint não encontrado'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 'Método não permitido'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Erro interno do servidor'
    }), 500

# ===============================
# INICIALIZAÇÃO
# ===============================

if __name__ == '__main__':
    # Verificar se o banco de dados existe, se não, criar
    if not os.path.exists(DATABASE_PATH):
        print("Banco de dados não encontrado. Executando inicialização...")
        from init_db import init_database
        init_database()
    
    print("🚀 Iniciando API do WebCurso...")
    print("📊 Endpoints disponíveis:")
    print("   GET    /api/cursos          - Listar cursos")
    print("   POST   /api/cursos          - Criar curso")
    print("   GET    /api/cursos/<id>     - Detalhes do curso")
    print("   PUT    /api/cursos/<id>     - Atualizar curso")
    print("   DELETE /api/cursos/<id>     - Deletar curso")
    print("   POST   /api/cursos/<id>/aula - Controlar aulas concluídas")
    print("   GET    /api/health          - Status da API")
    print("   GET    /api/stats           - Estatísticas gerais")
    print()
    print("🌐 CORS habilitado para:")
    print("   - http://localhost:3000")
    print("   - http://localhost:8080")
    print("   - http://127.0.0.1:3000")
    print("   - http://127.0.0.1:8080")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)