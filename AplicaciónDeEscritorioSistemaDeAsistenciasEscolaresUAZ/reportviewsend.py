# -*- coding: utf-8 -*-
import Tkinter, tkMessageBox
from Tkinter import *
import Tkinter as tk
import ttk, cx_Oracle, os, base64
from ttk import *
from tkdocviewer import *
import envioReportes

class reportes(Toplevel):
    def __init__(self, correoDestinatario, Nombre, Asignatura):
        Toplevel.__init__(self)
        self.geometry("1300x850+550+200")
        self.title("REPORTE GENERADO")
        self.resizable(False,False)
	self.correo = correoDestinatario
	self.nombre = Nombre
	self.asignatura = Asignatura
	
        # Ventanas
        self.top = tk.Frame(self, height=150, bg='#113a5d')
        self.top.pack(fill=X)
        self.botonFrame = tk.Frame(self, height=800, bg='#fffcef')
        self.botonFrame.pack(fill=X)

	self.v = DocViewer(self.botonFrame, width=820, height=700)
	self.v.place(x=0, y=0)

	# Display some document
	self.v.display_file(os.getcwd()+"/Reportes/reporte.pdf")

        # Encabezado, imagen y fecha
        self.top_image = tk.PhotoImage(file='icons/uaz.png')
        self.top_image_lbl = tk.Label(self.top, image=self.top_image, bg="#113a5d")
        self.top_image_lbl.place(x=10, y=10)
        self.encabezado = tk.Label(self.top, text='REPORTE DE ASISTENCIA', font='arial 20 bold', fg='white', bg="#113a5d")
        self.encabezado.place(x=450, y=50)
	
        #Etiquetas y entradas
        self.lbl_Clave = tk.Label(self.botonFrame,text='CLAVE PARA ENVIO:',font='arial 20 bold', fg='black',bg='#fffcef')
        self.lbl_Clave.place(x=880,y=40)
        self.ent_clave = tk.Entry(self.botonFrame,width=20,bd=4,font='arial 17 bold')
	self.ent_clave.config(show='*')
        self.ent_clave.place(x=880,y=100)

	self.lbl_CD = tk.Label(self.botonFrame,text='CORREO A ENVIAR \nREPORTE:',font='arial 20 bold', fg='black',bg='#fffcef')
        self.lbl_CD.place(x=880,y=240)
        self.ent_D = tk.Entry(self.botonFrame,width=20,bd=4,font='arial 17 bold')
	self.ent_D.place(x=880,y=340)

	if self.correo != None:
		self.ent_D.insert(0, str(self.correo))
        

	boton = tk.Button(self.botonFrame,text="       ENVIAR REPORTE      ", fg='black', font='arial 15 bold', command=self.enviarReporte)
        boton.place(x=880,y=420)

	boton = tk.Button(self.botonFrame,text="       SALIR      ", fg='black', font='arial 15 bold', command=self.SalirVentana)
        boton.place(x=880,y=480)
	
    
    def enviarReporte(self):
	if self.ent_D.get() != "" and self.ent_clave.get() != "":
		t = envioReportes.EnviarCorreo(self.ent_clave.get(),self.correo,self.nombre,self.asignatura)
		if t == True:
			tkMessageBox.showinfo("Éxito","SE ENVIO EL REPORTE",icon='info')
		else:
			tkMessageBox.showerror("Error","NO SE ENVIO EL REPORTE",icon='warning')
	else:
		tkMessageBox.showerror("Error","FALTAN DATOS PARA EL ENVIO CORREO O CLAVE INCORRECTA",icon='warning')

    def SalirVentana(self):
	self.top.destroy()
        self.botonFrame.destroy()
	self.destroy()
