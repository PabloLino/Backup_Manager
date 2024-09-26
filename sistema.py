'''
lógica de negócios e as classes para gerenciar clientes e ocorrências.
'''

import pyodbc
from config import connection_string

class Cliente:
    def __init__(self, id_cliente, nome_cartorio, nu_sac, conta_nuvem):
        self.id_cliente = id_cliente
        self.nome_cartorio = nome_cartorio
        self.nu_sac = nu_sac
        self.conta_nuvem = conta_nuvem
        self.ocorrencias = []

    def adicionar_ocorrencia(self, descricao, solucionado=False):
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
            cursor.execute("SELECT id_cliente, nome_cartorio, nu_sac, conta_nuvem FROM Clientes")
            for row in cursor.fetchall():
                id_cliente, nome_cartorio, nu_sac, conta_nuvem = row
                self.clientes[id_cliente] = Cliente(id_cliente, nome_cartorio, nu_sac, conta_nuvem)

    def carregar_ocorrencias(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_cliente, descricao, solucionado FROM Ocorrencias")
            for row in cursor.fetchall():
                id_cliente, descricao, solucionado = row
                if id_cliente in self.clientes:
                    self.clientes[id_cliente].adicionar_ocorrencia(descricao, solucionado)

    def cadastrar_cliente(self, nome_cartorio, nu_sac, conta_nuvem):
        novo_id = max(self.clientes.keys(), default=0) + 1

        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Clientes (id_cliente, nome_cartorio, nu_sac, conta_nuvem) VALUES (?, ?, ?, ?)",
                    (novo_id, nome_cartorio, nu_sac, conta_nuvem)
                )
                conn.commit()
            self.clientes[novo_id] = Cliente(novo_id, nome_cartorio, nu_sac, conta_nuvem)
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
