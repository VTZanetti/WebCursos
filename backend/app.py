from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from datetime import datetime
from database import db_manager
from config import DATABASE_TYPE

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
            "http://localhost:3000",  # Common port
            "http://127.0.0.1:3000",  # Alternative
            "http://localhost:3001",  # Frontend port
            "http://127.0.0.1:3001",  # Alternative
            "http://localhost:3002",  # Frontend port (vite dev)
            "http://127.0.0.1:3002",  # Alternative
            "http://localhost:3003",  # Backup port
            "http://127.0.0.1:3003",  # Alternative
            "http://localhost:3004",  # Backup port
            "http://127.0.0.1:3004",  # Alternative
            "http://localhost:8080",  # Alternative port
            "http://127.0.0.1:8080"   # Alternative
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"]
    }
})

# Configurações do banco de dados
logger.info(f"Usando banco de dados: {DATABASE_TYPE.upper()}")

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
    Estabelece conexão com o banco de dados com tratamento de erros.
    """
    try:
        return db_manager.get_connection()
    except Exception as e:
        logger.error(f"Erro ao conectar com o banco de dados: {str(e)}")
        raise Exception(f"Falha na conexão com o banco de dados: {str(e)}")

def get_curso_aulas_concluidas(connection, curso_id):
    """
    Retorna o número de aulas concluídas para um curso específico.
    """
    try:
        # Simplified for SQLite only
        query = "SELECT COUNT(*) as count FROM aulas_concluidas WHERE curso_id = ?"
        result = db_manager.execute_query(connection, query, (curso_id,), fetch_one=True)
        return result['count'] if result else 0
    except Exception as e:
        logger.error(f"Erro ao buscar aulas concluídas para curso {curso_id}: {str(e)}")
        raise Exception(f"Erro ao consultar aulas concluídas")

def get_aulas_concluidas_list(connection, curso_id):
    """
    Retorna lista das aulas concluídas para um curso específico.
    """
    try:
        # Simplified for SQLite only
        query = "SELECT numero_aula FROM aulas_concluidas WHERE curso_id = ? ORDER BY numero_aula"
        results = db_manager.execute_query(connection, query, (curso_id,), fetch_all=True)
        return [row['numero_aula'] for row in results] if results else []
    except Exception as e:
        logger.error(f"Erro ao buscar lista de aulas concluídas para curso {curso_id}: {str(e)}")
        raise Exception(f"Erro ao consultar lista de aulas")

def calcular_estimativas_tempo(curso):
    """
    Calcula estimativas de tempo baseadas na carga horária do curso.
    """
    try:
        horas = curso.get('horas', 0) or 0
        minutos = curso.get('minutos', 0) or 0
        total_aulas = curso.get('total_aulas', 0) or 0
        aulas_concluidas = curso.get('aulas_concluidas', 0) or 0
        
        # Converter tudo para minutos para cálculos
        duracao_total_minutos = (horas * 60) + minutos
        
        # Calcular duração por aula em minutos
        if total_aulas > 0 and duracao_total_minutos > 0:
            duracao_por_aula_minutos = duracao_total_minutos / total_aulas
        else:
            duracao_por_aula_minutos = 0
        
        # Calcular tempo restante
        aulas_restantes = max(0, total_aulas - aulas_concluidas)
        tempo_restante_minutos = aulas_restantes * duracao_por_aula_minutos
        
        # Converter de volta para horas e minutos
        def minutos_para_horas_minutos(total_minutos):
            if total_minutos <= 0:
                return {'horas': 0, 'minutos': 0}
            h = int(total_minutos // 60)
            m = int(total_minutos % 60)
            return {'horas': h, 'minutos': m}
        
        # Adicionar campos calculados
        curso['duracao_total'] = {
            'horas': horas,
            'minutos': minutos,
            'total_minutos': duracao_total_minutos
        }
        
        curso['duracao_por_aula'] = minutos_para_horas_minutos(duracao_por_aula_minutos)
        curso['duracao_por_aula']['total_minutos'] = duracao_por_aula_minutos
        
        curso['tempo_restante'] = minutos_para_horas_minutos(tempo_restante_minutos)
        curso['tempo_restante']['total_minutos'] = tempo_restante_minutos
        
        # Formatacao amigável
        def formatar_duracao(duracao_obj):
            h = duracao_obj['horas']
            m = duracao_obj['minutos']
            if h > 0 and m > 0:
                return f"{h}h {m}min"
            elif h > 0:
                return f"{h}h"
            elif m > 0:
                return f"{m}min"
            else:
                return "0min"
        
        curso['duracao_total_formatada'] = formatar_duracao(curso['duracao_total'])
        curso['duracao_por_aula_formatada'] = formatar_duracao(curso['duracao_por_aula'])
        curso['tempo_restante_formatado'] = formatar_duracao(curso['tempo_restante'])
        
        return curso
        
    except Exception as e:
        logger.error(f"Erro ao calcular estimativas de tempo: {str(e)}")
        # Retornar valores padrão em caso de erro
        curso['duracao_total'] = {'horas': 0, 'minutos': 0, 'total_minutos': 0}
        curso['duracao_por_aula'] = {'horas': 0, 'minutos': 0, 'total_minutos': 0}
        curso['tempo_restante'] = {'horas': 0, 'minutos': 0, 'total_minutos': 0}
        curso['duracao_total_formatada'] = '0min'
        curso['duracao_por_aula_formatada'] = '0min'
        curso['tempo_restante_formatado'] = '0min'
        return curso

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
        
        # Buscar todos os cursos
        query = "SELECT id, titulo, link, total_aulas, anotacoes, horas, minutos, created_at, updated_at FROM cursos ORDER BY created_at DESC"
        cursos_data = db_manager.execute_query(conn, query, fetch_all=True)
        
        cursos = []
        for curso in cursos_data:
            # Calcular aulas concluídas para cada curso
            curso['aulas_concluidas'] = get_curso_aulas_concluidas(conn, curso['id'])
            # Calcular progresso em percentual
            if curso['total_aulas'] > 0:
                curso['progresso'] = round((curso['aulas_concluidas'] / curso['total_aulas']) * 100, 1)
            else:
                curso['progresso'] = 0.0
            
            # Calcular estimativas de tempo
            curso = calcular_estimativas_tempo(curso)
            
            cursos.append(curso)
        
        logger.info(f"Retornando {len(cursos)} cursos")
        return create_success_response({
            'cursos': cursos,
            'count': len(cursos)
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar cursos: {str(e)}")
        return create_error_response(
            "Erro ao acessar o banco de dados",
            500,
            "Falha na consulta dos cursos"
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
        
        # Validar horas e minutos (opcionais)
        horas = data.get('horas', 0)
        minutos = data.get('minutos', 0)
        
        if horas is not None and (not isinstance(horas, int) or horas < 0):
            return create_error_response(
                "Horas deve ser um número inteiro não negativo",
                400,
                f"Valor recebido: {horas}"
            )
            
        if minutos is not None and (not isinstance(minutos, int) or minutos < 0 or minutos >= 60):
            return create_error_response(
                "Minutos deve ser um número inteiro entre 0 e 59",
                400,
                f"Valor recebido: {minutos}"
            )
        
        conn = get_db_connection()
        
        # Inserir novo curso - simplified for SQLite
        insert_query = "INSERT INTO cursos (titulo, link, total_aulas, anotacoes, horas, minutos) VALUES (?, ?, ?, ?, ?, ?)"
        
        curso_id = db_manager.execute_query(
            conn,
            insert_query,
            (
                data['titulo'].strip(),
                data.get('link', '').strip(),
                data['total_aulas'],
                data.get('anotacoes', '').strip(),
                horas or 0,
                minutos or 0
            )
        )
        
        # Commit the transaction
        conn.commit()
        
        # Buscar o curso recém-criado para retornar
        select_query = "SELECT id, titulo, link, total_aulas, anotacoes, horas, minutos, created_at, updated_at FROM cursos WHERE id = ?"
        
        curso_row = db_manager.execute_query(conn, select_query, (curso_id,), fetch_one=True)
        
        if not curso_row:
            raise Exception("Falha ao recuperar o curso criado")
            
        novo_curso = curso_row
        novo_curso['aulas_concluidas'] = 0
        novo_curso['progresso'] = 0.0
        
        # Calcular estimativas de tempo
        novo_curso = calcular_estimativas_tempo(novo_curso)
        
        logger.info(f"Curso criado com sucesso: ID {curso_id} - {data['titulo']}")
        
        return create_success_response(
            novo_curso,
            "Curso criado com sucesso",
            201
        )
        
    except Exception as e:
        logger.error(f"Erro ao criar curso: {str(e)}")
        return create_error_response(
            "Erro ao salvar curso no banco de dados",
            500,
            str(e)
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
        
        # Buscar o curso
        query = "SELECT id, titulo, link, total_aulas, anotacoes, horas, minutos, created_at, updated_at FROM cursos WHERE id = ?"
        curso_row = db_manager.execute_query(conn, query, (curso_id,), fetch_one=True)
        
        if not curso_row:
            conn.close()
            return create_error_response("Curso não encontrado", 404)
        
        curso = curso_row
        curso['aulas_concluidas'] = get_curso_aulas_concluidas(conn, curso_id)
        curso['aulas_concluidas_list'] = get_aulas_concluidas_list(conn, curso_id)
        
        # Calcular progresso
        if curso['total_aulas'] > 0:
            curso['progresso'] = round((curso['aulas_concluidas'] / curso['total_aulas']) * 100, 1)
        else:
            curso['progresso'] = 0.0
            
        # Calcular estimativas de tempo
        curso = calcular_estimativas_tempo(curso)
        
        conn.close()
        return create_success_response(curso)
        
    except Exception as e:
        logger.error(f"Erro ao buscar curso {curso_id}: {str(e)}")
        return create_error_response(
            "Erro ao acessar o banco de dados",
            500,
            str(e)
        )

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
            
        if 'horas' in data:
            if not isinstance(data['horas'], int) or data['horas'] < 0:
                return jsonify({
                    'success': False,
                    'error': 'horas deve ser um número inteiro não negativo'
                }), 400
            update_fields.append('horas = ?')
            update_values.append(data['horas'])
            
        if 'minutos' in data:
            if not isinstance(data['minutos'], int) or data['minutos'] < 0 or data['minutos'] >= 60:
                return jsonify({
                    'success': False,
                    'error': 'minutos deve ser um número inteiro entre 0 e 59'
                }), 400
            update_fields.append('minutos = ?')
            update_values.append(data['minutos'])
        
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
        cursor.close()  # Close the cursor after use
        
        # Buscar e retornar o curso atualizado
        cursor = conn.cursor()  # Create a new cursor for the next query
        cursor.execute('''
            SELECT id, titulo, link, total_aulas, anotacoes, horas, minutos, created_at, updated_at
            FROM cursos 
            WHERE id = ?
        ''', (curso_id,))
        
        curso_atualizado = dict(cursor.fetchone())
        curso_atualizado['aulas_concluidas'] = get_curso_aulas_concluidas(conn, curso_id)
        curso_atualizado['aulas_concluidas_list'] = get_aulas_concluidas_list(conn, curso_id)
        
        if curso_atualizado['total_aulas'] > 0:
            curso_atualizado['progresso'] = round((curso_atualizado['aulas_concluidas'] / curso_atualizado['total_aulas']) * 100, 1)
        else:
            curso_atualizado['progresso'] = 0.0
            
        # Calcular estimativas de tempo
        curso_atualizado = calcular_estimativas_tempo(curso_atualizado)
            
        cursor.close()
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
        cursor.close()  # Close the cursor after use
        
        # Retornar status atualizado do curso
        total_concluidas = get_curso_aulas_concluidas(conn, curso_id)
        aulas_concluidas_list = get_aulas_concluidas_list(conn, curso_id)
        
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

@app.route('/api/cursos/<int:curso_id>/aulas/batch', methods=['POST'])
def batch_toggle_aulas_concluidas(curso_id):
    """
    POST /api/cursos/<id>/aulas/batch - Marca ou desmarca múltiplas aulas como concluídas em lote.
    Recebe: aulas (array de objetos com numero_aula e concluida)
    """
    try:
        data = request.get_json()
        
        if not data or 'aulas' not in data or not isinstance(data['aulas'], list):
            return create_error_response(
                'Campo obrigatório: aulas (array de objetos com numero_aula e concluida)',
                400
            )
        
        if len(data['aulas']) == 0:
            return create_error_response(
                'Array de aulas não pode estar vazio',
                400
            )
        
        # Validate each aula object
        for aula in data['aulas']:
            if not isinstance(aula, dict) or 'numero_aula' not in aula or 'concluida' not in aula:
                return create_error_response(
                    'Cada item em aulas deve ter numero_aula e concluida',
                    400
                )
            
            numero_aula = aula['numero_aula']
            concluida = aula['concluida']
            
            if not isinstance(numero_aula, int) or numero_aula <= 0:
                return create_error_response(
                    'numero_aula deve ser um número inteiro positivo',
                    400
                )
            
            if not isinstance(concluida, bool):
                return create_error_response(
                    'concluida deve ser true ou false',
                    400
                )
        
        conn = get_db_connection()
        
        # Verificar se o curso existe e obter total de aulas
        query = "SELECT titulo, total_aulas FROM cursos WHERE id = ?"
        curso = db_manager.execute_query(conn, query, (curso_id,), fetch_one=True)
        if not curso:
            conn.close()
            return create_error_response("Curso não encontrado", 404)
        
        # Validate all aula numbers
        for aula in data['aulas']:
            numero_aula = aula['numero_aula']
            if numero_aula > curso['total_aulas']:
                conn.close()
                return create_error_response(
                    f'Número da aula ({numero_aula}) não pode ser maior que o total de aulas ({curso["total_aulas"]})',
                    400
                )
        
        # Process all aulas in a single transaction
        cursor = conn.cursor()
        updated_aulas = []
        
        for aula in data['aulas']:
            numero_aula = aula['numero_aula']
            concluida = aula['concluida']
            
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
            
            updated_aulas.append({
                'numero_aula': numero_aula,
                'concluida': concluida,
                'message': message
            })
        
        conn.commit()
        cursor.close()
        
        # Get updated course status
        total_concluidas = get_curso_aulas_concluidas(conn, curso_id)
        aulas_concluidas_list = get_aulas_concluidas_list(conn, curso_id)
        
        progresso = 0.0
        if curso['total_aulas'] > 0:
            progresso = round((total_concluidas / curso['total_aulas']) * 100, 1)
        
        conn.close()
        
        return create_success_response({
            'curso_id': curso_id,
            'updated_aulas': updated_aulas,
            'total_aulas_concluidas': total_concluidas,
            'aulas_concluidas_list': aulas_concluidas_list,
            'progresso': progresso
        }, 'Aulas atualizadas com sucesso')
        
    except Exception as e:
        logger.error(f"Erro ao atualizar aulas em lote: {str(e)}")
        return create_error_response(
            f'Erro ao atualizar aulas: {str(e)}',
            500
        )

# ===============================
# ENDPOINTS DE UTILIDADE
# ===============================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Endpoint de verificação de saúde da API.
    """
    try:
        # Tentar conexão com banco
        conn = get_db_connection()
        
        # Apenas verificar conexão, sem queries complexas
        query = "SELECT 1" if DATABASE_TYPE == 'mysql' else "SELECT 1"
        result = db_manager.execute_query(conn, query, fetch_one=True)
        
        # Fechar conexão após teste
        conn.close()
        
        # Informações de status
        return jsonify({
            'success': True,
            'message': 'API funcionando corretamente',
            'database_type': DATABASE_TYPE,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Health check falhou: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'API está online, mas há problemas com o banco de dados',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 503

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
    # Check database configuration
    from config import DATABASE_TYPE
    logger.info(f"Starting WebCurso API with {DATABASE_TYPE.upper()} database")
    
    # Initialize database if needed
    try:
        from init_db import init_database
        init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
    
    # Run the Flask application
    # Make it accessible from outside the container
    app.run(debug=False, host='0.0.0.0', port=5000)
