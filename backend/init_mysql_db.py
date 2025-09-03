#!/usr/bin/env python3
"""
WebCurso MySQL Database Initialization Script
==============================================

This script initializes the MySQL database for the WebCurso application.
It creates the necessary tables and inserts sample data.

Requirements:
- MySQL server running on localhost
- Root user with no password (or configure MYSQL_* environment variables)
"""

import logging
import sys
from datetime import datetime
from database import db_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_tables(connection):
    """Create the necessary tables for WebCurso"""
    
    # Table: cursos
    cursos_table = """
    CREATE TABLE IF NOT EXISTS cursos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        titulo VARCHAR(200) NOT NULL,
        link VARCHAR(500) DEFAULT '',
        total_aulas INT NOT NULL DEFAULT 0,
        anotacoes TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_titulo (titulo),
        INDEX idx_created_at (created_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
    
    # Table: aulas_concluidas
    aulas_table = """
    CREATE TABLE IF NOT EXISTS aulas_concluidas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        curso_id INT NOT NULL,
        numero_aula INT NOT NULL,
        data_conclusao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
        UNIQUE KEY unique_aula_curso (curso_id, numero_aula),
        INDEX idx_curso_id (curso_id),
        INDEX idx_numero_aula (numero_aula)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
    
    try:
        logger.info("Criando tabela 'cursos'...")
        db_manager.execute_query(connection, cursos_table)
        logger.info("✓ Tabela 'cursos' criada com sucesso")
        
        logger.info("Criando tabela 'aulas_concluidas'...")
        db_manager.execute_query(connection, aulas_table)
        logger.info("✓ Tabela 'aulas_concluidas' criada com sucesso")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {str(e)}")
        return False

def insert_sample_data(connection):
    """Insert sample course data"""
    
    sample_courses = [
        {
            'titulo': 'Vue.js 3 - Do Zero ao Avançado',
            'link': 'https://exemplo.com/vue-curso',
            'total_aulas': 45,
            'anotacoes': 'Curso completo de Vue.js 3 com Composition API, Pinia e TypeScript'
        },
        {
            'titulo': 'Python para Análise de Dados',
            'link': 'https://exemplo.com/python-data',
            'total_aulas': 32,
            'anotacoes': 'Pandas, NumPy, Matplotlib e projetos práticos de análise'
        },
        {
            'titulo': 'MySQL Avançado e Otimização',
            'link': 'https://exemplo.com/mysql-avancado',
            'total_aulas': 28,
            'anotacoes': 'Técnicas avançadas de otimização, índices e performance'
        }
    ]
    
    try:
        for i, course in enumerate(sample_courses, 1):
            logger.info(f"Inserindo curso {i}: {course['titulo']}")
            
            curso_id = db_manager.execute_query(
                connection,
                """INSERT INTO cursos (titulo, link, total_aulas, anotacoes) 
                   VALUES (%s, %s, %s, %s)""",
                (course['titulo'], course['link'], course['total_aulas'], course['anotacoes'])
            )
            
            # Add some completed lessons for demonstration
            completed_lessons = [1, 2, 3, 5, 8] if i == 1 else [1, 2] if i == 2 else [1]
            
            for lesson_num in completed_lessons:
                if lesson_num <= course['total_aulas']:
                    db_manager.execute_query(
                        connection,
                        "INSERT INTO aulas_concluidas (curso_id, numero_aula) VALUES (%s, %s)",
                        (curso_id, lesson_num)
                    )
            
            logger.info(f"✓ Curso '{course['titulo']}' inserido com {len(completed_lessons)} aulas concluídas")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao inserir dados de exemplo: {str(e)}")
        return False

def get_database_info(connection):
    """Get database statistics"""
    try:
        # Count courses
        courses = db_manager.execute_query(
            connection,
            "SELECT COUNT(*) as count FROM cursos",
            fetch_one=True
        )
        
        # Count completed lessons
        lessons = db_manager.execute_query(
            connection,
            "SELECT COUNT(*) as count FROM aulas_concluidas",
            fetch_one=True
        )
        
        # Get table info
        tables = db_manager.execute_query(
            connection,
            "SHOW TABLES",
            fetch_all=True
        )
        
        return {
            'total_courses': courses['count'] if courses else 0,
            'total_completed_lessons': lessons['count'] if lessons else 0,
            'tables': [list(table.values())[0] for table in tables] if tables else []
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter informações do banco: {str(e)}")
        return None

def main():
    """Main initialization function"""
    print("🚀 Inicializando banco de dados MySQL do WebCurso...")
    print("=" * 50)
    
    try:
        # Test database connection
        logger.info("Testando conexão com MySQL...")
        connection = db_manager.get_connection()
        logger.info("✓ Conexão com MySQL estabelecida com sucesso")
        
        # Create tables
        logger.info("\nCriando estrutura do banco de dados...")
        if not create_tables(connection):
            logger.error("Falha ao criar tabelas")
            sys.exit(1)
        
        # Insert sample data
        logger.info("\nInserindo dados de exemplo...")
        if not insert_sample_data(connection):
            logger.error("Falha ao inserir dados de exemplo")
            sys.exit(1)
        
        # Get database info
        logger.info("\nColetando informações do banco...")
        db_info = get_database_info(connection)
        
        if db_info:
            print("\n" + "=" * 50)
            print("✅ Banco de dados MySQL inicializado com sucesso!")
            print("=" * 50)
            print(f"📊 Estatísticas:")
            print(f"   • Total de cursos: {db_info['total_courses']}")
            print(f"   • Total de aulas concluídas: {db_info['total_completed_lessons']}")
            print(f"   • Tabelas criadas: {', '.join(db_info['tables'])}")
            print("\n🔌 Configuração de conexão:")
            print(f"   • Host: {db_manager.db_type == 'mysql' and 'localhost' or 'SQLite'}")
            print(f"   • Database: webcurso")
            print(f"   • User: root")
            print(f"   • Password: (sem senha)")
            
            print("\n🚀 Para iniciar a aplicação:")
            print("   python app.py")
            
            print("\n📊 Para acessar via Navicat:")
            print("   • Host: localhost")
            print("   • Port: 3306")
            print("   • Username: root")
            print("   • Password: (deixe em branco)")
            print("   • Database: webcurso")
        
        connection.close()
        
    except Exception as e:
        logger.error(f"Erro durante a inicialização: {str(e)}")
        print(f"\n❌ Erro: {str(e)}")
        print("\n🔧 Soluções possíveis:")
        print("   1. Verifique se o MySQL está rodando")
        print("   2. Verifique se o usuário 'root' tem permissões")
        print("   3. Instale as dependências: pip install mysql-connector-python pymysql")
        sys.exit(1)

if __name__ == "__main__":
    main()