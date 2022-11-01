from tkinter import *

window_sped = Tk()


class Speds:

    cor_de_fundo = "DarkRed"
    cor_dentro_frame = "white"
    cor_bordas_frame = "black"

    def __init__(self):
        self.window_sped = window_sped
        self.home()
        self.frames_home()
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
                             highlightbackground= self.cor_bordas_frame,)
Speds()