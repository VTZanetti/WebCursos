#!/usr/bin/env python3
"""
WebCurso Database Initialization Script
======================================

This script initializes the database for the WebCurso application.
It handles both SQLite and MySQL database backends.
"""

import logging
import sys
import os
from config import DATABASE_TYPE

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to initialize the correct database"""
    print(f"🚀 Inicializando banco de dados {DATABASE_TYPE.upper()} do WebCurso...")
    print("=" * 50)
    
    # Import the appropriate initialization module based on database type
    if DATABASE_TYPE == 'mysql':
        try:
            # Try to import mysql_connector for checking
            import mysql.connector
            from init_mysql_db import main as init_mysql
            init_mysql()
        except ImportError:
            logger.error("Erro: MySQL libraries não instaladas")
            print("\n❌ Erro: MySQL libraries não instaladas")
            print("\n🔧 Por favor, execute setup_mysql.bat primeiro para instalar as dependências")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Erro ao inicializar MySQL: {str(e)}")
            print(f"\n❌ Erro: {str(e)}")
            print("\n🔧 Considere usar SQLite como alternativa:")
            print("   set DATABASE_TYPE=sqlite")
            print("   python init_db.py")
            sys.exit(1)
    else:
        # Use SQLite (default/fallback option)
        try:
            import sqlite3
            from init_db import init_database
            init_database()
            
            # Show success message
            print("\n✅ Banco de dados SQLite inicializado com sucesso!")
            print("   SQLite é ideal para desenvolvimento e uso pessoal.")
            print("   Não requer configuração adicional de servidor.\n")
            print("Para iniciar o servidor com SQLite:")
            print("   start_sqlite_server.bat")
        except Exception as e:
            logger.error(f"Erro ao inicializar SQLite: {str(e)}")
            print(f"\n❌ Erro ao inicializar SQLite: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    main()