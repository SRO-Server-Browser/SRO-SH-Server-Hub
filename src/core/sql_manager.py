import pyodbc
import os
from utils.colors import print_success, print_fail

class SQLManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.connection = None
        self.sqls_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sqls')
        self.sql_config = self.config_manager.get_special_config("SQL")
        self.state = (self.sql_config.get('connect_sql') != 0)
        if self.state:
            self.connect()

    def connect(self):
        """SQL Server'a bağlanır."""
        sql_config = self.sql_config
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
        """SQL sorgusunu çalıştırır."""
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

    def execute_sql_file(self, sql_file_name, params=None):
        """Belirtilen SQL dosyasını okur ve çalıştırır."""
        sql_file_path = os.path.join(self.sqls_dir, sql_file_name)
        if not os.path.exists(sql_file_path):
            print_fail(f"[SQL] SQL file not found: {sql_file_path}")
            return None

        try:
            with open(sql_file_path, 'r', encoding='utf-8') as file:
                sql_query = file.read()
            return self.execute_query(sql_query, params)
        except (IOError, pyodbc.Error) as e:
            print_fail(f"[SQL] Error executing SQL file {sql_file_name}: {e}")
            return None

    def close(self):
        """SQL bağlantısını kapatır."""
        if self.connection:
            self.connection.close()
            print_success("[SQL] Connection closed.")