# -*- coding: utf-8 -*-
import Tkinter, tkMessageBox
from Tkinter import *
import Tkinter as tk
import ttk, cx_Oracle, os, base64
from ttk import *

class Info(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("660x600+550+200")
        self.title("Información")
        self.resizable(False,False)

        # Ventanas
        self.top = tk.Frame(self, height=150, bg='#000c36')
        self.top.pack(fill=X)
        self.botonFrame = tk.Frame(self, height=600, bg='#cbac74')
        self.botonFrame.pack(fill=X)

        # Encabezado, imagen y fecha
        self.top_image = tk.PhotoImage(file='icons/uaz.png')
        self.top_image_lbl = tk.Label(self.top, image=self.top_image, bg="#000c36")
        self.top_image_lbl.place(x=10, y=10)
        self.encabezado = tk.Label(self.top, text='ACERCA DEL SISTEMA DE CONTROL\nDE ASISTENCIAS MEDIANTE\nRECONOCEDORES BIOMETRICOS', font='arial 14 bold', fg='white', bg="#000c36")
        self.encabezado.place(x=170, y=30)

        #Etiquetas y entradas
        #NombreServidor
        self.lbl_NombreServidor = tk.Label(self.botonFrame,text='SOFTWARE VERSION 1.0\n\nDESARROLLADO:\n\n EN LA UNIVERSIDAD AUTÓNOMA DE ZACATECAS\n\nSISTEMA DE CONTROL DE ASISTENCIAS ESCOLAR\n UTILIZANDO RECONOCEDORES BIOMÉTRICOS\n\nBIOMETRÍA DACTILAR Y VOZ\n\nCONGRESOS DE PRESENTACIÓN:\n\nACADEMIA JOURNALS, SENIE, JORNADA ESTATAL\nDE LA CIENCIA Y LA TECNOLOGÍA\n\n',font='arial 15 bold', fg='black',bg='#cbac74')
        self.lbl_NombreServidor.grid(row=0,column=0)  
        


