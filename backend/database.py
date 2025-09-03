import sqlite3
import os
import logging
from config import DATABASE_TYPE, SQLITE_DATABASE_PATH

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        # Permanently use SQLite
        self.db_type = 'sqlite'
        
    def get_connection(self):
        """Get SQLite database connection"""
        try:
            return self._get_sqlite_connection()
        except Exception as e:
            logger.error(f"Erro ao conectar com o banco de dados {self.db_type}: {str(e)}")
            raise Exception(f"Falha na conexão com o banco de dados: {str(e)}")
    
    def _get_sqlite_connection(self):
        """Get SQLite connection"""
        conn = sqlite3.connect(SQLITE_DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA busy_timeout = 30000')
        return conn
    
    def execute_query(self, connection, query, params=None, fetch_one=False, fetch_all=False):
        """Execute query with proper error handling"""
        cursor = None
        try:
            cursor = connection.cursor()
            
            # SQLite execution
            cursor.execute(query, params or ())
            
            if fetch_one:
                result = cursor.fetchone()
                # Convert sqlite3.Row to dict
                if result:
                    if isinstance(result, sqlite3.Row):
                        # Convert to dict properly
                        return dict(zip(result.keys(), result))
                    else:
                        return dict(result)
                else:
                    return None
            elif fetch_all:
                # Convert all sqlite3.Row objects to dicts
                results = cursor.fetchall()
                converted_results = []
                for row in results:
                    if isinstance(row, sqlite3.Row):
                        # Convert to dict properly
                        converted_results.append(dict(zip(row.keys(), row)))
                    else:
                        converted_results.append(dict(row))
                return converted_results
            else:
                return cursor.lastrowid
                    
        except Exception as e:
            logger.error(f"Erro ao executar query: {str(e)}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise e
        finally:
            if cursor:
                cursor.close()

# Global database manager instance
db_manager = DatabaseManager()