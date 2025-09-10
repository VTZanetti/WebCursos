import sqlite3
import os

def init_database():
    """
    Inicializa o banco de dados SQLite criando as tabelas necessárias.
    """
    # Garante que o diretório instance existe
    instance_path = os.path.join(os.path.dirname(__file__), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    
    # Caminho do banco de dados
    db_path = os.path.join(instance_path, 'database.sqlite')
    
    # Conecta ao banco de dados (cria o arquivo se não existir)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Criação da tabela cursos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            link TEXT,
            total_aulas INTEGER NOT NULL DEFAULT 0,
            anotacoes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Criação da tabela aulas_concluidas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aulas_concluidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            curso_id INTEGER NOT NULL,
            numero_aula INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (curso_id) REFERENCES cursos (id) ON DELETE CASCADE,
            UNIQUE(curso_id, numero_aula)
        )
    ''')
    
    # Criar índices para melhor performance
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_aulas_concluidas_curso_id 
        ON aulas_concluidas (curso_id)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_aulas_concluidas_numero_aula 
        ON aulas_concluidas (numero_aula)
    ''')
    
    # Commit das mudanças
    conn.commit()
    
    print(f"Banco de dados inicializado em: {db_path}")
    print("Tabelas criadas:")
    print("- cursos (id, titulo, link, total_aulas, anotacoes, created_at, updated_at)")
    print("- aulas_concluidas (id, curso_id, numero_aula, created_at)")
    
    # Inserir alguns dados de exemplo (opcional)
    cursor.execute("SELECT COUNT(*) FROM cursos")
    if cursor.fetchone()[0] == 0:
        print("\nInserindo dados de exemplo...")
        cursor.execute('''
            INSERT INTO cursos (titulo, link, total_aulas, anotacoes)
            VALUES (?, ?, ?, ?)
        ''', ('Curso de Python Avançado', 'https://exemplo.com/python', 30, 'Curso excelente para backend'))
        
        cursor.execute('''
            INSERT INTO cursos (titulo, link, total_aulas, anotacoes)
            VALUES (?, ?, ?, ?)
        ''', ('Curso de Vue.js', 'https://exemplo.com/vue', 25, 'Framework frontend moderno'))
        
        # Marcar algumas aulas como concluídas
        cursor.execute('''
            INSERT INTO aulas_concluidas (curso_id, numero_aula)
            VALUES (1, 1), (1, 2), (1, 3), (2, 1)
        ''')
        
        conn.commit()
        print("Dados de exemplo inseridos!")
    
    conn.close()

if __name__ == '__main__':
    init_database()