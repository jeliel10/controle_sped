from tkinter import *
from tkinter import ttk
import sqlite3

window_sped = Tk()


class Functions():
    def limpar_tela(self):
        self.entry_codigo.delete(0, END)
        self.entry_ano.delete(0, END)
        self.entry_mes.delete(0, END)
        self.entry_dia.delete(0, END)
        self.entry_client.delete(0, END)
        self.entry_sistema.delete(0, END)
        self.entry_observacao.delete(0, END)

    def conectar_bd(self):
        self.conn = sqlite3.connect("armazenamento_speds.bd")
        self.cursor = self.conn.cursor()
        print("Conectado ao Banco de Dados")

    def desconecta_bd(self):
        self.conn.close()

    def montaTabelas(self):
        self.conectar_bd()
        print("Banco de dados conectado")

        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS speds(
                            codigo INTEGER PRIMARY KEY,
                            ano INTEGER NOT NULL,
                            mes INTEGER,
                            dia INTEGER,
                            cliente VARCHAR(200),
                            sistema VARCHAR(200),
                            observacao VARCHAR(500)
                        );
                    """)
        self.conn.commit()
        print("Banco de dados criado")
        self.desconecta_bd()

    def select_bd(self):
        self.list.delete(*self.list.get_children())
        self.conectar_bd()
        lista = self.cursor.execute("""
                            SELECT codigo, ano, mes, dia, cliente, sistema, observacao 
                            FROM speds 
                            ORDER BY sistema ASC;
                            """)
        for i in lista:
            self.list.insert("", END, values= i)
        self.desconecta_bd()

    def adicionarSped(self):
        self.ano = self.entry_ano.get()
        self.mes = self.entry_mes.get()
        self.dia = self.entry_dia.get()
        self.client = self.entry_client.get()
        self.sistema = self.entry_sistema.get()
        self.observacao = self.entry_observacao.get()

        self.conectar_bd()
        self.cursor.execute("""
                        INSERT INTO speds (ano, mes, dia, cliente, sistema, observacao)
                         VALUES (?, ?, ?, ?, ?, ?)""", (self.ano, self.mes, self.dia, self.client, self.sistema, self.observacao))
        self.conn.commit()
        self.desconecta_bd()
        self.select_bd()
        self.limpar_tela()

    def OnDoubleClick(self, event):
        self.limpar_tela()
        self.list.selection()

        for n in self.list.selection():
            col1, col2, col3, col4, col5, col6, col7 = self.list.item(n, 'values')
            self.entry_codigo.insert(END, col1)
            self.entry_ano.insert(END, col2)
            self.entry_mes.insert(END, col3)
            self.entry_dia.insert(END, col4)
            self.entry_client.insert(END, col5)
            self.entry_sistema.insert(END, col6)
            self.entry_observacao.insert(END, col7)

    def deletaSped(self):
        self.codigo = self.entry_codigo.get()
        self.ano = self.entry_ano.get()
        self.mes = self.entry_mes.get()
        self.dia = self.entry_dia.get()
        self.client = self.entry_client.get()
        self.sistema = self.entry_sistema.get()
        self.observacao = self.entry_observacao.get()

        self.conectar_bd()
        self.cursor.execute("""DELETE FROM speds WHERE codigo = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_bd()

    def updateSped(self):
        self.codigo = self.entry_codigo.get()
        self.ano = self.entry_ano.get()
        self.mes = self.entry_mes.get()
        self.dia = self.entry_dia.get()
        self.client = self.entry_client.get()
        self.sistema = self.entry_sistema.get()
        self.observacao = self.entry_observacao.get()

        self.conectar_bd()
        self.cursor.execute("""
                        UPDATE  speds SET ano = ?, mes = ?, dia = ?, cliente = ?, sistema = ?, observacao = ?
                        WHERE codigo = ?""", (self.ano, self.mes, self.dia, self.client, self.sistema, self.observacao, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_bd()
        self.limpar_tela()

    def search_sped(self):
        self.conectar_bd()
        self.list.delete(*self.list.get_children())

        # self.entry_ano.insert(END, '%')
        # self.entry_mes.insert(END, '%')
        self.ano = self.entry_ano.get()
        self.mes = self.entry_mes.get()
        self.dia = self.entry_dia.get()

        self.cursor.execute("""
                        SELECT codigo, ano, mes, dia, cliente, sistema, observacao 
                        FROM speds
                        WHERE ano = ? AND mes = ?  
                        ORDER BY dia ASC
                        """, (self.ano, self.mes))

        searchTar = self.cursor.fetchall()
        for i in searchTar:
            self.list.insert("", END, values= i)
        self.limpar_tela()
        self.desconecta_bd()

class Speds(Functions):

    cor_de_fundo = "DarkRed"
    cor_dentro_frame = "Navy"
    cor_bordas_frame = "black"
    cor_texto_titulo = "DarkRed"
    cor_botoes = "Red"

    def __init__(self):
        self.window_sped = window_sped
        self.home()
        self.frames_home()
        self.create_labels()
        self.create_buttons()
        self.list_frame()
        self.montaTabelas()
        self.select_bd()
        self.window_sped.mainloop()

    def home(self):
        self.window_sped.title("Controle e Armazenamento dos Speds")
        self.window_sped.geometry("1500x900")
        self.window_sped.configure(background= self.cor_de_fundo)
        self.window_sped.resizable(True, True)
        self.window_sped.minsize(width= 1000, height= 800)

    def frames_home(self):
        self.frame_1 = Frame(self.window_sped,
                             bd= 4,
                             bg= self.cor_dentro_frame,
                             highlightbackground= self.cor_bordas_frame,
                             highlightthickness= 5)
        self.frame_1.place(rely=0.01, relx=0.01, relwidth=0.98, relheight=0.08)

        self.frame_2 = Frame(self.window_sped,
                             bd= 4,
                             bg= self.cor_dentro_frame,
                             highlightbackground= self.cor_bordas_frame,
                             highlightthickness= 5)
        self.frame_2.place(rely= 0.1, relx= 0.01, relwidth= 0.98, relheight= 0.2)

        self.frame_3 = Frame(self.window_sped,
                             bd= 4,
                             bg= self.cor_dentro_frame,
                             highlightbackground= self.cor_bordas_frame,
                             highlightthickness= 5)
        self.frame_3.place(rely= 0.315, relx= 0.01, relwidth= 0.98, relheight= 0.66)

    def create_labels(self):
        self.lb_title = Label(self.frame_1, text= "CONTROLE E ARMAZENAMENTO DOS SPEDS", font= "-weight bold -size 28", bg= self.cor_dentro_frame, fg= self.cor_texto_titulo)
        self.lb_title.place(rely= 0.01, relx= 0.2, relwidth= 0.6)


        self.lb_codigo = Label(self.frame_2, text= "Código", font= 15)
        self.lb_codigo.place(rely= 0.01, relx= 0.01, relwidth= 0.045)

        self.entry_codigo = Entry(self.frame_2)
        self.entry_codigo.place(rely= 0.2, relx= 0.01, relwidth= 0.046)


        self.lb_dia = Label(self.frame_2, text= "Dia", font= 15)
        self.lb_dia.place(rely= 0.01, relx= 0.1, relwidth= 0.045)

        self.entry_dia = Entry(self.frame_2)
        self.entry_dia.place(rely= 0.2, relx= 0.1, relwidth= 0.045)


        self.lb_ano = Label(self.frame_2, text= "Ano", font= 15)
        self.lb_ano.place(rely= 0.4, relx= 0.01, relwidth= 0.045)

        self.entry_ano = Entry(self.frame_2)
        self.entry_ano.place(rely= 0.6, relx= 0.01, relwidth= 0.046)


        self.lb_mes = Label(self.frame_2, text= "Mês", font= 15)
        self.lb_mes.place(rely= 0.4, relx= 0.1, relwidth= 0.045)

        self.entry_mes = Entry(self.frame_2)
        self.entry_mes.place(rely= 0.6, relx= 0.1, relwidth= 0.046)


        self.lb_client = Label(self.frame_2, text= "Cliente", font= 15)
        self.lb_client.place(rely= 0.01, relx= 0.18, relwidth= 0.045)

        self.entry_client = Entry(self.frame_2)
        self.entry_client.place(rely= 0.2, relx= 0.18, relwidth= 0.136)


        self.lb_sistema = Label(self.frame_2, text= "Sistema", font= 15)
        self.lb_sistema.place(rely= 0.4, relx= 0.18, relwidth= 0.045)

        self.entry_sistema = Entry(self.frame_2)
        self.entry_sistema.place(rely= 0.6, relx= 0.18, relwidth= 0.06)


        self.lb_observacao = Label(self.frame_2, text= "Observações", font= 15)
        self.lb_observacao.place(rely=0.01, relx= 0.35, relwidth= 0.075)

        self.entry_observacao = Entry(self.frame_2)
        self.entry_observacao.place(rely= 0.2, relx= 0.35, relwidth= 0.6)

    def create_buttons(self):
        self.bt_cadastrar = Button(self.frame_2, text= "Cadastrar", background= self.cor_botoes, bd= 5, command= self.adicionarSped)
        self.bt_cadastrar.place(rely= 0.45, relx= 0.35, relwidth= 0.045)

        self.bt_alterar = Button(self.frame_2, text= "Alterar", background= self.cor_botoes, bd= 5, command= self.updateSped)
        self.bt_alterar.place(rely= 0.45, relx= 0.41, relwidth= 0.045)

        self.bt_buscar = Button(self.frame_2, text= "Buscar", background= self.cor_botoes, bd= 5, command= self.search_sped)
        self.bt_buscar.place(rely= 0.45, relx= 0.47, relwidth= 0.045)

        self.bt_apagar = Button(self.frame_2, text= "Apagar", background= self.cor_botoes, bd= 5, command= self.deletaSped)
        self.bt_apagar.place(rely= 0.45, relx= 0.53, relwidth= 0.045)

    def list_frame(self):
        self.list = ttk.Treeview(self.frame_3, height= 3, columns= ("col1", "col2", "col3", "col4", "col5", "col6", "col7"))

        self.list.heading("#0", text= "")
        self.list.heading("#1", text= "Código")
        self.list.heading("#2", text= "Ano")
        self.list.heading("#3", text= "Mês")
        self.list.heading("#4", text= "Dia")
        self.list.heading("#5", text= "Cliente")
        self.list.heading("#6", text= "Sistema")
        self.list.heading("#7", text= "Observação")

        self.list.column("#0", width= 1)
        self.list.column("#1", width= 20)
        self.list.column("#2", width= 20)
        self.list.column("#3", width= 20)
        self.list.column("#4", width= 20)
        self.list.column("#5", width= 200)
        self.list.column("#6", width= 50)
        self.list.column("#7", width= 500)

        self.list.place(rely= 0.01, relx= 0.01, relwidth= 0.96, relheight= 0.98)

        self.scrollList = Scrollbar(self.frame_3, orient= "vertical")
        self.list.configure(yscroll= self.scrollList.set)
        self.scrollList.place(relx= 0.97, rely= 0.01, relwidth= 0.02, relheight= 0.98)
        self.list.bind("<Double-1>", self.OnDoubleClick)
Speds()