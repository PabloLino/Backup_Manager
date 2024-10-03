'''
Lógica de negócios e as classes para gerenciar clientes e ocorrências.
'''

import pyodbc
from config import connection_string

class Cliente:
    def __init__(self, id_cliente, nome_cartorio, nu_sac, conta_nuvem, nome_oficial, nu_telefone, email_cliente, usuario_cliente, senha_cliente):
        self.id_cliente = id_cliente
        self.nome_cartorio = nome_cartorio
        self.nu_sac = nu_sac
        self.conta_nuvem = conta_nuvem
        self.nome_oficial = nome_oficial
        self.nu_telefone = nu_telefone
        self.email_cliente = email_cliente
        self.usuario_cliente = usuario_cliente
        self.senha_cliente = senha_cliente
        self.ocorrencias = []

    def adicionar_ocorrencia(self, descricao, solucionado=True):
        self.ocorrencias.append((descricao, solucionado))

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
            cursor.execute("SELECT id_cliente, nome_cartorio, nu_sac, conta_nuvem, nome_oficial, nu_telefone, email_cliente, usuario_cliente, senha_cliente FROM Clientes")
            for row in cursor.fetchall():
                id_cliente, nome_cartorio, nu_sac, conta_nuvem, nome_oficial, nu_telefone, email_cliente, usuario_cliente, senha_cliente = row
                self.clientes[nu_sac] = Cliente(id_cliente, nome_cartorio, nu_sac, conta_nuvem, nome_oficial, nu_telefone, email_cliente, usuario_cliente, senha_cliente)

    def carregar_ocorrencias(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_cliente, descricao, solucionado FROM Ocorrencias")
            for row in cursor.fetchall():
                id_cliente, descricao, solucionado = row
                if id_cliente in self.clientes:
                    self.clientes[id_cliente].adicionar_ocorrencia(descricao, solucionado)

    def cadastrar_cliente(self, **cliente_data):
        # Chaves do cliente
        required_keys = ['Nome do Cartório', 'Número SAC', 'Conta Nuvem', 'Nome Oficial', 'Número de Telefone', 'Email do Cliente', 'Usuário', 'Senha'] #relação com telas.py em  def cadastrar_cliente(self): cliente_data 
    
        for key in required_keys:
            if key not in cliente_data:
                return f"Erro: '{key}' não foi fornecido!"

        if any(cliente.nu_sac == cliente_data['Número SAC'] for cliente in self.clientes.values()):
            return "Já existe um cliente cadastrado com este número SAC!"

        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Clientes (nome_cartorio, nu_sac, conta_nuvem, nome_oficial, nu_telefone, email_cliente, usuario_cliente, senha_cliente) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (cliente_data['Nome do Cartório'], cliente_data['Número SAC'], cliente_data['Conta Nuvem'], cliente_data['Nome Oficial'],
                    cliente_data['Número de Telefone'], cliente_data['Email do Cliente'], cliente_data['Usuário'], cliente_data['Senha'])
                )
                conn.commit()
            self.carregar_clientes()
            return "Cliente cadastrado com sucesso!"
        except Exception as e:
            return f"Erro ao cadastrar cliente: {str(e)}"

    def registrar_ocorrencia(self, id_cliente, descricao, solucionado=False):
        if id_cliente not in self.clientes:
            return "Cliente não encontrado!"

        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Ocorrencias (id_cliente, descricao, solucionado) VALUES (?, ?, ?)",
                    (id_cliente, descricao, solucionado)
                )
                conn.commit()
            self.clientes[id_cliente].adicionar_ocorrencia(descricao, solucionado)
            return "Ocorrência registrada com sucesso!"
        except Exception as e:
            return f"Erro ao registrar ocorrência: {str(e)}"

    def relatorio_ocorrencias(self):
        return [(cliente.nome_cartorio, cliente.ocorrencias) for cliente in self.clientes.values()]
