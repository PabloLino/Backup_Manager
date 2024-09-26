'''
config da interface do usuário
'''

import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class TelaMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#000000')

        # Definindo o caminho da imagem
        if getattr(sys, 'frozen', False):
            # Se o aplicativo estiver congelado (executável)
            self.imagem_path = os.path.join(os.path.dirname(sys.executable), 'database.png')
        else:
            # Se estiver em modo de desenvolvimento
            self.imagem_path = "C:/Users/pablo/Desktop/Gerenciamento_BackupOn/database.png"
        
        self.img = Image.open(self.imagem_path)
        self.img = self.img.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.img)

        self.label_imagem = tk.Label(self, image=self.photo, bg='#000000')
        self.label_imagem.pack(pady=20)

        label_instrucoes = tk.Label(self, text="Escolha uma funcionalidade no menu", bg='#000000', fg='#FFC107', font=('Arial', 12))
        label_instrucoes.pack(pady=10)


class TelaCadastroCliente(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#000000')

        self.label_nome_cartorio = tk.Label(self, text="Nome do Cartório:", bg='#000000', fg='#FFC107', font=('Arial', 12))
        self.label_nome_cartorio.pack()
        self.entry_nome_cartorio = tk.Entry(self)
        self.entry_nome_cartorio.pack()

        self.label_nu_sac = tk.Label(self, text="Número SAC:", bg='#000000', fg='#FFC107', font=('Arial', 12))
        self.label_nu_sac.pack()
        self.entry_nu_sac = tk.Entry(self)
        self.entry_nu_sac.pack()

        self.label_conta_nuvem = tk.Label(self, text="Conta Nuvem:", bg='#000000', fg='#FFC107', font=('Arial', 12))
        self.label_conta_nuvem.pack()
        self.entry_conta_nuvem = tk.Entry(self)
        self.entry_conta_nuvem.pack()

        self.button_cadastrar = tk.Button(self, text="Cadastrar Cliente", command=self.cadastrar_cliente, bg='#333333', fg='#FFC107', font=('Arial', 12, 'bold'))
        self.button_cadastrar.pack(pady=10)

        self.button_menu = tk.Button(self, text="Menu", command=self.voltar_menu, bg='#333333', fg='#FFC107', font=('Arial', 12, 'bold'))
        self.button_menu.pack(anchor='se', padx=10, pady=10, side='bottom')

    def cadastrar_cliente(self):
        nome_cartorio = self.entry_nome_cartorio.get()
        nu_sac = self.entry_nu_sac.get()
        conta_nuvem = self.entry_conta_nuvem.get()

        resultado = self.master.sistema.cadastrar_cliente(nome_cartorio, nu_sac, conta_nuvem)
        messagebox.showinfo("Cadastro de Cliente", resultado)

        self.entry_nome_cartorio.delete(0, tk.END)
        self.entry_nu_sac.delete(0, tk.END)
        self.entry_conta_nuvem.delete(0, tk.END)

    def voltar_menu(self):
        self.master.combo_funcionalidades.current(0)
        self.master.abrir_tela(None)


class TelaRegistrarOcorrencia(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#000000')

        self.label_id = tk.Label(self, text="ID do Cliente:", bg='#000000', fg='#FFC107', font=('Arial', 12))
        self.label_id.pack()
        self.entry_id = tk.Entry(self)
        self.entry_id.pack()

        self.label_ocorrencia = tk.Label(self, text="Descrição Ocorrência:", bg='#000000', fg='#FFC107', font=('Arial', 12))
        self.label_ocorrencia.pack()
        self.entry_ocorrencia = tk.Entry(self)
        self.entry_ocorrencia.pack()

        self.button_registrar = tk.Button(self, text="Registrar Ocorrência", command=self.registrar_ocorrencia, bg='#333333', fg='#FFC107', font=('Arial', 12, 'bold'))
        self.button_registrar.pack(pady=10)

        self.button_menu = tk.Button(self, text="Menu", command=self.voltar_menu, bg='#333333', fg='#FFC107', font=('Arial', 12, 'bold'))
        self.button_menu.pack(anchor='se', padx=10, pady=10, side='bottom')

    def registrar_ocorrencia(self):
        id_cliente = self.entry_id.get()
        descricao = self.entry_ocorrencia.get()

        resultado = self.master.sistema.registrar_ocorrencia(id_cliente, descricao)
        messagebox.showinfo("Registro de Ocorrência", resultado)

        self.entry_id.delete(0, tk.END)
        self.entry_ocorrencia.delete(0, tk.END)

    def voltar_menu(self):
        self.master.combo_funcionalidades.current(0)
        self.master.abrir_tela(None)


class TelaConsultarClientes(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#000000')

        self.text_clientes = tk.Text(self, height=20, bg='#333333', fg='#FFC107', font=('Arial', 12))
        self.text_clientes.pack()

        self.button_consultar = tk.Button(self, text="Consultar Clientes", command=self.consultar_clientes, bg='#333333', fg='#FFC107', font=('Arial', 12, 'bold'))
        self.button_consultar.pack(pady=10)

        self.button_menu = tk.Button(self, text="Menu", command=self.voltar_menu, bg='#333333', fg='#FFC107', font=('Arial', 12, 'bold'))
        self.button_menu.pack(anchor='se', padx=10, pady=10, side='bottom')

    def consultar_clientes(self):
        self.text_clientes.delete(1.0, tk.END)
        for id_cliente, cliente in self.master.sistema.clientes.items():
            self.text_clientes.insert(tk.END, f"ID: {id_cliente}, Nome: {cliente.nome_cartorio}, SAC: {cliente.nu_sac}, Nuvem: {cliente.conta_nuvem}\n")

    def voltar_menu(self):
        self.master.combo_funcionalidades.current(0)
        self.master.abrir_tela(None)


class TelaGerarRelatorio(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#000000')

        self.label_id_cliente = tk.Label(self, text="ID do Cliente:", bg='#000000', fg='#FFC107', font=('Arial', 12))
        self.label_id_cliente.pack()
        self.entry_id_cliente = tk.Entry(self)
        self.entry_id_cliente.pack()

        self.button_gerar = tk.Button(self, text="Gerar Relatório", command=self.gerar_relatorio, bg='#333333', fg='#FFC107', font=('Arial', 12, 'bold'))
        self.button_gerar.pack(pady=10)

        self.button_menu = tk.Button(self, text="Menu", command=self.voltar_menu, bg='#333333', fg='#FFC107', font=('Arial', 12, 'bold'))
        self.button_menu.pack(anchor='se', padx=10, pady=10, side='bottom')

    def gerar_relatorio(self):
        id_cliente = self.entry_id_cliente.get()

        resultado = self.master.sistema.gerar_relatorio(id_cliente)
        messagebox.showinfo("Gerar Relatório", resultado)

        self.entry_id_cliente.delete(0, tk.END)

    def voltar_menu(self):
        self.master.combo_funcionalidades.current(0)
        self.master.abrir_tela(None)
