from flask import Flask, request, jsonify
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicialização do Flask
app = Flask(__name__)

# Configuração robusta do CORS para Vue.js dev server
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173",  # Vite default port
            "http://127.0.0.1:5173", # Alternative localhost
            "http://localhost:3000",  # Backup port
            "http://127.0.0.1:3000"  # Backup alternative
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"]
    }
})

# Configurações do banco de dados
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'database.sqlite')

# ===============================
# HELPER FUNCTIONS
# ===============================

def create_error_response(message, status_code=500, details=None):
    """
    Cria uma resposta de erro padronizada.
    """
    error_data = {
        'success': False,
        'error': message,
        'timestamp': datetime.now().isoformat()
    }
    
    if details:
        error_data['details'] = details
        
    if status_code >= 500:
        logger.error(f"Server Error {status_code}: {message} - Details: {details}")
    else:
        logger.warning(f"Client Error {status_code}: {message}")
        
    return jsonify(error_data), status_code

def create_success_response(data, message=None, status_code=200):
    """
    Cria uma resposta de sucesso padronizada.
    """
    response_data = {
        'success': True,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }
    
    if message:
        response_data['message'] = message
        
    return jsonify(response_data), status_code

def get_db_connection():
    """
    Estabelece conexão com o banco de dados SQLite com tratamento de erros.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
        
        # Configurar timeout para evitar deadlocks
        conn.execute('PRAGMA busy_timeout = 30000')  # 30 seconds
        
        return conn
    except sqlite3.Error as e:
        logger.error(f"Erro ao conectar com o banco de dados: {str(e)}")
        raise Exception(f"Falha na conexão com o banco de dados: {str(e)}")
    except Exception as e:
        logger.error(f"Erro inesperado ao conectar com o banco: {str(e)}")
        raise Exception(f"Erro interno ao acessar o banco de dados")

def get_curso_aulas_concluidas(cursor, curso_id):
    """
    Retorna o número de aulas concluídas para um curso específico.
    """
    try:
        cursor.execute('''
            SELECT COUNT(*) as count 
            FROM aulas_concluidas 
            WHERE curso_id = ?
        ''', (curso_id,))
        result = cursor.fetchone()
        return result['count'] if result else 0
    except sqlite3.Error as e:
        logger.error(f"Erro ao buscar aulas concluídas para curso {curso_id}: {str(e)}")
        raise Exception(f"Erro ao consultar aulas concluídas")

def get_aulas_concluidas_list(cursor, curso_id):
    """
    Retorna lista das aulas concluídas para um curso específico.
    """
    try:
        cursor.execute('''
            SELECT numero_aula 
            FROM aulas_concluidas 
            WHERE curso_id = ? 
            ORDER BY numero_aula
        ''', (curso_id,))
        return [row['numero_aula'] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        logger.error(f"Erro ao buscar lista de aulas concluídas para curso {curso_id}: {str(e)}")
        raise Exception(f"Erro ao consultar lista de aulas")

# ===============================
# ENDPOINTS DA API RESTful
# ===============================

@app.route('/api/cursos', methods=['GET'])
def get_cursos():
    """
    GET /api/cursos - Retorna lista de todos os cursos com número de aulas concluídas.
    """
    conn = None
    try:
        logger.info("Buscando lista de cursos")
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
        
        logger.info(f"Retornando {len(cursos)} cursos")
        return create_success_response({
            'cursos': cursos,
            'count': len(cursos)
        })
        
    except sqlite3.Error as db_error:
        logger.error(f"Erro no banco de dados ao buscar cursos: {str(db_error)}")
        return create_error_response(
            "Erro ao acessar o banco de dados",
            500,
            "Falha na consulta dos cursos"
        )
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar cursos: {str(e)}")
        return create_error_response(
            "Erro interno do servidor ao buscar cursos",
            500
        )
    finally:
        if conn:
            try:
                conn.close()
            except Exception as close_error:
                logger.error(f"Erro ao fechar conexão: {str(close_error)}")

@app.route('/api/cursos', methods=['POST'])
def create_curso():
    """
    POST /api/cursos - Cria um novo curso.
    Recebe: titulo, link (opcional), total_aulas, anotacoes (opcional)
    """
    conn = None
    try:
        data = request.get_json()
        logger.info(f"Tentativa de criar novo curso: {data.get('titulo') if data else 'dados inválidos'}")
        
        # Validações de entrada
        if not data:
            return create_error_response(
                "Nenhum dado fornecido",
                400,
                "Corpo da requisição vazio ou inválido"
            )
            
        if 'titulo' not in data or not data['titulo']:
            return create_error_response(
                "Título é obrigatório",
                400,
                "Campo 'titulo' ausente ou vazio"
            )
            
        if 'total_aulas' not in data:
            return create_error_response(
                "Total de aulas é obrigatório",
                400,
                "Campo 'total_aulas' ausente"
            )
        
        if not isinstance(data['total_aulas'], int) or data['total_aulas'] < 0:
            return create_error_response(
                "Total de aulas deve ser um número inteiro não negativo",
                400,
                f"Valor recebido: {data['total_aulas']}"
            )
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Inserir novo curso
        cursor.execute('''
            INSERT INTO cursos (titulo, link, total_aulas, anotacoes)
            VALUES (?, ?, ?, ?)
        ''', (
            data['titulo'].strip(),
            data.get('link', '').strip(),
            data['total_aulas'],
            data.get('anotacoes', '').strip()
        ))
        
        curso_id = cursor.lastrowid
        
        # Buscar o curso recém-criado para retornar
        cursor.execute('''
            SELECT id, titulo, link, total_aulas, anotacoes, created_at, updated_at
            FROM cursos 
            WHERE id = ?
        ''', (curso_id,))
        
        curso_row = cursor.fetchone()
        if not curso_row:
            raise Exception("Falha ao recuperar o curso criado")
            
        novo_curso = dict(curso_row)
        novo_curso['aulas_concluidas'] = 0
        novo_curso['progresso'] = 0.0
        
        conn.commit()
        logger.info(f"Curso criado com sucesso: ID {curso_id} - {data['titulo']}")
        
        return create_success_response(
            novo_curso,
            "Curso criado com sucesso",
            201
        )
        
    except sqlite3.IntegrityError as integrity_error:
        logger.error(f"Erro de integridade ao criar curso: {str(integrity_error)}")
        return create_error_response(
            "Erro de validação dos dados",
            400,
            "Possível duplicação de dados ou violação de restrições"
        )
    except sqlite3.Error as db_error:
        logger.error(f"Erro no banco de dados ao criar curso: {str(db_error)}")
        return create_error_response(
            "Erro ao salvar curso no banco de dados",
            500,
            "Falha na operação de inserção"
        )
    except Exception as e:
        logger.error(f"Erro inesperado ao criar curso: {str(e)}")
        return create_error_response(
            "Erro interno do servidor ao criar curso",
            500
        )
    finally:
        if conn:
            try:
                conn.close()
            except Exception as close_error:
                logger.error(f"Erro ao fechar conexão: {str(close_error)}")

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