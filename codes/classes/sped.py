from calendar import isleap
from datetime import datetime
from tkinter import *
from tkinter import ttk
import sqlite3
import psycopg2
import pandas as pd

home_page = Tk()


class Functions():
    def limpar_tela(self):
        self.entry_data.delete(0, END)
        self.entry_client.delete(0, END)
        self.entry_system.delete(0, END)
        self.entry_observation.delete(0, END)

    def conectar_bd(self):

        self.conn = psycopg2.connect(host='localhost',
                               database='SPED',
                               user='postgres',
                               password='123')
        print("Iniciando conexão")
        self.cursor = self.conn.cursor()
        print("Conectado ao Banco de Dados")

    def desconecta_bd(self):
        self.conn.close()

    def montaTabelas(self):
        self.conectar_bd()
        print("Banco de dados conectado")

        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS speds(
                            data DATE,
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
        self.cursor.execute("""
                            SELECT data, cliente, sistema, observacao 
                            FROM speds 
                            ORDER BY sistema ASC;
                            """)
        searchTar = self.cursor.fetchall()

        new_lista = [[0, 0, 0, 0]]
        try:
            for i in searchTar:
                self.list.insert("", END, values= i)
        except:
            for k in new_lista:
                self.list.insert("", END, values= k)

        self.desconecta_bd()

    def adicionarSped(self):
        self.data = self.entry_data.get()
        self.client = self.entry_client.get()
        self.sistema = self.entry_system.get()
        self.observacao = self.entry_observation.get()

        self.conectar_bd()
        self.cursor.execute("""
                        INSERT INTO speds (data, cliente, sistema, observacao)
                         VALUES (%s, %s, %s, %s)""", (self.data, self.client, self.sistema, self.observacao))
        self.conn.commit()
        self.desconecta_bd()
        self.select_bd()
        self.limpar_tela()

    def OnDoubleClick(self, event):
        self.limpar_tela()
        self.list.selection()

        for n in self.list.selection():
            col1, col2, col3, col4 = self.list.item(n, 'values')
            self.entry_data.insert(END, col1)
            self.entry_client.insert(END, col2)
            self.entry_system.insert(END, col3)
            self.entry_observation.insert(END, col4)

    def deletaSped(self):
        self.data = self.entry_data.get()
        self.client = self.entry_client.get()
        self.system = self.entry_system.get()
        self.observacao = self.entry_observation.get()

        self.conectar_bd()
        self.cursor.execute("""DELETE FROM speds WHERE data = %s and cliente = %s""", (self.data, self.client))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_bd()

    def updateSped(self):
        self.data = self.entry_data.get()
        self.client = self.entry_client.get()
        self.sistema = self.entry_system.get()
        self.observacao = self.entry_observation.get()

        self.conectar_bd()
        self.cursor.execute("""
                        UPDATE  speds SET data = %s, cliente = %s, sistema = %s, observacao = %s
                        WHERE data = %s and cliente = %s""", (self.data, self.client, self.sistema, self.observacao, self.data, self.client))
        self.conn.commit()
        self.desconecta_bd()
        self.select_bd()
        self.limpar_tela()

    def search_sped(self):
        self.conectar_bd()
        self.list.delete(*self.list.get_children())
        self.data = 0
        self.month = 0
        self.year = 0

        self.data = self.entry_data.get()


        self.month = self.data[3:5]
        self.year = self.data[6:10]

        self.data_inicial = '{}/{}/{}'.format(self.year, self.month, 1)

        self.dia_fev = 0
        self.year = int(self.year)
        self.month = int(self.month)
        if isleap(self.year):
           self.dia_fev = 29
        else:
           self.dia_fev = 28

        if self.month == 1:
            self.data_final = '{}/{}/{}'.format(self.year, self.month, 31)
        elif self.month == 2:
            self.data_final = '{}/{}/{}'.format(self.year, self.month, self.dia_fev)
        elif self.month == 3:
            self.data_final = '{}/{}/{}'.format(self.year, self.month, 31)
        elif self.month == 4:
            self.data_final = '{}/{}/{}'.format(self.year, self.month, 30)
        elif self.month == 5:
            self.data_final = '{}/{}/{}'.format(self.year, self.month, 31)
        elif self.month == 6:
            self.data_final = '{}/{}/{}'.format(self.year, self.month, 30)
        elif self.month == 7:
            self.data_final = '{}/{}/{}'.format(self.year, self.month, 31)
        elif self.month == 8:
            self.data_final = '{}/{}/{}'.format(self.year, self.month, 31)
        elif self.month == 9:
            self.data_final = '{}/{}/{}'.format(self.year, self.month, 30)
        elif self.month == 10:
            self.data_final = '{}/{}/{}'.format(self.year, self.month, 31)
        elif self.month == 11:
            self.data_final = '{}/{}/{}'.format(self.year, self.month, 30)
        else:
            self.data_final = '{}/{}/{}'.format(self.year, self.month, 31)


        self.cursor.execute("""
                        SELECT data, cliente, sistema, observacao 
                            FROM speds
                            WHERE data BETWEEN %s and %s
                            ORDER BY cliente ASC
                            """, (self.data_inicial, self.data_final))

        lista = self.cursor.fetchall()
        for i in lista:
            print(i)

        for i in lista:
            self.list.insert("", END, values=i)
        self.limpar_tela()
        self.desconecta_bd()

class Speds(Functions):

    cor_de_fundo = "LightGrey"
    cor_dentro_frame = "SteelBlue"
    cor_bordas_frame = "LightSlateGray"
    cor_texto_titulo = "Blue"
    cor_botoes = "SlateGray"

    def __init__(self):
        self.home_page = home_page
        self.home()
        self.frames_home()
        self.create_labels()
        self.create_buttons()
        self.list_frame()
        self.montaTabelas()
        self.select_bd()
        self.center(self.home_page)
        self.home_page.mainloop()

    def home(self):
        self.home_page.title("CONTROLE E ARMAZENAMENTO DOS SPEDS")
        self.home_page.geometry("800x800")
        self.home_page.configure(background= self.cor_de_fundo)
        self.home_page.resizable(False, False)

    def center(self, page):
        """ FUNÇÃO RESPONSAVEL POR CENTRALIZAR AS PAGES NA TELA"""

        page.withdraw()
        page.update_idletasks()  # Update "requested size" from geometry manager

        x = (page.winfo_screenwidth() - page.winfo_reqwidth()) / 4
        y = (page.winfo_screenheight() - page.winfo_reqheight()) / 6
        page.geometry("+%d+%d" % (x, y))

        # This seems to draw the window frame immediately, so only call deiconify()
        # after setting correct window position
        page.deiconify()

    def frames_home(self):
        self.frame_titulo = Frame(self.home_page,
                                  bd= 4,
                                  bg= self.cor_de_fundo,
                                  highlightbackground= self.cor_bordas_frame,
                                  highlightthickness= 1)
        self.frame_titulo.place(rely= 0.01, relx= 0.01, relwidth= 0.98, relheight= 0.23)

        self.frame_speds = Frame(self.home_page,
                                 bd= 4,
                                 bg= self.cor_de_fundo,
                                 highlightbackground= self.cor_bordas_frame,
                                 highlightthickness= 1)
        self.frame_speds.place(rely= 0.28, relx= 0.01, relwidth= 0.98, relheight= 0.685)

    def create_labels(self):
        self.lb_title = Label(self.frame_titulo, text= "SPEDS", font= "-weight bold -size 25",
                              bg= self.cor_de_fundo, fg= self.cor_texto_titulo)
        self.lb_title.place(rely= 0.01, relx= 0.37, relwidth= 0.2)


        self.lb_data = Label(self.frame_titulo, text= "Data Sped", font= "-weight bold -size 15",
                             bg= self.cor_de_fundo, fg= self.cor_texto_titulo)
        self.lb_data.place(rely= 0.3, relx= 0.01, relwidth= 0.2)

        self.entry_data = Entry(self.frame_titulo)
        self.entry_data.place(rely= 0.48, relx= 0.042, relwidth=0.14)


        self.lb_client = Label(self.frame_titulo, text= "Cliente", font= "-weight bold -size 15",
                               bg= self.cor_de_fundo, fg= self.cor_texto_titulo)
        self.lb_client.place(rely= 0.3, relx= 0.2, relwidth= 0.14)

        self.entry_client = Entry(self.frame_titulo)
        self.entry_client.place(rely= 0.48, relx= 0.225, relwidth= 0.14)


        self.lb_system = Label(self.frame_titulo, text= "Sistema", font= "-weight bold -size 15",
                               bg= self.cor_de_fundo, fg= self.cor_texto_titulo)
        self.lb_system.place(rely= 0.3, relx= 0.4, relwidth= 0.14)

        self.entry_system = Entry(self.frame_titulo)
        self.entry_system.place(rely= 0.48, relx= 0.42, relwidth= 0.14)


        self.lb_observation = Label(self.frame_titulo, text= "Observações", font= "-weight bold -size 15",
                                    bg= self.cor_de_fundo, fg= self.cor_texto_titulo)
        self.lb_observation.place(rely= 0.3, relx= 0.6, relwidth= 0.16)

        self.entry_observation = Entry(self.frame_titulo)
        self.entry_observation.place(rely= 0.48, relx= 0.6, relwidth= 0.3)

    def create_buttons(self):
        self.bt_cadastrar = Button(self.frame_titulo, text= "Cadastrar", background= self.cor_botoes, bd= 8, font= "-weight bold -size 10", command= self.adicionarSped)
        self.bt_cadastrar.place(rely= 0.7, relx= 0.04, relwidth= 0.1)

        self.bt_delete = Button(self.frame_titulo, text= "Excluir", background= self.cor_botoes, bd= 8, font= "-weight bold -size 10", command= self.deletaSped)
        self.bt_delete.place(rely= 0.7, relx= 0.22, relwidth= 0.1)

        self.bt_update = Button(self.frame_titulo, text= "Alterar", background= self.cor_botoes, bd= 8, font= "-weight bold -size 10", command= self.updateSped)
        self.bt_update.place(rely= 0.7, relx= 0.418, relwidth= 0.1)

        self.bt_search = Button(self.frame_titulo, text= "Buscar", background= self.cor_botoes, bd= 8, font= "-weight bold -size 10", command= self.search_sped)
        self.bt_search.place(rely= 0.7, relx= 0.6, relwidth= 0.1)

    def list_frame(self):
        self.list = ttk.Treeview(self.frame_speds, height= 3, columns= ("col1", "col2", "col3", "col4"))

        self.list.heading("#0", text= "")
        self.list.heading("#1", text= "Data")
        self.list.heading("#2", text= "Cliente")
        self.list.heading("#3", text= "Sistema")
        self.list.heading("#4", text= "Observação")
        #
        self.list.column("#0", width= 1)
        self.list.column("#1", width= 80)
        self.list.column("#2", width= 100)
        self.list.column("#3", width= 180)
        self.list.column("#4", width= 270)

        self.list.place(rely= 0.01, relx= 0.01, relwidth= 0.96, relheight= 0.98)

        self.scrollList = Scrollbar(self.frame_speds, orient= "vertical")
        self.list.configure(yscroll= self.scrollList.set)
        self.scrollList.place(relx= 0.97, rely= 0.01, relwidth= 0.02, relheight= 0.98)
        self.list.bind("<Double-1>", self.OnDoubleClick)
Speds()