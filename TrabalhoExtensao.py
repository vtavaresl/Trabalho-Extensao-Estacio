import tkinter as tk
from tkinter import ttk, messagebox

### Inclusoes ###
import os
import sqlite3

# Caminho para o banco de dados
diretorio_corrente = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(diretorio_corrente, 'database.db')

# Conexão com o banco de dados e criação da tabela, se não existir
conexao = sqlite3.connect(db_path)
query = '''CREATE TABLE IF NOT EXISTS COLABORADOR 
           (NOME_COMPLETO TEXT, NCELULAR CHAR(11), EMAIL TEXT, COMUNIDADE TEXT, AREA TEXT, SUGESTAO TEXT)'''
conexao.execute(query)
conexao.close()

######

class PrincipalProgram:
    def __init__(self, win):
        self.janela = win
        self.janela.geometry("820x600+10+10")
        self.janela.title('Bem Vindo ao Cadastro Colaborativo')

        #-----------------------------------------------------------------------------
        # Frame principal
        #-----------------------------------------------------------------------------
        self.frame_principal = tk.Frame(win)
        self.frame_principal.pack(padx=10, pady=10)

        #-----------------------------------------------------------------------------
        # Componentes principais (para inserção de dados)
        #-----------------------------------------------------------------------------
        self.lblNome = tk.Label(self.frame_principal, text='Nome Completo:')
        self.txtNome = tk.Entry(self.frame_principal, bd=2)

        self.lblCelular = tk.Label(self.frame_principal, text='Celular:')
        self.txtCelular = tk.Entry(self.frame_principal)

        self.lblEmail = tk.Label(self.frame_principal, text='Email:')
        self.txtEmail = tk.Entry(self.frame_principal)

        self.lblComunidade = tk.Label(self.frame_principal, text='Comunidade:')
        self.txtComunidade = tk.Entry(self.frame_principal)

        self.lblArea = tk.Label(self.frame_principal, text='Área:')
        self.txtArea = ttk.Combobox(self.frame_principal, width=27)
        self.txtArea['values'] = ('Alimentação', 'Educação', 'Infraestrutura', 'Negócio', 'Saneamento', 'Saúde', 'Segurança')
        self.txtArea['state'] = 'readonly'

        self.lblSugestao = tk.Label(self.frame_principal, text='Sugestão:', font=("Arial", 12))
        self.txtSugestao = tk.Text(self.frame_principal, height=11, width=40, bd=2)

        #-----------------------------------------------------------------------------
        # Barra de rolagem para a caixa de texto da Sugestão
        #-----------------------------------------------------------------------------
        self.sugestao_scrollbar = ttk.Scrollbar(self.frame_principal, orient='vertical', command=self.txtSugestao.yview)
        self.txtSugestao['yscrollcommand'] = self.sugestao_scrollbar.set

        #-----------------------------------------------------------------------------
        # TreeView para exibir os dados
        #-----------------------------------------------------------------------------
        self.dadosColunas = ('Nome', 'Celular', 'Email', 'Comunidade', 'Área', 'Sugestão')
        self.treeMedias = ttk.Treeview(self.frame_principal, columns=self.dadosColunas, show='headings')

        #-----------------------------------------------------------------------------
        # Barra de rolagem para o TreeView
        #-----------------------------------------------------------------------------
        self.verscrlbar = ttk.Scrollbar(self.frame_principal, orient='vertical', command=self.treeMedias.yview)
        self.treeMedias.configure(yscrollcommand=self.verscrlbar.set)

        #-----------------------------------------------------------------------------
        # Configuração das colunas do TreeView
        #-----------------------------------------------------------------------------
        for coluna in self.dadosColunas:
            self.treeMedias.heading(coluna, text=coluna)
            self.treeMedias.column(coluna, minwidth=0, width=120)

        #---------------------------------------------------------------------        
        # Posicionamento dos componentes na janela usando grid
        #---------------------------------------------------------------------
        # Coluna 1
        self.lblNome.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txtNome.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.lblCelular.grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.txtCelular.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        self.lblEmail.grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.txtEmail.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

        self.lblComunidade.grid(row=6, column=0, sticky='w', padx=5, pady=5)
        self.txtComunidade.grid(row=7, column=0, sticky="ew", padx=5, pady=5)

        #-----------------------------------------------------------------------------
        # Coluna 2
        self.lblComunidade.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.txtComunidade.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.lblArea.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        self.txtArea.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        #-----------------------------------------------------------------------------
        # Coluna 3
        self.lblSugestao.grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.txtSugestao.grid(row=1, column=2, rowspan=5, sticky="ew", padx=2, pady=5)

        self.sugestao_scrollbar.grid(row=1, column=3, sticky='ns', rowspan=5, pady=2)

        #-----------------------------------------------------------------------------
        # Coluna 4 (Botões)
        self.btnLogin = tk.Button(self.frame_principal, text="Login", command=self.abrir_janela_login)
        self.btnLogin.grid(row=1, column=4, padx=5, pady=5)

        self.btnLogout = tk.Button(self.frame_principal, text="Logout", command=self.fazer_logout, state='disabled')
        self.btnLogout.grid(row=2, column=4, padx=5, pady=5)

        self.btnEditar = tk.Button(self.frame_principal, text="Editar", command=self.fEditar, state='disabled')
        self.btnEditar.grid(row=3, column=4, padx=5, pady=5)

        self.btnDeletar = tk.Button(self.frame_principal, text="Deletar", command=self.fDeletar, state='disabled')
        self.btnDeletar.grid(row=4, column=4, padx=5, pady=5)

        self.btnEnviar = tk.Button(self.frame_principal, text='Enviar', command=self.fEnviarSugestao)
        self.btnEnviar.grid(row=5, column=4, padx=5, pady=10)

        #-----------------------------------------------------------------------------
        # Configurações de layout
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.columnconfigure(1, weight=1)
        self.frame_principal.columnconfigure(2, weight=2)
        self.frame_principal.columnconfigure(3, weight=0)
        self.frame_principal.columnconfigure(4, weight=0)

        #-----------------------------------------------------------------------------
        # TreeView e barra de rolagem
        self.treeMedias.grid(row=6, column=0, columnspan=3, pady=10)
        self.verscrlbar.grid(row=6, column=3, sticky='ns', pady=2)

        #---------------------------------------------------------------------
        # Carregar dados existentes do banco de dados
        #---------------------------------------------------------------------
        self.carregar_dados_existentes()

    #---------------------------------------------------------------------
    # Função para abrir uma nova janela para login
    #---------------------------------------------------------------------
    def abrir_janela_login(self):
        self.login_win = tk.Toplevel(self.janela)
        self.login_win.title("Login")
        self.login_win.geometry("200x200")

        self.lblUser = tk.Label(self.login_win, text="Login:")
        self.lblUser.pack(pady=10)
        self.txtUser = tk.Entry(self.login_win)
        self.txtUser.pack(pady=5)

        self.lblPass = tk.Label(self.login_win, text="Senha:")
        self.lblPass.pack(pady=10)
        self.txtPass = tk.Entry(self.login_win, show="*")
        self.txtPass.pack(pady=5)

        self.btnLogin = tk.Button(self.login_win, text="Login", command=self.fazer_login)
        self.btnLogin.pack(pady=20)

    #---------------------------------------------------------------------
    # Função de login
    #---------------------------------------------------------------------
    def fazer_login(self):
        login = self.txtUser.get()
        senha = self.txtPass.get()

        if login == 'admin' and senha == '123':
            messagebox.showinfo("Login bem-sucedido", "Você entrou com sucesso!")
            self.habilitar_botoes()
            self.login_win.destroy()
        else:
            messagebox.showerror("Erro de login", "Login ou senha incorretos")
            self.login_win.destroy()

    #---------------------------------------------------------------------
    # Função de logout
    #---------------------------------------------------------------------
    def fazer_logout(self):
        self.desabilitar_botoes()
        messagebox.showinfo("Logout", "Você saiu com sucesso!")

    #-----------------------------------------------------------------------------
    # Habilitar botões após login
    def habilitar_botoes(self):
        self.btnEditar.config(state='normal')
        self.btnDeletar.config(state='normal')
        self.btnLogout.config(state='normal')

    #-----------------------------------------------------------------------------
    # Desabilitar botões após logout
    def desabilitar_botoes(self):
        self.btnEditar.config(state='disabled')
        self.btnDeletar.config(state='disabled')
        self.btnLogout.config(state='disabled')

    #---------------------------------------------------------------------
    # Função para salvar dados no banco de dados
    #---------------------------------------------------------------------
    def fSalvarDados(self, nome, celular, email, comunidade, area, sugestao):
        try:
            conexao = sqlite3.connect(db_path)
            query = '''INSERT INTO COLABORADOR (NOME_COMPLETO, NCELULAR, EMAIL, COMUNIDADE, AREA, SUGESTAO) 
                       VALUES (?, ?, ?, ?, ?, ?)'''
            conexao.execute(query, (nome, celular, email, comunidade, area, sugestao))
            conexao.commit()
            conexao.close()
            print('Dados salvos com sucesso!')
        except Exception as e:
            print(f'Erro ao salvar os dados: {e}')

    #---------------------------------------------------------------------
    # Função para enviar sugestão
    #---------------------------------------------------------------------
    def fEnviarSugestao(self):
        try:
            nome = self.txtNome.get()
            celular = self.txtCelular.get()
            email = self.txtEmail.get()
            comunidade = self.txtComunidade.get()
            area = self.txtArea.get()
            sugestao = self.txtSugestao.get("1.0", tk.END).strip()

            self.treeMedias.insert('', 'end', values=(nome, celular, email, comunidade, area, sugestao))
            self.fSalvarDados(nome, celular, email, comunidade, area, sugestao)

            #-----------------------------------------------------------------------------
            # Limpar campos
            self.txtNome.delete(0, 'end')
            self.txtCelular.delete(0, 'end')
            self.txtEmail.delete(0, 'end')
            self.txtComunidade.delete(0, 'end')
            self.txtArea.set('')
            self.txtSugestao.delete("1.0", tk.END)

        except ValueError:
            print('Entre com valores válidos')

    #---------------------------------------------------------------------
    # Função para editar o dado selecionado
    #---------------------------------------------------------------------
    def fEditar(self):
        selected_item = self.treeMedias.selection()
        if selected_item:
            for item in selected_item:
                valores = self.treeMedias.item(item, 'values')

                self.txtNome.insert(0, valores[0])
                self.txtCelular.insert(0, valores[1])
                self.txtEmail.insert(0, valores[2])
                self.txtComunidade.insert(0, valores[3])
                self.txtArea.set(valores[4])
                self.txtSugestao.insert("1.0", valores[5])

                self.treeMedias.delete(item)

    #---------------------------------------------------------------------
    # Função para deletar dados
    #---------------------------------------------------------------------
    def fDeletar(self):
        selected_item = self.treeMedias.selection()
        if selected_item:
            for item in selected_item:
                valores = self.treeMedias.item(item, 'values')
                nome = valores[0]
                celular = valores[1]
                sugestao = valores[5]

                #-----------------------------------------------------------------------------
                # Remover do banco de dados
                try:
                    conexao = sqlite3.connect(db_path)
                    cursor = conexao.cursor()
                    query = "DELETE FROM COLABORADOR WHERE NOME_COMPLETO = ? AND NCELULAR = ? AND SUGESTAO = ?"
                    cursor.execute(query, (nome, celular, sugestao))
                    conexao.commit()
                    conexao.close()
                    print('Registro deletado do banco de dados.')
                except Exception as e:
                    print(f'Erro ao deletar do banco de dados: {e}')

                #-----------------------------------------------------------------------------
                # Remover da interface gráfica
                self.treeMedias.delete(item)

    #---------------------------------------------------------------------
    # Carregar dados existentes do banco de dados
    #---------------------------------------------------------------------
    def carregar_dados_existentes(self):
        try:
            conexao = sqlite3.connect(db_path)
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM COLABORADOR")
            registros = cursor.fetchall()
            for registro in registros:
                self.treeMedias.insert('', 'end', values=registro)
            conexao.close()
            print('Dados carregados com sucesso!')
        except Exception as e:
            print(f'Erro ao carregar os dados: {e}')

#---------------------------------------------------------------------
# Programa Principal
#---------------------------------------------------------------------
janela = tk.Tk()
principal = PrincipalProgram(janela)
janela.mainloop()
