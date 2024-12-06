import locale
import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry


class TelaLogin(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#121212')  # Cor de fundo
        
        #Frame
        self.pack(expand=True, fill='both')

        #Centralização
        frame_central = tk.Frame(self, bg='#121212')
        frame_central.place(relx=0.5, rely=0.5, anchor='center')

        #Caminho imagem de login
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        
        image_path = os.path.join(base_path, 'chave-eletronica.png')

        # Carregando a imagem
        self.imagem_database = Image.open(image_path)
        self.imagem_database = self.imagem_database.resize((100, 100), Image.LANCZOS)
        self.imagem_database_tk = ImageTk.PhotoImage(self.imagem_database)

        # Imagem tela de login
        label_imagem = tk.Label(frame_central, image=self.imagem_database_tk, bg='#121212')
        label_imagem.pack(pady=10)

        label_usuario = tk.Label(frame_central, text="Usuário:", bg='#121212', fg='#FFC107', font=('Arial', 12))
        label_usuario.pack(pady=10)
        self.entry_usuario = tk.Entry(frame_central, width=30)
        self.entry_usuario.pack()

        label_senha = tk.Label(frame_central, text="Senha:", bg='#121212', fg='#FFC107', font=('Arial', 12))
        label_senha.pack(pady=10)
        self.entry_senha = tk.Entry(frame_central, show='*', width=30)  # Campo senha (*****)
        self.entry_senha.pack()

        botao_login = tk.Button(frame_central, text="Login", command=self.fazer_login, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        botao_login.pack(pady=20)

        botao_acesso_visitante = tk.Button(frame_central, text="Acesso como visitante", command=self.acesso_visitante, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        botao_acesso_visitante.pack()

    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        self.master.autenticar(usuario, senha)

    def acesso_visitante(self):
        self.master.autenticar(None, None)



class TelaMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#121212')  # Cor de fundo

        # Imagem
        self.imagem_path = os.path.join(os.path.dirname(__file__), 'database.png')
        self.img = Image.open(self.imagem_path)
        self.img = self.img.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.img)

        self.label_imagem = tk.Label(self, image=self.photo, bg='#121212')
        self.label_imagem.place(relx=0.5, rely=0.35, anchor='center')  # Centraliza a imagem com ajuste

        tipo_usuario = "Administrador do Backup Manager" if self.master.usuario_logado == "admin" else "Visitante"

        label_bem_vindo = tk.Label(self, text=f"Bem-vindo, {tipo_usuario}", bg='#121212', fg='#FFC107', font=('Arial', 14, 'bold'))
        label_bem_vindo.place(relx=0.49, rely=0.45, anchor='center')  # Ajustado para menor espaçamento

        label_instrucoes = tk.Label(self, text="Escolha uma funcionalidade no menu", bg='#121212', fg='#FFC107', font=('Arial', 14, 'bold'))
        label_instrucoes.place(relx=0.49, rely=0.5, anchor='center')  # Ajustado para menor espaçamento

        # Botão "Trocar usuário"
        #botao_trocar_usuario = tk.Button(self, text="Trocar usuário", command=self.trocar_usuario, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        #botao_trocar_usuario.place(relx=0.95, rely=0.05, anchor='ne')  # Canto superior direito

        self.pack(expand=True, fill='both')

    def trocar_usuario(self):
        # Chama a função de logout e volta para a tela de login
        self.master.usuario_logado = None
        self.master.abrir_tela_login()  # Certifique-se de usar o nome correto do método


class TelaCadastroCliente(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#121212')  # Cor de fundo

        # Título da tela
        self.titulo = tk.Label(self, text="Cadastro de Clientes de Backup", bg='#121212', fg='#FFC107', font=('Arial', 16, 'bold'))
        self.titulo.pack(pady=10)

        self.create_label_entry("Cartório:")
        self.create_label_entry("Número SAC Formato 0000:")
        self.create_combobox("UF", ["SC", "PR", "PA", "MA", "AC"])
        self.create_combobox("Conta Nuvem",
        ["backup@extradigital-backup.com", "backup2@extradigital-backup.com", "backup3@extradigital-backup.com", "backup4@extradigital-backup.com", "backup5@extradigital-backup.com", "backup6@extradigital-backup.com", "backup7@extradigital-backup.com", "backup8@extradigital-backup.com", "backup9@extradigital-backup.com", "backup10@extradigital-backup.com"])
        self.create_label_entry("Nome Oficial:")
        self.create_label_entry("Número de Telefone:")
        self.create_label_entry("Número Do Telefone 2:")
        self.create_label_entry("Email do Cliente:")
        self.create_label_entry("Usuário:")
        self.create_label_entry("Senha:")
        self.create_label_entry("Horário Backup Diário")

        self.botao_cadastrar = tk.Button(self, text="Cadastrar Cliente", command=self.cadastrar_cliente, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        self.botao_cadastrar.pack(pady=20)

        self.botao_menu = tk.Button(self, text="Menu", command=self.voltar_menu, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        self.botao_menu.pack(side=tk.BOTTOM, anchor='se', padx=10, pady=10)
        
    #a função a seguir, é para todos os campos da tela de cadastro, ou seja, a edição dos campos é de forma conjunta.
    def create_label_entry(self, text, show=None):
        label = tk.Label(self, text=text, bg='#121212', fg='#FFC107', font=('Arial', 12))
        label.pack()
        entry = tk.Entry(self, show=show, width=30)  #largura dos campos de entrada
        entry.pack(pady=3)  #espaçamento entre os campos
        safe_name = text.replace(" ", "_").replace(":", "").replace("ç", "c").lower()  # Substituir caracteres especiais
        setattr(self, f'entry_{safe_name}', entry)  # Criar o atributo dinamicamente

    def create_combobox(self, text, options):
        label = tk.Label(self, text=text, bg='#121212', fg='#FFC107', font=('Arial', 12))
        label.pack()
        combobox = ttk.Combobox(self, values=options, state="readonly", width=28)  # Combobox com opções
        combobox.pack(pady=3)
        safe_name = text.replace(" ", "_").replace(":", "").replace("ç", "c").lower()
        setattr(self, f'entry_{safe_name}', combobox)

    #função de cadastrar cliente, pega as informações em cada campo pelo método get e armazena para enviar para o banco de dados.
    def cadastrar_cliente(self):
        cliente_data = {
            "Cartório": self.entry_cartório.get(),
            "Número SAC Formato 0000": self.entry_número_sac_formato_0000.get(),
            "UF": self.entry_uf.get(),
            "Conta Nuvem": self.entry_conta_nuvem.get(),
            "Nome Oficial": self.entry_nome_oficial.get(),
            "Número de Telefone": self.entry_número_de_telefone.get(),
            "Número Do Telefone 2": self.entry_número_do_telefone_2.get(),
            "Email do Cliente": self.entry_email_do_cliente.get(),
            "Usuário": self.entry_usuário.get(),
            "Senha": self.entry_senha.get(),
            "Horário Backup Diário": self.entry_horário_backup_diário.get()
    }

        if not cliente_data["Número SAC Formato 0000"].isdigit() or len(cliente_data["Número SAC Formato 0000"]) != 4:
                messagebox.showerror("Erro", "O Número SAC deve conter exatamente 4 dígitos numéricos!")
                return

        resultado = self.master.sistema.cadastrar_cliente(**cliente_data)
        messagebox.showinfo("Cadastro de Cliente", resultado)


        # Limpar todos os campos
        for attr in cliente_data.keys():
        # Modifica a formatação para o nome correto dos atributos dinâmicos
            safe_name = attr.replace(" ", "_").replace(":", "").replace("ç", "c").lower()
            try:
                getattr(self, f'entry_{safe_name}').delete(0, tk.END)
            except AttributeError:
                print(f"Campo '{safe_name}' não encontrado.")

    def voltar_menu(self):
        self.master.combo_funcionalidades.set("Menu")
        self.master.abrir_tela(None)


class TelaRegistrarOcorrencia(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#121212')

        # Frame para centralizar o título
        self.frame_titulo = tk.Frame(self, bg='#121212')  # Fundo preto para o frame do título
        self.frame_titulo.grid(row=0, column=0, columnspan=2, sticky="n", pady=20)  # Adicionando o título no topo com espaçamento

        # Título centralizado dentro do frame
        self.titulo = tk.Label(self.frame_titulo, text="Registro de Ocorrências de Backup", bg='#121212', fg='#FFC107', font=('Arial', 16, 'bold'))
        self.titulo.pack()  # Centraliza o título dentro do frame

        # Configuração da grid principal para os outros componentes
        self.grid_columnconfigure(0, weight=1)  # coluna para o botão no canto esquerdo
        self.grid_columnconfigure(1, weight=1)  # coluna central para outros componentes

        # Nº SAC do Cliente
        self.label_id_cliente = tk.Label(self, text="Nº SAC do Cliente:\n(Formato 0000)", bg='#121212', fg='#FFC107', font=('Arial', 12))
        self.label_id_cliente.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_id_cliente = tk.Entry(self, width=35)
        self.entry_id_cliente.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Banco
        self.label_tipo_banco = tk.Label(self, text="Banco:", bg='#121212', fg='#FFC107', font=('Arial', 12))
        self.label_tipo_banco.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.combobox_tipo_banco = ttk.Combobox(self, values=["PROD", "IMG", "AUD", "ANX", "OUTROS", "TODOS"], state="readonly", width=33)
        self.combobox_tipo_banco.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Tipo Da Ocorrência
        self.label_tipeocorrencia = tk.Label(self, text="Tipo Da Ocorrência:", bg='#121212', fg='#FFC107', font=('Arial', 12))
        self.label_tipeocorrencia.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.combobox_tipeocorrencia = ttk.Combobox(self, values=["Não subiu para a nuvem", "Backup não executado", "SAC"], state="readonly", width=33)
        self.combobox_tipeocorrencia.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Descrição
        self.label_DescriOcorrencia = tk.Label(self, text="Descrição:", bg='#121212', fg='#FFC107', font=('Arial', 12))
        self.label_DescriOcorrencia.grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.combobox_DescriOcorrencia = ttk.Combobox(
            self,
            values=[
                "Ativação do Serviço de Backup Online",
                "Serviço ok, mas não conclui upload",
                "Não rodou backup do dia anterior",
                "Backup executado, mas não subiu",
                "Servidor do cliente estragou",
                "Relatório SAC desatualizado",
                "Cliente usando o servidor",
                "Deixou de ser cliente",
                "Sem espaço em disco",
                "Servidor sem acesso",
                "Banco corrompido",
                "Outros"
            ],
            state="readonly", width=33
        )
        self.combobox_DescriOcorrencia.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        # Ocorrência Solucionada
        self.label_solucionado = tk.Label(self, text="Ocorrência Solucionada?", bg='#121212', fg='#FFC107', font=('Arial', 12))
        self.label_solucionado.grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.combobox_solucionado = ttk.Combobox(self, values=["NÃO", "SIM"], state="readonly", width=33)
        self.combobox_solucionado.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        # Configuração de "Data da Ocorrência" com as cores especificadas
        locale.setlocale(locale.LC_ALL, 'pt_BR')
        self.label_data_ocorrencia = tk.Label(self, text="Data da Ocorrência:", bg='#121212', fg='#FFC107', font=('Arial', 12))
        self.label_data_ocorrencia.grid(row=6, column=0, sticky="e", padx=5, pady=5)

        # Estilização do DateEntry
        self.data_ocorrencia = DateEntry(self, width=12,
            background='#333333',       # Fundo do campo de entrada do calendário
            foreground='#FFC107',       # Cor do texto do campo de entrada do calendário
            borderwidth=2,
            year=2024,
            date_pattern='y-mm-dd',     # Formato de data yyyy-mm-dd
            font=('Arial', 11),
            headersbackground='#333333', # Fundo do cabeçalho (mês e dias da semana)
            headersforeground='#FFC107', # Cor do texto do cabeçalho
            weekendbackground='#8B0000', # Fundo dos finais de semana
            weekendforeground='#FFC107', # Texto dos finais de semana
            normalbackground='#121212',  # Fundo dos dias normais
            normalforeground='#FFC107',  # Texto dos dias normais
            selectbackground='#FFC107',  # Fundo da data selecionada
            selectforeground='#000000'   # Texto da data selecionada
        )
        self.data_ocorrencia.grid(row=6, column=1, sticky="w", padx=5, pady=5)

        # Botão Registrar Ocorrência
        self.botao_registrar = tk.Button(self, text="Registrar Ocorrência", command=self.registrar_ocorrencia, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        self.botao_registrar.grid(row=7, column=0, columnspan=2, pady=20)

        # Tabela estilo Excel
        self.tree = ttk.Treeview(self, columns=("id_cliente", "tipo_banco", "tipo_ocorrencia", "descricao", "solucionado", "data_ocorrencia"), show="headings")
        self.tree.heading("id_cliente", text="Nº SAC")
        self.tree.heading("tipo_banco", text="Banco")
        self.tree.heading("tipo_ocorrencia", text="Tipo da Ocorrência")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("solucionado", text="Solucionado")
        self.tree.heading("data_ocorrencia", text="Data da Ocorrência")
        self.tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Configura a scrollbar para a tabela
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=8, column=2, sticky="ns")

        # Botão Menu
        self.botao_menu = tk.Button(self, text="Menu", command=self.voltar_menu, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        self.botao_menu.grid(row=9, column=1, sticky="e", padx=10, pady=10)

    def registrar_ocorrencia(self):
        id_cliente = self.entry_id_cliente.get()
        tipo_banco = self.combobox_tipo_banco.get()
        tipo_ocorrencia = self.combobox_tipeocorrencia.get()
        descricao = self.combobox_DescriOcorrencia.get()
        solucionado = self.combobox_solucionado.get()
        data_ocorrencia = self.data_ocorrencia.get_date().strftime("%Y/%m/%d")  # Formato yyyy/mm/dd

    # Registrar a ocorrência no sistema e verificar o resultado
        resultado = self.master.sistema.registrar_ocorrencia(
            id_cliente, tipo_banco, tipo_ocorrencia, descricao, solucionado, data_ocorrencia
        )

        if resultado == "Ocorrência registrada com sucesso!":
        # Exibe mensagem de sucesso
            messagebox.showinfo("Registro de Ocorrência", resultado)

        # Adiciona a nova ocorrência na tabela estilo Excel
            self.tree.insert("", "end", values=(id_cliente, tipo_banco, tipo_ocorrencia, descricao, solucionado, data_ocorrencia))

        # Limpar campos
            self.entry_id_cliente.delete(0, tk.END)
            self.combobox_tipo_banco.set('')
            self.combobox_tipeocorrencia.set('')
            self.combobox_DescriOcorrencia.set('')
            self.combobox_solucionado.set('')
        else:
        # Não exibe outra mensagem, pois o erro já foi tratado no sistema.py
            pass



    def voltar_menu(self):
        self.master.combo_funcionalidades.set("Menu")
        self.master.abrir_tela(None)


class TelaConsultarClientes(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#121212')  #fundo

        # Título da tela
        self.titulo = tk.Label(self, text="Consulta de Dados do Cliente", bg='#121212', fg='#FFC107', font=('Arial', 16, 'bold'))
        self.titulo.pack(pady=10)

        self.label_busca = tk.Label(self, text="Digite o número do SAC:\n(Formato 0000)", bg='#121212', fg='#FFC107', font=('Arial', 12))
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
        #A parte a seguir que mostra as informações do cliente ao consultar no sistema, está dessa forma as setas (Desalinhada), para manter
        # o alinhamento no sistema, caso as setas fiquem alinhadas aqui no fonte, irão desalinhar no sistema.
        cliente = self.master.sistema.clientes.get((nu_sac), None)
        if cliente:
            resultado = (f"CARTÓRIO          --> {cliente.nome_cartorio}\n"
                         f"UF                         --> {cliente.uf}\n"
                         f"TELEFONE         --> {cliente.nu_telefone}\n"
                         f"TELEFONE 2      --> {cliente.nu_telefone2}\n"
                         f"EMAIL                  --> {cliente.email_cliente}\n"
                         f"CONTA NUVEM --> {cliente.conta_nuvem}\n"
                         f"OFICIAL               --> {cliente.nome_oficial}\n"
                         f"HORÁRIO BACKUP\nDIÁRIO                 --> {cliente.hr_backup_diario}\n"
                         f"LOGIN                  --> {cliente.usuario_cliente}\n"
                         f"SENHA                --> {cliente.senha_cliente}")
        else:
            resultado = "Cliente não encontrado."

        self.label_resultado.delete(1.0, tk.END)  # Limpa o texto anterior
        self.label_resultado.insert(tk.END, resultado)  # novo resultado

    def voltar_menu(self):
        self.master.combo_funcionalidades.set("Menu")
        self.master.abrir_tela(None)


class TelaConsultarOcorrencia(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#121212')  # Cor de fundo

        self.label_relatorio = tk.Label(self, text="Relatório de Ocorrências", bg='#121212', fg='#FFC107', font=('Arial', 16, 'bold'))
        self.label_relatorio.pack(pady=10)

        # Campo de entrada para o número SAC
        self.label_sac = tk.Label(self, text="Número SAC", bg='#121212', fg='#FFC107', font=('Arial', 12))
        self.label_sac.pack(pady=5)
        self.entry_sac = tk.Entry(self, width=30, font=('Arial', 12))
        self.entry_sac.pack(pady=5)

        # Campos para data inicial e final
        self.label_data_inicio = tk.Label(self, text="Data Início", bg='#121212', fg='#FFC107', font=('Arial', 12))
        self.label_data_inicio.pack(pady=5)
        self.data_inicio = DateEntry(self, width=12,
                                     background='#333333',
                                     foreground='#FFC107',
                                     borderwidth=2,
                                     year=2024,
                                     date_pattern='y-mm-dd',
                                     font=('Arial', 12),
                                     headersbackground='#333333',
                                     headersforeground='#FFC107',
                                     weekendbackground='#8B0000',
                                     weekendforeground='#FFC107',
                                     normalbackground='#121212',
                                     normalforeground='#FFC107',
                                     selectbackground='#FFC107',
                                     selectforeground='#000000')
        self.data_inicio.pack(pady=5)

        self.label_data_fim = tk.Label(self, text="Data Fim", bg='#121212', fg='#FFC107', font=('Arial', 12))
        self.label_data_fim.pack(pady=5)
        self.data_fim = DateEntry(self, width=12,
                                  background='#333333',
                                  foreground='#FFC107',
                                  borderwidth=2,
                                  year=2024,
                                  date_pattern='y-mm-dd',
                                  font=('Arial', 12),
                                  headersbackground='#333333',
                                  headersforeground='#FFC107',
                                  weekendbackground='#8B0000',
                                  weekendforeground='#FFC107',
                                  normalbackground='#121212',
                                  normalforeground='#FFC107',
                                  selectbackground='#FFC107',
                                  selectforeground='#000000')
        self.data_fim.pack(pady=5)

        # Botão para gerar o relatório
        self.botao_gerar = tk.Button(self, text="Consultar Ocorrências", command=self.gerar_relatorio, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        self.botao_gerar.pack(pady=10)  # Espaçamento ajustado

        # Frame para o relatório e scrollbar
        frame_relatorio = tk.Frame(self, bg='#121212')
        frame_relatorio.pack(pady=20)

        # Área de texto para exibir o relatório com scrollbar
        self.text_relatorio = tk.Text(frame_relatorio, width=80, height=15, bg='#2C2C2C', fg='#FFC107', font=('Arial', 12), wrap='word')
        scrollbar = tk.Scrollbar(frame_relatorio, command=self.text_relatorio.yview)
        self.text_relatorio.config(yscrollcommand=scrollbar.set)

         # Botão para voltar ao menu, agora dentro do grid
        self.botao_menu = tk.Button(frame_relatorio, text="Menu", command=self.voltar_menu, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
        self.botao_menu.grid(row=1, column=0, sticky='e', padx=10, pady=10)
        
        # Posiciona a área de texto e a scrollbar
        self.text_relatorio.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Expansão do frame para acomodar o redimensionamento
        frame_relatorio.grid_columnconfigure(0, weight=1)
        frame_relatorio.grid_rowconfigure(0, weight=1)

        
    def gerar_relatorio(self):
        # Captura os valores dos filtros
        nu_sac = self.entry_sac.get()
        data_inicio = self.data_inicio.get()
        data_fim = self.data_fim.get()

        # Gera o relatório com os filtros
        relatorio = self.master.sistema.relatorio_ocorrencias(nu_sac, data_inicio, data_fim)

        # Limpa o texto anterior e insere o novo relatório
        self.text_relatorio.delete(1.0, tk.END)

        # Verifica se o relatório está vazio
        if relatorio.strip():
            self.text_relatorio.insert(tk.END, relatorio)
        else:
            self.text_relatorio.insert(tk.END, "Nenhuma ocorrência encontrada para os filtros fornecidos.")

    def voltar_menu(self):
        self.master.combo_funcionalidades.set("Menu")
        self.master.abrir_tela(None)