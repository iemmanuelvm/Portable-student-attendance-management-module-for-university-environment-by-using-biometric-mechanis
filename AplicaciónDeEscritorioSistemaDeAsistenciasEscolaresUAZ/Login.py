# -*- coding: utf-8 -*-
import Tkinter, tkMessageBox, os, base64, time, datetime, warnings
from Tkinter import *
import Tkinter as tk
import ttk, cx_Oracle
from ttk import *
import panel_control
import configurarconexion
import validacioncampos
import sys
warnings.filterwarnings("ignore")
time1 =''
fecha = datetime.datetime.now().date()
class Aplicacion(object):
    def __init__(self,master):
        self.master = master
	def reloj (*args):
		global time1
		time2 = time.strftime ('%H:%M:%S')
		if time2 != time1:
			time1 = time2
			self.clock.configure (text='Hora\n\n' +time2)
		self.clock.after(500,reloj)
        #Ventanas
	self.top = tk.Frame(master,height=150,bg='#05004e')
        self.top.pack(fill=X)
        self.boton = tk.Frame(master,height=500,bg='#ffedc6')
        self.boton.pack(fill=X)
        #Encabezado, imagen y fecha
        self.top_image = PhotoImage(file='icons/uaz.png')
        self.top_image_lbl = tk.Label(self.top,image=self.top_image,bg="#05004e")
        self.top_image_lbl.place(x=10,y=10)
        self.encabezado=tk.Label(self.top,text='INICIO DE SESIÓN - UAZ',font='arial 20 bold', fg='white', bg="#05004e")
        self.encabezado.place(x=200,y=60)
	#formulario
	self.lbl_asesion = tk.Label(self.boton, text='Nombre ó Correo Electrónico', font='arial 11 bold', fg='black', bg='#ffedc6')
        self.lbl_asesion.place(x=55, y=50)
        self.ent_sesion = tk.Entry(self.boton, width=20, bd=2, font='arial 16 bold')
        self.ent_sesion.place(x=30, y=100)
	#self.ent_sesion.insert(0,'ALDONSO')
	self.lbl_anombre = tk.Label(self.boton, text='Contraseña', font='arial 11 bold', fg='black', bg='#ffedc6')
        self.lbl_anombre.place(x=130, y=200)
        self.ent_clave = tk.Entry(self.boton, width=20, bd=2, font='arial 16 bold')
	self.ent_clave.config(show='*')
	#self.ent_clave.insert(0,'1111')
        self.ent_clave.place(x=30, y=250)
	self.lbl_fecha = tk.Label(self.boton, text='Fecha\n\n' +str(fecha), font='arial 15 bold', fg='black', bg='#ffedc6')
        self.lbl_fecha.place(x=450, y=50)
	self.clock = tk.Label(self.boton, font='arial 15 bold', fg='black', bg='#ffedc6')
	self.clock.pack()
	self.clock.place (x=460, y=200)
        self.btnIcon = PhotoImage(file='icons/view.png')
        self.login = tk.Button(self.boton,text='INICIAR SESIÓN',font='arial 12 bold',  justify='center')
        self.login.config(image=self.btnIcon, compound=LEFT,command=self.abrirEstudiantes)
        self.login.place(x=65,y=350)
        self.btnIcon1 = PhotoImage(file='icons/db.png')
        self.buttonCDB = tk.Button(self.boton,text='CONFIGURAR\nBASE DE DATOS',font='arial 12 bold',  justify='center')
        self.buttonCDB.config(image=self.btnIcon1, compound=LEFT,command=self.ConfigurarDB)
        self.buttonCDB.place(x=390,y=350)
	self.buttons = tk.Button(self.boton,text='Salir',font='arial 9 bold',  justify='center')
        self.buttons.config(compound=LEFT,command=self.SalirVentana)
        self.buttons.place(x=640,y=0)

	reloj(self)
    
    def SalirVentana(self):
	self.master.destroy()
	sys.exit()
    def ConfigurarDB(self):
	conf = configurarconexion.ConfigurarConexion()   
	
    def abrirEstudiantes(self):
	if(self.ent_sesion.get()!="" and self.ent_clave.get() ==""):
		try:
			url = self.ent_sesion.get()
			con =  cx_Oracle.connect(url)
			cur = con.cursor()
			tkMessageBox.showinfo("Éxito","ACCEDIENDO MODO ADMINISTRADOR:\n"+con.version, icon='info')
			con.close()
			self.master.destroy()
			panel = panel_control.Principal(True)
		except:
        		tkMessageBox.showerror("Error", "ERROR AL INGRESAR", icon="warning")
		self.master.destroy()
		

	if(self.ent_sesion.get()!="" and self.ent_clave.get()!=""):
		f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
		mensaje = f.read()
		f.close()
		url = base64.b64decode(mensaje)
		x = url.split('-')
		con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
		cur = con.cursor()
		docentes = cur.execute("SELECT DO_CLAVE, DO_NOMBRE, DO_APATERNO, DO_AMATERNO FROM DOCENTE WHERE (DO_EMAIL='"+self.ent_sesion.get()+"' OR DO_NOMBRE='"+self.ent_sesion.get()+"') AND DO_CLAVE = '"+self.ent_clave.get()+"'").fetchall()	
		if(len(docentes)==0):
			tkMessageBox.showerror("Error","DATOS ERRONEOS",icon='warning')
		else:
			if(docentes[0][3]!=None):
				mbox = tkMessageBox.askquestion("warning","ESTA INGRESANDO COMO: "+docentes[0][1] + " " + docentes[0][2]+" "+docentes[0][3],icon="warning")
				if mbox == 'yes':
					f = open (os.getcwd()+"/auxHuella/docente.uaz",'w')
					f.write(str(docentes[0][0] +"+"+ docentes[0][1] + " " + docentes[0][2]+" "+docentes[0][3]))
					f.close()
					self.master.destroy()
					panel = panel_control.Principal(False)
				else:
					self.ent_sesion.delete(first=0,last=50)
					self.ent_clave.delete(first=0,last=50)
			else:
				mbox = tkMessageBox.askquestion("warning","ESTA INGRESANDO COMO: "+docentes[0][1] + " " + docentes[0][2]+"?",icon="warning")
				if mbox == 'yes':
					f = open (os.getcwd()+"/auxHuella/docente.uaz",'w')
					f.write(str(docente_info[0][4] + " " + docente_info[0][2]))
					f.close()
					self.master.destroy()
					panel = panel_control.Principal(False)
				else:
					self.ent_sesion.delete(first=0,last=50)
					self.ent_clave.delete(first=0,last=50)
		cur.close()
		con.close()
		
	else:
		tkMessageBox.showerror("Error", "DATOS ERRONEOS", icon="warning")

def principal():
    root = Tk()
    app = Aplicacion(root)
    root.title("Sistema de Asistencia Biométrico - UAZ")
    root.geometry("700x600+600+200")
    root.resizable(False,False)
    root.mainloop()

if __name__ == '__main__':
    principal()
