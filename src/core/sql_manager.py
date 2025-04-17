# src/core/sql_manager.py
import pyodbc
from utils.colors import print_success, print_fail

class SQLManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.connection = None
        self.sql_config = self.config_manager.get_special_config("SQL")
        if self.check_auth():
            self.connect()

    def check_auth(self):
        if int( self.sql_config.get('connect_sql', 0)) != 0:
            return True
        return False

    def connect(self):
        self.sql_config = self.config_manager.get_special_config("SQL")
        try:
            conn_str = (
                f"DRIVER={sql_config.get('driver', 'SQL Server')};"
                f"SERVER={sql_config.get('host', 'localhost')};"
                f"DATABASE={sql_config.get('database', 'SRO_VT_ACCOUNT')};"
                f"UID={sql_config.get('uuid', 'sa')};"
                f"PWD={sql_config.get('pwd', '')}"
            )
            self.connection = pyodbc.connect(conn_str)
            print_success(f"[SQL] Connected to database: {sql_config['database']}")
        except pyodbc.Error as e:
            print_fail(f"[SQL] Error connecting to database: {e}")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            if query.strip().upper().startswith("SELECT"):
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            self.connection.commit()
            return cursor.rowcount
        except pyodbc.Error as e:
            print_fail(f"[SQL] Query error: {e}")
            return None
        finally:
            cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()
            print_success("[SQL] Connection closed.")