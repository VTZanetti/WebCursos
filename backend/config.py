# Database Configuration
import os

# Database choice: permanently set to 'sqlite'
DATABASE_TYPE = 'sqlite'

# SQLite Configuration - permanent location
SQLITE_DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'database.sqlite')

# Removed MySQL Configuration as it's no longer needed

def get_mysql_url():
    """Placeholder function to avoid errors - not used with SQLite"""
    return None