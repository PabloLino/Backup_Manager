import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class TelaMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#121212')  # Cor de fundo

        self.imagem_path = os.path.join(os.path.dirname(__file__), 'database.png')

        self.img = Image.open(self.imagem_path)
        self.img = self.img.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.img)

        self.label_imagem = tk.Label(self, image=self.photo, bg='#121212')
        self.label_imagem.pack(pady=20)

        label_instrucoes = tk.Label(self, text="Escolha uma funcionalidade no menu", bg='#121212', fg='#FFC107', font=('Arial', 14, 'bold'))
        label_instrucoes.pack(pady=10)


class TelaCadastroCliente(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#121212')  # Cor de fundo

        self.create_label_entry("Nome do Cartório:")
        self.create_label_entry("Número SAC:")
        self.create_label_entry("Conta Nuvem:")
        self.create_label_entry("Nome Oficial:")
        self.create_label_entry("Número de Telefone:")
        self.create_label_entry("Email do Cliente:")
        self.create_label_entry("Usuário:")
        self.create_label_entry("Senha:")

        self.botao_cadastrar = tk.Button(self, text="Cadastrar Cliente", command=self.cadastrar_cliente, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        self.botao_cadastrar.pack(pady=20)

        self.botao_menu = tk.Button(self, text="Menu", command=self.voltar_menu, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        self.botao_menu.pack(side=tk.BOTTOM, anchor='se', padx=10, pady=10)

    def create_label_entry(self, text, show=None):
        label = tk.Label(self, text=text, bg='#121212', fg='#FFC107', font=('Arial', 11))
        label.pack()
        entry = tk.Entry(self, show=show)
        entry.pack()
        safe_name = text.replace(" ", "_").replace(":", "").replace("ç", "c").lower()  # Substituir caracteres especiais
        setattr(self, f'entry_{safe_name}', entry)  # Criar o atributo dinamicamente

    def cadastrar_cliente(self):
        cliente_data = {
            "Nome do Cartório": self.entry_nome_do_cartório.get(),
            "Número SAC": self.entry_número_sac.get(),
            "Conta Nuvem": self.entry_conta_nuvem.get(),
            "Nome Oficial": self.entry_nome_oficial.get(),
            "Número de Telefone": self.entry_número_de_telefone.get(),
            "Email do Cliente": self.entry_email_do_cliente.get(),
            "Usuário": self.entry_usuário.get(),
            "Senha": self.entry_senha.get()
    }

        resultado = self.master.sistema.cadastrar_cliente(**cliente_data)
        messagebox.showinfo("Cadastro de Cliente", resultado)


        # Limpar todos os campos
        for attr in cliente_data.keys():
            getattr(self, f'entry_{attr.replace(" ", "_").replace("ç", "c").lower()}').delete(0, tk.END)

    def voltar_menu(self):
        self.master.combo_funcionalidades.set("Menu")
        self.master.abrir_tela(None)


class TelaRegistrarOcorrencia(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#121212')  # Cor de fundo

        self.label_id_cliente = tk.Label(self, text="Nº SAC do Cliente:", bg='#121212', fg='#FFC107', font=('Arial', 12))
        self.label_id_cliente.pack()
        self.entry_id_cliente = tk.Entry(self)
        self.entry_id_cliente.pack()

        self.label_descricao = tk.Label(self, text="Descrição da Ocorrência:", bg='#121212', fg='#FFC107', font=('Arial', 12))
        self.label_descricao.pack()
        self.entry_descricao = tk.Entry(self)
        self.entry_descricao.pack()

        self.botao_registrar = tk.Button(self, text="Registrar Ocorrência", command=self.registrar_ocorrencia, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        self.botao_registrar.pack(pady=20)

        self.botao_menu = tk.Button(self, text="Menu", command=self.voltar_menu, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        self.botao_menu.pack(side=tk.BOTTOM, anchor='se', padx=10, pady=10)

    def registrar_ocorrencia(self):
        id_cliente = self.entry_id_cliente.get()
        descricao = self.entry_descricao.get()

        resultado = self.master.sistema.registrar_ocorrencia(id_cliente, descricao)
        messagebox.showinfo("Registro de Ocorrência", resultado)

        # Limpar campos
        self.entry_id_cliente.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)

    def voltar_menu(self):
        self.master.combo_funcionalidades.set("Menu")
        self.master.abrir_tela(None)


class TelaConsultarClientes(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#121212')  #fundo

        self.label_busca = tk.Label(self, text="Digite o número do SAC:", bg='#121212', fg='#FFC107', font=('Arial', 12))
        self.label_busca.pack(pady=(10, 0))

        self.entry_busca = tk.Entry(self)
        self.entry_busca.pack(pady=(0, 10))

        self.botao_buscar = tk.Button(self, text="Consultar", command=self.buscar_cliente, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        self.botao_buscar.pack(pady=20)

        # Adicionando um quadro para exibir o resultado
        self.quadro_resultado = tk.Frame(self, bg='#A68C00') #amarelo escuro #BDAF00
        self.quadro_resultado.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.label_resultado = tk.Text(self.quadro_resultado, bg='#121212', fg='#FFC107', font=('Arial', 12), wrap=tk.WORD, height=8)
        self.label_resultado.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.botao_menu = tk.Button(self, text="Menu", command=self.voltar_menu, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        self.botao_menu.pack(side=tk.BOTTOM, anchor='se', padx=10, pady=10)

    def buscar_cliente(self):
        nu_sac = self.entry_busca.get()
        
        cliente = self.master.sistema.clientes.get((nu_sac), None)
        if cliente:
            resultado = (f"CARTÓRIO: {cliente.nome_cartorio}\n"
                         f"TELEFONE: {cliente.nu_telefone}\n"
                         f"EMAIL: {cliente.email_cliente}\n"
                         f"CONTA NUVEM: {cliente.conta_nuvem}\n"
                         f"NOME DO OFICIAL: {cliente.nome_oficial}\n"
                         f"LOGIN: {cliente.usuario_cliente}\n"
                         f"SENHA: {cliente.senha_cliente}")
        else:
            resultado = "Cliente não encontrado."

        self.label_resultado.delete(1.0, tk.END)  # Limpa o texto anterior
        self.label_resultado.insert(tk.END, resultado)  # novo resultado

    def voltar_menu(self):
        self.master.combo_funcionalidades.set("Menu")
        self.master.abrir_tela(None)


class TelaGerarRelatorio(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#121212')  # Cor de fundo

        self.label_relatorio = tk.Label(self, text="Relatório de Ocorrências", bg='#121212', fg='#FFC107', font=('Arial', 12))
        self.label_relatorio.pack()

        self.text_relatorio = tk.Text(self, width=80, height=20, bg='#2C2C2C', fg='white', font=('Arial', 12))
        self.text_relatorio.pack()

        self.botao_gerar = tk.Button(self, text="Gerar Relatório", command=self.gerar_relatorio, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        self.botao_gerar.pack(pady=20)

        self.botao_menu = tk.Button(self, text="Menu", command=self.voltar_menu, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        self.botao_menu.pack(side=tk.BOTTOM, anchor='se', padx=10, pady=10)

    def gerar_relatorio(self):
        relatorio = self.master.sistema.relatorio_ocorrencias()
        self.text_relatorio.delete(1.0, tk.END)  # Limpa o texto anterior
        self.text_relatorio.insert(tk.END, relatorio)

    def voltar_menu(self):
        self.master.combo_funcionalidades.set("Menu")
        self.master.abrir_tela(None)
