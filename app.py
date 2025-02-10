from logging import root
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from sistema import Sistema
from telas import TelaCadastroCliente, TelaRegistrarOcorrencia, TelaConsultarClientes, TelaConsultarOcorrencia, TelaMenu, TelaLogin
import pyodbc
from tkinter import messagebox
import pyodbc
import sys 
import os
from config import connection_string
import locale
import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry

# Determina o diretório base (normal ou embutido pelo PyInstaller)
if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS  # Diretório temporário criado pelo PyInstaller
else:
    base_path = os.path.abspath(".")

# Determina o caminho correto do ícone
if hasattr(sys, "_MEIPASS"):
    icon_path = os.path.join(sys._MEIPASS, "favicon1.ico")
else:
    icon_path = "favicon1.ico"

# Configura o ícone
try:
    root.iconbitmap(icon_path)
except Exception as e:
    print(f"Erro ao configurar o ícone: {e}")

# Caminho para a pasta internal
internal_path = os.path.join(base_path, 'internal')

class Aplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Backup Manager")
        self.geometry("1200x900")  # Tamanho ao sair da tela cheia
        self.state('zoomed')       # Abre o app em tela cheia como padrão
        self.configure(bg='#000000')  # Cor padrão do sistema

        # Caminho do ícone atualizado para buscar na pasta internal
        caminho_icone = os.path.join(os.path.dirname(__file__), 'favicon1.ico')# Ícone do sistema
        self.iconbitmap(caminho_icone)

        self.sistema = Sistema()
        self.tela_atual = None
        self.usuario_logado = None
        self.menu_frame = None  # Inicializa a variável que irá armazenar o menu

        # Start tela de login
        self.abrir_tela_login()

    def ajusta_tamanho_tela(self, event=None):
        if self.state() != 'zoomed':
            self.geometry("1200x900")

    def abrir_tela_login(self):
        if self.tela_atual is not None:
            self.tela_atual.destroy()

        self.tela_atual = TelaLogin(self)
        self.tela_atual.pack(fill=tk.BOTH, expand=True)

    def abrir_tela(self, event):
        funcionalidade = self.combo_funcionalidades.get()

        if self.usuario_logado == "*****":  # Acesso total
            funcionalidades_completas = ["Menu", "Cadastrar Cliente", "Registrar Ocorrência", "Consultar Clientes", "Consultar Ocorrências"]
        else:  # Acesso limitado
            funcionalidades_completas = ["Menu", "Consultar Clientes", "Consultar Ocorrências"]

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
        elif funcionalidade == "Consultar Ocorrências":
            self.tela_atual = TelaConsultarOcorrencia(self)

        self.tela_atual.pack(fill=tk.BOTH, expand=True)

    def autenticar(self, usuario, senha):
        if usuario == "*****" and senha == "E*******":
            self.usuario_logado = "admin"
        else:
            self.usuario_logado = "visitante"
        self.mostrar_menu()

    def mostrar_menu(self):
        # Se o menu já existir, não cria novamente
        if self.menu_frame is not None:
            self.menu_frame.destroy()

        # Menu inicial
        self.menu_frame = tk.Frame(self, bg='#000000')
        self.menu_frame.pack(side=tk.TOP, anchor='nw', pady=10, padx=10)

        # Combobox para funcionalidades
        self.combo_funcionalidades = ttk.Combobox(self.menu_frame, state="readonly", width=20)
        if self.usuario_logado == "admin":
            self.combo_funcionalidades['values'] = ["Menu", "Cadastrar Cliente", "Registrar Ocorrência", "Consultar Clientes", "Consultar Ocorrências"]
        else:
            self.combo_funcionalidades['values'] = ["Menu", "Consultar Clientes", "Consultar Ocorrências"]

        self.combo_funcionalidades.current(0)
        self.combo_funcionalidades.bind("<<ComboboxSelected>>", self.abrir_tela)
        self.combo_funcionalidades.pack()

        # Botão para trocar de usuário com tamanho reduzido
        self.botao_trocar_usuario = tk.Button(self.menu_frame, text="Trocar Usuário", command=self.confirmar_troca_usuario, bg='#FFC107', fg='black', font=('Arial', 8, 'bold'), width=12, height=1)
        self.botao_trocar_usuario.pack(pady=5)

        # Carrega o menu inicial
        self.abrir_tela(None)

    def confirmar_troca_usuario(self):
        resposta = messagebox.askyesno("Confirmação", "Deseja realmente trocar de usuário?")
        if resposta:  # Se o usuário confirmar, vai para a tela de login
            self.abrir_tela_login()
        else:
            # Caso o usuário não queira trocar, apenas retorna
            return


if __name__ == "__main__":
    app = Aplicacao()
    app.mainloop()
