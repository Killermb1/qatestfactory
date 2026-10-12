import pyodbc

# Update connection details as required
DB_CONFIG = {
    "server": r"localhost\SQLEXPRESS",
    "database": "TestQB",
    "driver": "{ODBC Driver 17 for SQL Server}",
    "trusted_connection": "yes"
}

def get_connection():
    conn_str = f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};Trusted_Connection={DB_CONFIG['trusted_connection']};"
    return pyodbc.connect(conn_str)