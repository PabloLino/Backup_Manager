import pyodbc

connection_string = (
    "Driver= {ODBC Driver 11 for SQL Server};"
    "Server=localhost;"
    "Database=DB_BackupOn_Manager;"
    "UID=SA;"
    "PWD=Extr@123;"
)

try:
    conn = pyodbc.connect(connection_string)
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro na conexão: {str(e)}")
