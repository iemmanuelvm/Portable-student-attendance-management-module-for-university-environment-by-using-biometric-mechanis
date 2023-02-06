# -*- coding: utf-8 -*-
import Tkinter, tkMessageBox
from Tkinter import *
import Tkinter as tk
import ttk, cx_Oracle, os, base64
from ttk import *


class ConfigurarConexion(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("580x580+550+200")
        self.title("CONFIGURACION DE LA BASE DE DATOS")
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
        self.encabezado = tk.Label(self.top, text='Configuración de la \n Base De Datos', font='arial 20 bold', fg='white',
                                bg="#000c36")
        self.encabezado.place(x=220, y=30)

        #Etiquetas y entradas
        #NombreServidor
        self.lbl_NombreServidor = tk.Label(self.botonFrame,text='Servidor:',font='arial 15 bold', fg='black',bg='#cbac74')
        self.lbl_NombreServidor.place(x=40,y=40)
        self.ent_NombreServidor = tk.Entry(self.botonFrame,width=30,bd=4)
        self.ent_NombreServidor.place(x=190,y=45)
        #NumeroPuerto
        self.lbl_NumeroPuerto = tk.Label(self.botonFrame, text = 'Puerto:', font = 'arial 15 bold', fg = 'black',bg='#cbac74')
        self.lbl_NumeroPuerto.place(x=40, y=80)
        self.ent_NumeroPuerto = tk.Entry(self.botonFrame, width=30, bd=4)
        self.ent_NumeroPuerto.place(x=190, y=85)
        #Sid
        self.lbl_Sid = tk.Label(self.botonFrame, text = 'SID:', font = 'arial 15 bold', fg = 'black', bg = '#cbac74')
        self.lbl_Sid.place(x=40, y=120)
        self.ent_Sid = tk.Entry(self.botonFrame, width=30, bd=4)
        self.ent_Sid.place(x=190, y=125)
        #User
        self.lbl_User = tk.Label(self.botonFrame, text = 'User:', font = 'arial 15 bold', fg = 'black', bg = '#cbac74')
        self.lbl_User.place(x=40, y=160)
        self.ent_User = tk.Entry(self.botonFrame, width=30, bd=4)
        self.ent_User.place(x=190, y=165)
        #Pass
        self.lbl_Pass = tk.Label(self.botonFrame, text = 'Password:', font = 'arial 15 bold', fg = 'black', bg = '#cbac74')
        self.lbl_Pass.place(x=40, y=200)
        self.ent_Pass = tk.Entry(self.botonFrame, width=30, bd=4)
	self.ent_Pass.config(show='*')
        self.ent_Pass.place(x=190, y=205)
	#Pass
        self.lbl_Passc = tk.Label(self.botonFrame, text = 'Password\nCorreo:', font = 'arial 15 bold', fg = 'black', bg = '#cbac74')
        self.lbl_Passc.place(x=40, y=300)
        self.ent_Passc = tk.Entry(self.botonFrame, width=30, bd=4)
	self.ent_Passc.config(show='*')
        self.ent_Passc.place(x=190, y=305)
        # Boton
        boton = tk.Button(self.botonFrame,text="Comprobar Conexión", fg='black', font='arial 12 bold', command=self.confdb)
        boton.place(x=230,y=255)
        self.lift()
	# Boton
        boton1 = tk.Button(self.botonFrame,text="Guardar Clave Correo", fg='black', font='arial 12 bold', command=self.correo)
        boton1.place(x=230,y=350)
        self.lift()

    def correo(self):
	if(self.ent_Passc.get() != ""):
		f2 = open (os.getcwd()+"/RASPBERRY/LOGIN/EVALC.bin",'w')
		f2.write(base64.b64encode(self.ent_Passc.get()))
		f2.close()
		tkMessageBox.showinfo("Éxito","SE ALMACENO LA CLAVE DE CORREO",icon='info')
		self.ent_Passc.delete(first=0,last=50)

    def confdb(self):
        if(self.ent_NombreServidor.get() != "" and self.ent_NumeroPuerto.get() != "" and self.ent_Sid.get() != "" and self.ent_User.get() != "" and self.ent_Pass.get() != ""):
            try:
		url = self.ent_User.get()+"/"+self.ent_Pass.get()+"@"+self.ent_NombreServidor.get()+"/"+self.ent_Sid.get()
		con =  cx_Oracle.connect(url)
		cur = con.cursor()
		f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'w')
		f.write(base64.b64encode(self.ent_User.get()+"-"+self.ent_Pass.get()+"-"+self.ent_NombreServidor.get()+"-"+self.ent_Sid.get()+"-"+self.ent_NumeroPuerto.get()))
		f.close()
		f1 = open (os.getcwd()+"/RASPBERRY/CONFIGURACION_DB/conexiondb.uaz",'w')
		f1.write(base64.b64encode(self.ent_User.get()+"$-#"+self.ent_Pass.get()+"$-#"+self.ent_NombreServidor.get()+"$-#"+self.ent_Sid.get()+"$-#"+self.ent_NumeroPuerto.get()))
		f1.close()
		tkMessageBox.showinfo("Éxito","Todo Correcto Conexión DB. Versión"+con.version,icon='info')
		self.ent_NombreServidor.delete(first=0,last=50)
		self.ent_NumeroPuerto.delete(first=0,last=50)
		self.ent_Sid.delete(first=0,last=50)
		self.ent_User.delete(first=0,last=50)
		self.ent_Pass.delete(first=0,last=50)
		con.close()
            except:
                tkMessageBox.showerror("Error", "No se pudo configurar la db", icon="warning")
        else:
            tkMessageBox.showerror("Error","Falta un dato de la db", icon="warning")

