import pyodbc

connection_string = (
    "Driver={ODBC Driver 11 for SQL Server};" #verificar qual esta instalado
    "Server=*******;" #ip  
    "Database=DB_BackupOn_Manager;" #nome do banco  
    "UID=*********;" #usuario sql  
    "PWD=*****;" #senha sql  
)

try:
    conn = pyodbc.connect(connection_string)
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro na conexão: {str(e)}")
