import pyodbc

connection_string = (
    "Driver={ODBC Driver 11 for SQL Server};"
    "Server=*******;"  
    "Database=DB_BackupOn_Manager;"  
    "UID=****;"  
    "PWD=E***;"  
)

try:
    conn = pyodbc.connect(connection_string)
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro na conexão: {str(e)}")
