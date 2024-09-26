'''
classe principal da aplicação, gerenciamento das telas do aplicativo.
'''

import tkinter as tk
from tkinter import ttk
from sistema import Sistema
from telas import TelaCadastroCliente, TelaRegistrarOcorrencia, TelaConsultarClientes, TelaGerarRelatorio, TelaMenu

class Aplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador Backup Online")
        self.geometry("900x600") # defini um tamnho da tela padrão, mas pode ser alterado, ideal é deixar reponsivo no futuro.
        self.configure(bg='#000000')  # tema de cor do projeto, deixei preto como padrão.

        self.sistema = Sistema()
        self.tela_atual = None

        # Menu inicial
        self.menu_frame = tk.Frame(self, bg='#000000') # cor padrão
        self.menu_frame.pack(side=tk.TOP, anchor='nw', pady=10, padx=10)

        # Combobox para funcionalidades
        self.combo_funcionalidades = ttk.Combobox(self.menu_frame, state="readonly", width=20)
        self.combo_funcionalidades['values'] = ["Menu", "Cadastrar Cliente", "Registrar Ocorrência", "Consultar Clientes", "Gerar Relatório"]
        self.combo_funcionalidades.current(0)
        self.combo_funcionalidades.bind("<<ComboboxSelected>>", self.abrir_tela)
        self.combo_funcionalidades.pack()

        # Carrega o menu inicial
        self.abrir_tela(None)

    def abrir_tela(self, event):
        funcionalidade = self.combo_funcionalidades.get()
        
        # botão menu que faz voltar para a tela inicial do projeto
        if funcionalidade == "Menu" or funcionalidade == "":
            if self.tela_atual is not None:
                self.tela_atual.destroy()  #Destrói a tela atual, para voltar para a inicial e não ter sobreposição
            self.tela_atual = TelaMenu(self)
            self.tela_atual.pack(fill=tk.BOTH, expand=True)
            return

        if self.tela_atual is not None:
            self.tela_atual.destroy()  #Destrói a tela atual

        if funcionalidade == "Cadastrar Cliente":
            self.tela_atual = TelaCadastroCliente(self)
        elif funcionalidade == "Registrar Ocorrência":
            self.tela_atual = TelaRegistrarOcorrencia(self)
        elif funcionalidade == "Consultar Clientes":
            self.tela_atual = TelaConsultarClientes(self)
        elif funcionalidade == "Gerar Relatório":
            self.tela_atual = TelaGerarRelatorio(self)

        self.tela_atual.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = Aplicacao()
    app.mainloop() #tem que ter esse comando de loop, se não o programa roda mas não exibe a interface gráfica para o usuário
