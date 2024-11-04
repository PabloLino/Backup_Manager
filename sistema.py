import pyodbc
from config import connection_string

class Cliente:
    def __init__(self, id_cliente, nome_cartorio, nu_sac, uf, conta_nuvem, nome_oficial, nu_telefone, nu_telefone2, email_cliente, usuario_cliente, senha_cliente):
        self.id_cliente = id_cliente
        self.nome_cartorio = nome_cartorio
        self.nu_sac = nu_sac
        self.uf = uf
        self.conta_nuvem = conta_nuvem
        self.nome_oficial = nome_oficial
        self.nu_telefone = nu_telefone
        self.nu_telefone2 = nu_telefone2
        self.email_cliente = email_cliente
        self.usuario_cliente = usuario_cliente
        self.senha_cliente = senha_cliente
        self.ocorrencias = []

    def adicionar_ocorrencia(self, tipo_banco, tipeocorrencia, DescriOcorrencia, solucionado):
        self.ocorrencias.append((tipo_banco, tipeocorrencia, DescriOcorrencia, solucionado))

class Sistema:
    def __init__(self):
        self.connection_string = connection_string
        self.clientes = {}
        self.carregar_clientes()
        self.carregar_ocorrencias()

    def conectar(self):
        try:
            return pyodbc.connect(self.connection_string)
        except Exception as e:
            raise ConnectionError(f"Erro ao conectar ao banco de dados: {str(e)}")

    def carregar_clientes(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_cliente, nome_cartorio, nu_sac, uf, conta_nuvem, nome_oficial, nu_telefone, nu_telefone2, email_cliente, usuario_cliente, senha_cliente FROM Clientes")
            for row in cursor.fetchall():
                id_cliente, nome_cartorio, nu_sac, uf, conta_nuvem, nome_oficial, nu_telefone, nu_telefone2, email_cliente, usuario_cliente, senha_cliente = row
                self.clientes[nu_sac] = Cliente(id_cliente, nome_cartorio, nu_sac, uf, conta_nuvem, nome_oficial, nu_telefone, nu_telefone2, email_cliente, usuario_cliente, senha_cliente)

    def carregar_ocorrencias(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_cliente, tipo_banco, tipo_ocorrencia, descri_ocorrencia, solucionado FROM Ocorrencias")
            for row in cursor.fetchall():
                id_cliente, tipo_banco, tipeocorrencia, DescriOcorrencia, solucionado = row
                if id_cliente in self.clientes:
                    self.clientes[id_cliente].adicionar_ocorrencia(tipo_banco, tipeocorrencia, DescriOcorrencia, solucionado)

    def cadastrar_cliente(self, **cliente_data):
        #relação com telas.py em  def cadastrar_cliente(self): cliente_data 
        # Chaves do cliente
        required_keys = ['Cartório', 'Número SAC Formato 0000', 'UF', 'Conta Nuvem', 'Nome Oficial', 'Número de Telefone', 'Número Do Telefone 2', 'Email do Cliente', 'Usuário', 'Senha'] 
    
        for key in required_keys:
            if key not in cliente_data:
                return f"Erro: '{key}' não foi fornecido!"
            
        nu_sac = cliente_data['Número SAC Formato 0000']
        if not nu_sac.isdigit() or len(nu_sac) != 4:
            return "O Número SAC deve conter exatamente 4 dígitos!"


        if any(cliente.nu_sac == cliente_data['Número SAC Formato 0000'] for cliente in self.clientes.values()):
            return "Já existe um cliente cadastrado com este número SAC!"

        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Clientes (nome_cartorio, nu_sac, uf, conta_nuvem, nome_oficial, nu_telefone, nu_telefone2, email_cliente, usuario_cliente, senha_cliente) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (cliente_data['Cartório'], cliente_data['Número SAC Formato 0000'], cliente_data['UF'], cliente_data['Conta Nuvem'], cliente_data['Nome Oficial'],
                    cliente_data['Número de Telefone'], cliente_data['Número Do Telefone 2'], cliente_data['Email do Cliente'], cliente_data['Usuário'], cliente_data['Senha'])
                )
                conn.commit()
            self.carregar_clientes()
            return "Cliente cadastrado com sucesso!"
        except Exception as e:
            return f"Erro ao cadastrar cliente: {str(e)}"

    def registrar_ocorrencia(self, id_cliente, tipo_banco, tipeocorrencia, DescriOcorrencia, solucionado, data_ocorrencia):
        if id_cliente not in self.clientes:
            return "Cliente não encontrado!"

        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Ocorrencias (id_cliente, tipo_banco, tipo_ocorrencia, descri_ocorrencia, solucionado, data_ocorrencia) VALUES (?, ?, ?, ?, ?, ?)",
                    (id_cliente, tipo_banco, tipeocorrencia, DescriOcorrencia, solucionado, data_ocorrencia)
                )
                conn.commit()
            self.clientes[id_cliente].adicionar_ocorrencia(tipo_banco, tipeocorrencia, DescriOcorrencia, solucionado)
            return "Ocorrência registrada com sucesso!"
        except Exception as e:
            return f"Erro ao registrar ocorrência: {str(e)}"
        



    def relatorio_ocorrencias(self, nu_sac=None, data_inicio=None, data_fim=None):
        try:
            with self.conectar() as conn:  #Usando o método conectar()
                cursor = conn.cursor()

            #Consulta SQL para visualização do relatório
                query = """
                SELECT o.id_cliente, o.tipo_ocorrencia, o.data_ocorrencia, o.tipo_banco
                FROM Ocorrencias o
                JOIN Clientes c ON o.id_cliente = c.nu_sac
                WHERE 1=1
                """
                params = []

            #Filtro
                if nu_sac:
                    query += " AND o.id_cliente = ?"
                    params.append(nu_sac)

            #Filtro data início
                if data_inicio:
                    query += " AND o.data_ocorrencia >= ?"
                    params.append(data_inicio)

            #Filtro data fim
                if data_fim:
                    query += " AND o.data_ocorrencia <= ?"
                    params.append(data_fim)


                cursor.execute(query, params)
                resultados = cursor.fetchall()

            # Verificação
                if resultados:
                    relatorio = "SAC | Tipo Ocorrência | Data Ocorrência | Tipo Banco\n"
                    relatorio += "-" * 90 + "\n"
                    for row in resultados:
                        relatorio += f"{row[0]} | {row[1]} | {row[2]} | {row[3]}\n"
                else:
                    relatorio = ""  #vazio se não houver resultados

                return relatorio

        except Exception as e:
            return f"Erro ao gerar o relatório: {e}"
