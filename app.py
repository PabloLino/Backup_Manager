import os
import tkinter as tk
from tkinter import ttk, messagebox
from sistema import Sistema
from telas import TelaCadastroCliente, TelaRegistrarOcorrencia, TelaConsultarClientes, TelaGerarRelatorio, TelaMenu, TelaLogin

class Aplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Backup Manager")
        self.geometry("1200x900")
        self.configure(bg='#000000')  # Cor padrão do sistema
        caminho_icone = os.path.join(os.path.dirname(__file__), 'favicon1.ico')  # Ícone do sistema
        self.iconbitmap(caminho_icone)

        self.sistema = Sistema()
        self.tela_atual = None
        self.usuario_logado = None

        #start tela de login
        self.abrir_tela_login()

    def abrir_tela_login(self):
        if self.tela_atual is not None:
            self.tela_atual.destroy()

        self.tela_atual = TelaLogin(self)
        self.tela_atual.pack(fill=tk.BOTH, expand=True)

    def abrir_tela(self, event):
        funcionalidade = self.combo_funcionalidades.get()

        if self.usuario_logado == "admin":  # acesso full
            funcionalidades_completas = ["Menu", "Cadastrar Cliente", "Registrar Ocorrência", "Consultar Clientes", "Gerar Relatório"]
        else:  #acesso limitado
            funcionalidades_completas = ["Menu", "Consultar Clientes", "Gerar Relatório"]

        if funcionalidade == "Menu" or funcionalidade == "":
            if self.tela_atual is not None:
                self.tela_atual.destroy()
            self.tela_atual = TelaMenu(self)
            self.tela_atual.pack(fill=tk.BOTH, expand=True)
            return

        if self.tela_atual is not None:
            self.tela_atual.destroy()

        if funcionalidade == "Cadastrar Cliente" and funcionalidade in funcionalidades_completas:
            self.tela_atual = TelaCadastroCliente(self)
        elif funcionalidade == "Registrar Ocorrência" and funcionalidade in funcionalidades_completas:
            self.tela_atual = TelaRegistrarOcorrencia(self)
        elif funcionalidade == "Consultar Clientes":
            self.tela_atual = TelaConsultarClientes(self)
        elif funcionalidade == "Gerar Relatório":
            self.tela_atual = TelaGerarRelatorio(self)

        self.tela_atual.pack(fill=tk.BOTH, expand=True)

    def autenticar(self, usuario, senha):
        if usuario == "admin" and senha == "Extr@bkp":
            self.usuario_logado = "admin"
        else:
            self.usuario_logado = "visitante"
        self.mostrar_menu()

    def mostrar_menu(self):
        if self.tela_atual is not None:
            self.tela_atual.destroy()

        # Menu inicial
        self.menu_frame = tk.Frame(self, bg='#000000')
        self.menu_frame.pack(side=tk.TOP, anchor='nw', pady=10, padx=10)

        # Combobox para funcionalidades
        self.combo_funcionalidades = ttk.Combobox(self.menu_frame, state="readonly", width=20)
        if self.usuario_logado == "admin":
            self.combo_funcionalidades['values'] = ["Menu", "Cadastrar Cliente", "Registrar Ocorrência", "Consultar Clientes", "Gerar Relatório"]
        else:
            self.combo_funcionalidades['values'] = ["Menu", "Consultar Clientes", "Gerar Relatório"]

        self.combo_funcionalidades.current(0)
        self.combo_funcionalidades.bind("<<ComboboxSelected>>", self.abrir_tela)
        self.combo_funcionalidades.pack()

        # Carrega o menu inicial
        self.abrir_tela(None)


if __name__ == "__main__":
    app = Aplicacao()
    app.mainloop()
