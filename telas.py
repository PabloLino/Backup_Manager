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

        if getattr(sys, 'frozen', False):
            self.imagem_path = os.path.join(os.path.dirname(sys.executable), 'database.png')
        else:
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
        self.master.abrir_tela(None)


class TelaRegistrarOcorrencia(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#000000')

        self.label_id_cliente = tk.Label(self, text="ID do Cliente:", bg='#000000', fg='#FFC107', font=('Arial', 12))
        self.label_id_cliente.pack()
        self.entry_id_cliente = tk.Entry(self)
        self.entry_id_cliente.pack()

        self.label_descricao = tk.Label(self, text="Descrição da Ocorrência:", bg='#000000', fg='#FFC107', font=('Arial', 12))
        self.label_descricao.pack()
        self.entry_descricao = tk.Entry(self)
        self.entry_descricao.pack()

        self.label_solucionado = tk.Label(self, text="Solucionado (True/False):", bg='#000000', fg='#FFC107', font=('Arial', 12))
        self.label_solucionado.pack()
        self.entry_solucionado = tk.Entry(self)
        self.entry_solucionado.pack()

        self.button_registrar = tk.Button(self, text="Registrar Ocorrência", command=self.registrar_ocorrencia, bg='#333333', fg='#FFC107', font=('Arial', 12, 'bold'))
        self.button_registrar.pack(pady=10)

        self.button_menu = tk.Button(self, text="Menu", command=self.voltar_menu, bg='#333333', fg='#FFC107', font=('Arial', 12, 'bold'))
        self.button_menu.pack(anchor='se', padx=10, pady=10, side='bottom')

    def registrar_ocorrencia(self):
        id_cliente = self.entry_id_cliente.get()
        descricao = self.entry_descricao.get()
        solucionado = self.entry_solucionado.get().strip().lower() == 'true'

        resultado = self.master.sistema.registrar_ocorrencia(id_cliente, descricao, solucionado)
        messagebox.showinfo("Registro de Ocorrência", resultado)

        self.entry_id_cliente.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_solucionado.delete(0, tk.END)

    def voltar_menu(self):
        self.master.abrir_tela(None)


class TelaConsultarClientes(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#000000')

        self.label_titulo = tk.Label(self, text="Clientes Cadastrados", bg='#000000', fg='#FFC107', font=('Arial', 12))
        self.label_titulo.pack(pady=10)

        self.listbox_clientes = tk.Listbox(self, width=80)
        self.listbox_clientes.pack(pady=10)

        self.button_menu = tk.Button(self, text="Menu", command=self.voltar_menu, bg='#333333', fg='#FFC107', font=('Arial', 12, 'bold'))
        self.button_menu.pack(anchor='se', padx=10, pady=10, side='bottom')

        self.carregar_clientes()

    def carregar_clientes(self):
        self.listbox_clientes.delete(0, tk.END)
        for cliente in self.master.sistema.clientes.values():
            self.listbox_clientes.insert(tk.END, f"ID: {cliente.id_cliente}, Nome: {cliente.nome_cartorio}, SAC: {cliente.nu_sac}, Conta: {cliente.conta_nuvem}")

    def voltar_menu(self):
        self.master.abrir_tela(None)


class TelaGerarRelatorio(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#000000')

        self.label_titulo = tk.Label(self, text="Relatório de Ocorrências", bg='#000000', fg='#FFC107', font=('Arial', 12))
        self.label_titulo.pack(pady=10)

        self.text_relatorio = tk.Text(self, width=80, height=20)
        self.text_relatorio.pack(pady=10)

        self.button_gerar = tk.Button(self, text="Gerar Relatório", command=self.gerar_relatorio, bg='#333333', fg='#FFC107', font=('Arial', 12, 'bold'))
        self.button_gerar.pack(pady=10)

        self.button_menu = tk.Button(self, text="Menu", command=self.voltar_menu, bg='#333333', fg='#FFC107', font=('Arial', 12, 'bold'))
        self.button_menu.pack(anchor='se', padx=10, pady=10, side='bottom')

    def gerar_relatorio(self):
        self.text_relatorio.delete(1.0, tk.END)
        relatorio = self.master.sistema.relatorio_ocorrencias()
        for nome_cartorio, ocorrencias in relatorio:
            self.text_relatorio.insert(tk.END, f"Cartório: {nome_cartorio}\n")
            for descricao, solucionado in ocorrencias:
                self.text_relatorio.insert(tk.END, f" - {descricao} (Solucionado: {solucionado})\n")
            self.text_relatorio.insert(tk.END, "\n")

    def voltar_menu(self):
        self.master.abrir_tela(None)
