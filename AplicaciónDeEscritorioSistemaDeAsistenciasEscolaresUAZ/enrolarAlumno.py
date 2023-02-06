# -*- coding: utf-8 -*-
import Tkinter, tkMessageBox
from Tkinter import *
import Tkinter as tk
import ttk, cx_Oracle, os, base64, datetime, time
from ttk import *
import validacioncampos

time1 =''
fecha = datetime.datetime.now().date()
test_list = []
test_list1 = []
idsCiclo = []
nameCiclo = []
idsGrupos = []
nameMateria = []
claveGrupo = []
idMatricula = []
idMatricula2 = []

class EnrolarAlumno(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

	def on_keyrelease(event):
		    # get text from entry
		    value = event.widget.get()
		    value = value.strip().lower()

		    # get data from test_list1
		    if value == '':
			data = test_list1
		    else:
			data = []
			for item in test_list1:
			    if value in item.lower():
				data.append(item)

		    # update data in listbox
		    listbox_update(data)

	def listbox_update(data):
		    # delete previous data
		    self.list_box1.delete(0, 'end')

		    # sorting data
		    data = sorted(data, key=str.lower)

		    # put new data
		    for item in data:
			self.list_box1.insert('end', item)

	def on_select1(event):
		    try:
			    global idMatricula2
			    x = str(event.widget.get(event.widget.curselection()))
			    idMatricula2 = x.split(' - ')
			    self.btnEliminar['state'] = 'normal'
			    self.btnAgregar['state'] = 'disabled'
			    #print(idMatricula2[0])
		    except:
			    pass

	def on_select2(event):
		    try:
			    # display element selected on list
			    global idMatricula
			    x = str(event.widget.get(event.widget.curselection()))
			    idMatricula = x.split(' - ')
			    self.btnEliminar['state'] = 'disabled'
			    self.btnAgregar['state'] = 'normal'
			    #print(idMatricula[0])
		    except:
			    pass
		    
		    

	def comb1_selected(*args):
		    self.btnAgregar['state'] = 'disabled'
		    self.btnEliminar['state'] = 'disabled'
		    self.list_box.delete(0,END)
		    f = open (os.getcwd()+'/auxHuella/docente.uaz','r')
		    mensaje = f.read()
		    x1 = mensaje.split('+')
		    f.close()

		    #self.btnAgregar.config(state = DISABLED)

		    if (self.combo_grupos.current() != -1 ):
			f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
			mensaje = f.read()
			f.close()
			url = base64.b64decode(mensaje)
			x = url.split('-')

			del idsGrupos[:]
			del nameMateria[:]

			con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
			cur = con.cursor()

			docentes = cur.execute("SELECT PA.MT_CLAVE, PA.MT_NOMBRE, ME.DO_APATERNO, ME.DO_AMATERNO, ME.DO_NOMBRE, RE.GR_CLAVE, RE.GR_GRUPO FROM MATERIA PA JOIN GRUPO RE ON PA.MT_CLAVE = RE.MT_CLAVE JOIN DOCENTE ME ON ME.DO_CLAVE = RE.DO_CLAVE WHERE ME.DO_CLAVE = :1 AND RE.CE_CLAVE = :2",(str(x1[0]), str(idsCiclo[int(self.combo_grupos.current())]))).fetchall()

			for alumno in docentes:
				claveGrupo.append(str(alumno[5]))
				idsGrupos.append(str(alumno[0]))
				nameMateria.append(str(alumno[1])+' - '+str(alumno[6]))

			s = docentes
			 
			if str(s) != '[]':
				
				self.combo_ciclo.set(" ")
				self.combo_grupos['values']=nameCiclo
				self.combo_grupos.config(state='readonly')
				self.combo_grupos.current(0)
				self.combo_ciclo['values']=nameMateria
				self.combo_ciclo.config(state='readonly')
				
				
			else:	
				self.ent_TOL['state'] = 'normal'
				self.ent_SES['state'] = 'normal'
				self.ent_TOL.delete(first=0,last=50)
				self.ent_SES.delete(first=0,last=50)
				self.ent_TOL['state'] = 'disabled'
				self.ent_SES['state'] = 'disabled'
				self.list_box.configure(state = DISABLED)
				self.list_box1.configure(state = DISABLED)
				self.btnASES['state'] = 'disabled'
				self.btnAH['state'] = 'disabled'
				self.combo_ciclo.set(" ")
				s = []
				s.append(str(' '))
				self.combo_ciclo['values']=s
				self.combo_ciclo.config(state='readonly')
				self.combo_grupos['values']=nameCiclo
				self.combo_grupos.config(state='readonly')
				

			cur.close()
			con.close()

	def comb2_selected(*args):
	    	    self.btnAgregar['state'] = 'normal'
		    self.btnEliminar['state'] = 'disabled'
		    v = self.combo_ciclo.get()
		    if str(v) == ' ':
			self.btnAgregar['state'] = 'disabled'
		        self.btnEliminar['state'] = 'disabled'
			
		    else:
			self.ent_TOL['state'] = 'normal'
			self.ent_SES['state'] = 'normal'
			self.ent_SRET['state'] = 'normal'
			try:
				del test_list[:]
				
				# archivo-entrada.py
				f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
				mensaje = f.read()
				f.close()
				url = base64.b64decode(mensaje)
				x = url.split('-')
				con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
				cur = con.cursor()

				#print 'ando aqui 1 -' + str(idsCiclo[int(self.combo_grupos.current())])
				#print 'ando aqui 2 -' + str(claveGrupo[int(self.combo_ciclo.current())])

				alumnos = cur.execute("SELECT AL.AL_MATRICULA, AL.AL_NOMBRE, AL.AL_APATERNO, AL.AL_AMATERNO FROM ALUMNO AL JOIN ASIGNATURA ASI ON AL.AL_MATRICULA = ASI.AL_MATRICULA WHERE ASI.CE_CLAVE = :1 AND GR_CLAVE = :2 ORDER BY AL.AL_APATERNO",(str(idsCiclo[int(self.combo_grupos.current())]), str(claveGrupo[int(self.combo_ciclo.current())]))).fetchall()

				
				self.list_box.configure(state = NORMAL)
				self.list_box1.configure(state = NORMAL)
				count=0
				self.list_box.delete(0,END)

				for alumno in alumnos:
					if(str(alumno[3])!='None'):
						self.list_box.insert(count,str(alumno[0])+" - "+alumno[1]+" "+alumno[2]+" "+alumno[3])
						count += 1
						test_list.append((str(alumno[0])+" - "+alumno[1]+" "+alumno[2]+" "+alumno[3]))
					else:
						self.list_box.insert(count,str(alumno[0])+" - "+alumno[1]+" "+alumno[2])
						count += 1
						test_list.append((str(alumno[0])+" - "+alumno[1]+" "+alumno[2]))
				self.list_box.bind('<<ListboxSelect>>', on_select1)

				f = open (os.getcwd()+'/auxHuella/docente.uaz','r')
				mensaje = f.read()
				x = mensaje.split('+')
				f.close()

				tolerancia = cur.execute("SELECT GH.GH_RETARDO_TIEMPO, GR.GR_TOTAL_SESIONES, GH.GH_TOTAL_RETARDO_ASISTENCIA FROM GRUPO_HORARIO GH JOIN  GRUPO GR ON GH.GR_CLAVE = GR.GR_CLAVE WHERE GR.CE_CLAVE = :1 AND GR.DO_CLAVE = :2 AND GR.GR_CLAVE = :3",(str(idsCiclo[int(self.combo_grupos.current())]), x[0], str(claveGrupo[int(self.combo_ciclo.current())]))).fetchall()

				if tolerancia[0][0] != None:
					self.ent_TOL.delete(0,END)
					self.ent_TOL.insert(0, str(tolerancia[0][0]))
				else:
					self.ent_TOL.delete(0,END)
					self.ent_TOL.insert(0, '')

				if tolerancia[0][1] != None:
					self.ent_SES.delete(0,END)
					self.ent_SES.insert(0, str(tolerancia[0][1]))
				else:
					self.ent_SES.delete(0,END)
					self.ent_SES.insert(0, '')
				
				if tolerancia[0][2] != None:
					self.ent_SRET.delete(0,END)
					self.ent_SRET.insert(0, str(tolerancia[0][2]))
				else:
					self.ent_SRET.delete(0,END)
					self.ent_SRET.insert(0, '')
				
				self.ent_TOL['state'] = 'disabled'
				self.btnAH['state'] = 'normal'
				self.btnMH['state'] = 'disabled'

				self.ent_SES['state'] = 'disabled'
				self.btnMSES['state'] = 'disabled'
				self.btnASES['state'] = 'normal'
	
				self.ent_SRET['state'] = 'disabled'
				self.btnMSRET['state'] = 'disabled'
				self.btnHSRET['state'] = 'normal'

				cur.close()
				con.close()
				self.list_box1.configure(state = NORMAL)
				self.list_box.configure(state = NORMAL)
			except:
                		tkMessageBox.showerror("Error","Fallo la conexion de DB!!!",icon='warning')

				
		    		

				
		    	

	del claveGrupo[:]
        self.geometry("1700x800+220+100")
        self.title("Enrolar Alumno En Clase")
        self.resizable(False,False)

        # Ventanas
        self.top = tk.Frame(self, height=150, bg='#05004e')
        self.top.pack(fill=X)
        self.botonFrame = tk.Frame(self, height=900, bg='#ffedc6')
        self.botonFrame.pack(fill=X)

        # Encabezado, imagen y fecha
        self.top_image = tk.PhotoImage(file='icons/uaz.png')
        self.top_image_lbl = tk.Label(self.top, image=self.top_image, bg="#05004e")
        self.top_image_lbl.place(x=10, y=10)
        self.encabezado = tk.Label(self.top, text='ASIGNACIÓN DE ALUMNOS A GRUPOS DE CLASE', font='arial 26 bold', fg='white', bg="#05004e")
        self.encabezado.place(x=320, y=20)
	f = open (os.getcwd()+'/auxHuella/docente.uaz','r')
	mensaje = f.read()
	x = mensaje.split('+')
	f.close()
	self.encDocente = tk.Label(self.top, text='DOCENTE: '+x[1], font='arial 12 bold', fg='white', bg="#05004e")
        self.encDocente.place(x=150, y=110)
	

        #Etiquetas y entradas
        #NombreServidor
        self.lbl_Sid = tk.Label(self.botonFrame, text = 'Buscar:', font = 'arial 15 bold', fg = 'black', bg = '#ffedc6')
        self.lbl_Sid.place(x=40, y=40)

	self.ent_NombreServidor = tk.Entry(self.botonFrame,width=25,bd=2)
        self.ent_NombreServidor.place(x=160, y=45)

	self.ent_NombreServidor.bind('<KeyRelease>', on_keyrelease)

	self.lbl_ciclo = tk.Label(self.botonFrame, text = 'Ciclo escolar:', font = 'arial 15 bold', fg = 'black', bg = '#ffedc6')
        self.lbl_ciclo.place(x=460, y=40)

	try:
		del nameCiclo[:]
		f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
		mensaje = f.read()
		f.close()
		url = base64.b64decode(mensaje)
		x = url.split('-')
		#print x
		con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
		cur = con.cursor()
		ciclos = cur.execute("SELECT * FROM CICLO_ESCOLAR").fetchall()
		for ciclo in ciclos:
			idsCiclo.append(str(ciclo[0]))
			nameCiclo.append(str(ciclo[5]))

		cur.close()
		con.close()
	except:
                tkMessageBox.showerror("Error","No hay conexion a la base de datos!!!",icon='warning')

	self.mes1 = StringVar()
	self.mes2 = StringVar()
	self.combo_grupos = ttk.Combobox(self.botonFrame, width=15, textvariable=self.mes1, values=(nameCiclo), state = 'readonly')
        self.combo_grupos.place(x=640, y=45)
	self.combo_grupos.bind("<<ComboboxSelected>>", comb1_selected)

	self.lbl_ciclo = tk.Label(self.botonFrame, text = 'Grupos:', font = 'arial 15 bold', fg = 'black', bg = '#ffedc6')
        self.lbl_ciclo.place(x=850, y=40)
	self.combo_ciclo = ttk.Combobox(self.botonFrame,width=60,textvariable=self.mes2, values=(nameMateria), state = 'readonly')
        self.combo_ciclo.place(x=970, y=45)
	self.combo_ciclo.config(state=DISABLED)
	self.combo_ciclo.bind("<<ComboboxSelected>>", comb2_selected)

        #LISTADO ALUMNOS
	self.list_box1 = tk.Listbox(self.botonFrame,width=50,height=23,bd=1,font="times 12 bold")
        self.sb1 = tk.Scrollbar(self.botonFrame,orient=VERTICAL)
        self.list_box1.place(x=800, y=200)
        self.sb1.config(command=self.list_box1.yview)
        self.list_box1.config(yscrollcommand=self.sb1.set)
        self.list_box1.place(x=40, y=100)

	try:
		del test_list1[:]
		# archivo-entrada.py
		f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
		mensaje = f.read()
		f.close()
		url = base64.b64decode(mensaje)
		x = url.split('-')
		con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
		cur = con.cursor()

		alumnos = cur.execute("SELECT AL_MATRICULA, AL_NOMBRE, AL_APATERNO, AL_AMATERNO FROM ALUMNO ORDER BY AL_APATERNO").fetchall()

		count=0
		self.list_box1.delete(0,END)

		for alumno in alumnos:
			if(str(alumno[3])!='None'):
				self.list_box1.insert(count,str(alumno[0])+" - "+alumno[1]+" "+alumno[2]+" "+alumno[3])
				count += 1
				test_list1.append((str(alumno[0])+" - "+alumno[1]+" "+alumno[2]+" "+alumno[3]))
			else:
				self.list_box1.insert(count,str(alumno[0])+" - "+alumno[1]+" "+alumno[2])
				count += 1
				test_list1.append((str(alumno[0])+" - "+alumno[1]+" "+alumno[2]))
		self.list_box1.bind('<<ListboxSelect>>', on_select2)
		cur.close()
		con.close()
	except:
		tkMessageBox.showerror("Error","Fallo la conexion de DB!!!",icon='warning')

	self.list_box1.configure(state = DISABLED)

	#LISTADO CON ALUMNO EN EL GRUPO
	self.list_box = tk.Listbox(self.botonFrame,width=50,height=23,bd=1,font="times 12 bold")
        self.sb = tk.Scrollbar(self.botonFrame,orient=VERTICAL)
        self.list_box.place(x=550, y=200)
        self.sb.config(command=self.list_box.yview)
        self.list_box.config(yscrollcommand=self.sb.set)
        self.list_box.place(x=735, y=100)
	self.list_box.configure(state = DISABLED)

	self.btnAgregar = tk.Button(self.botonFrame,text="AGREGAR >>",font='fixedsys 15 bold', foreground="#000000", background="#fcf9ea", command=self.EnrolarAlumno)
        self.btnAgregar.place(x=550, y=300)
	self.btnAgregar['state'] = 'disabled'

	self.btnEliminar = tk.Button(self.botonFrame,text="< ELIMINAR",font='fixedsys 15 bold', foreground="#000000", background="#fcf9ea", command=self.EliminarGrupo)
        self.btnEliminar.place(x=550, y=450)
	self.btnEliminar['state'] = 'disabled'

	self.ent_TOL = tk.Entry(self.botonFrame,width=10,bd=2,font='fixedsys 17 bold')
        self.ent_TOL.place(x=1275, y=100)
	self.ent_TOL['state'] = 'disabled'

	self.btnMH = tk.Button(self.botonFrame,text=" MODIFICAR\nRETARDO ",font='fixedsys 15 bold', foreground="#000000", background="#fcf9ea", command=self.ActulizaRetardo)
        self.btnMH.place(x=1275, y=160)
	self.btnMH['state'] = 'disabled'

	self.btnAH = tk.Button(self.botonFrame,text=" HABILITAR\nRETARDO ",font='fixedsys 15 bold', foreground="#000000", background="#fcf9ea", command=self.HabilitaRetardo)
        self.btnAH.place(x=1275, y=250)
	self.btnAH['state'] = 'disabled'

	self.ent_SRET = tk.Entry(self.botonFrame,width=10,bd=2,font='fixedsys 17 bold')
        self.ent_SRET.place(x=1500, y=100)
	self.ent_SRET['state'] = 'disabled'

	self.btnMSRET = tk.Button(self.botonFrame,text=" MODIFICAR\nFALTA POR\nRETARDOS",font='fixedsys 15 bold', foreground="#000000", background="#fcf9ea", command=self.ActulizaSesionesRetardo)
        self.btnMSRET.place(x=1500, y=160)
	self.btnMSRET['state'] = 'disabled'

	self.btnHSRET = tk.Button(self.botonFrame,text=" HABILITAR\nFALTA POR\nRETARDOS",font='fixedsys 15 bold', foreground="#000000", background="#fcf9ea", command=self.HabilitaSesionesRetardo)
        self.btnHSRET.place(x=1500, y=280)
	self.btnHSRET['state'] = 'disabled'


	self.ent_SES = tk.Entry(self.botonFrame,width=10,bd=2,font='fixedsys 17 bold')
        self.ent_SES.place(x=1275, y=350)
	self.ent_SES['state'] = 'disabled'

	self.btnMSES = tk.Button(self.botonFrame,text=" MODIFICAR\nSESIÓN ",font='fixedsys 15 bold', foreground="#000000", background="#fcf9ea", command=self.ActulizarSesiones)
        self.btnMSES.place(x=1275, y=410)
	self.btnMSES['state'] = 'disabled'

	self.btnASES = tk.Button(self.botonFrame,text=" HABILITAR\nSESIÓN",font='fixedsys 15 bold', foreground="#000000", background="#fcf9ea", command=self.HabilitaSesiones)
        self.btnASES.place(x=1275, y=510)
	self.btnASES['state'] = 'disabled'

	self.btnSalir = tk.Button(self.botonFrame,text="SALIR",font='fixedsys 12 bold', foreground="#000000", background="#fcf9ea", command=self.SalirVentana)
        self.btnSalir.place(x=1275, y=610)

    def ActulizaSesionesRetardo(self):
	if(self.ent_SRET.get()!="" and validacioncampos.Entero(self.ent_SRET.get())):
		try:
			f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
			mensaje = f.read()
			f.close()
			url = base64.b64decode(mensaje)
			x = url.split('-')
			con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
			cur = con.cursor()

			ce = cur.execute("SELECT CE_CLAVE FROM CICLO_ESCOLAR WHERE CE_DESC_CORTA = '"+str(self.combo_grupos.get())+"'").fetchall()
			
			if(len(ce)>0):
				f = open (os.getcwd()+'/auxHuella/docente.uaz','r')
				mensaje = f.read()
				x = mensaje.split('+')
				f.close()
				gr = str(claveGrupo[int(self.combo_ciclo.current())])
				
				try:
					
					cur.execute("UPDATE GRUPO_HORARIO SET GH_TOTAL_RETARDO_ASISTENCIA = '"+self.ent_SRET.get()+"' WHERE CE_CLAVE = '"+ce[0][0]+"' AND GR_CLAVE = '"+gr[0][0]+"'")
					f = open (os.getcwd()+'/auxHuella/docente.uaz','r')
					mensaje = f.read()
					x = mensaje.split('+')
					f.close()

					tolerancia = cur.execute("SELECT GH.GH_TOTAL_RETARDO_ASISTENCIA FROM GRUPO_HORARIO GH JOIN  GRUPO GR ON GH.GR_CLAVE = GR.GR_CLAVE WHERE GR.CE_CLAVE = :1 AND GR.DO_CLAVE = :2 AND GR.GR_CLAVE = :3",(str(idsCiclo[int(self.combo_grupos.current())]), x[0], str(claveGrupo[int(self.combo_ciclo.current())]))).fetchall()
					#print(tolerancia)
					self.ent_SRET.delete(0,END)
					self.ent_SRET.insert(0, str(tolerancia[0][0]))
					self.ent_SRET['state'] = 'disabled'
					self.btnAH['state'] = 'normal'
					self.btnMH['state'] = 'disabled'
				except:
					tkMessageBox.showerror("Error","NO SE ACTUALIZO EL RETARDO",icon='warning')
			
				
				
				cur.close()
				con.commit()
				con.close()
			
		except:
			tkMessageBox.showerror("Error","ERROR DE BASE DE DATOS",icon='warning')
	else:
		tkMessageBox.showerror("Error","ERROR CAMPO VACIO O DATO ERRONEO",icon='warning')

    def ActulizaRetardo(self):
	#print(self.ent_TOL.get())
	if(self.ent_TOL.get()!="" and validacioncampos.Entero(self.ent_TOL.get())):
		try:
			f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
			mensaje = f.read()
			f.close()
			url = base64.b64decode(mensaje)
			x = url.split('-')
			con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
			cur = con.cursor()

			ce = cur.execute("SELECT CE_CLAVE FROM CICLO_ESCOLAR WHERE CE_DESC_CORTA = '"+str(self.combo_grupos.get())+"'").fetchall()
			
			if(len(ce)>0):
				f = open (os.getcwd()+'/auxHuella/docente.uaz','r')
				mensaje = f.read()
				x = mensaje.split('+')
				f.close()
				gr = str(claveGrupo[int(self.combo_ciclo.current())])
				try:
					cur.execute("UPDATE GRUPO_HORARIO SET GH_RETARDO_TIEMPO = '"+self.ent_TOL.get()+"' WHERE CE_CLAVE = '"+ce[0][0]+"' AND GR_CLAVE = '"+gr[0][0]+"'")
					f = open (os.getcwd()+'/auxHuella/docente.uaz','r')
					mensaje = f.read()
					x = mensaje.split('+')
					f.close()

					tolerancia = cur.execute("SELECT GH.GH_RETARDO_TIEMPO FROM GRUPO_HORARIO GH JOIN  GRUPO GR ON GH.GR_CLAVE = GR.GR_CLAVE WHERE GR.CE_CLAVE = :1 AND GR.DO_CLAVE = :2 AND GR.GR_CLAVE = :3",(str(idsCiclo[int(self.combo_grupos.current())]), x[0], str(claveGrupo[int(self.combo_ciclo.current())]))).fetchall()
					#print(tolerancia)
					self.ent_TOL.delete(0,END)
					self.ent_TOL.insert(0, str(tolerancia[0][0]))
					self.ent_TOL['state'] = 'disabled'
					self.btnAH['state'] = 'normal'
					self.btnMH['state'] = 'disabled'
				except:
					tkMessageBox.showerror("Error","NO SE ACTUALIZO EL RETARDO",icon='warning')
			
				
				
				cur.close()
				con.commit()
				con.close()
			
		except:
			tkMessageBox.showerror("Error","ERROR DE BASE DE DATOS",icon='warning')
	else:
		tkMessageBox.showerror("Error","ERROR CAMPO VACIO O DATO ERRONEO",icon='warning')

    def ActulizarSesiones(self):
	#print(self.ent_SES.get())
	if(self.ent_SES.get()!="" and validacioncampos.Entero(self.ent_SES.get())):
		try:
			f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
			mensaje = f.read()
			f.close()
			url = base64.b64decode(mensaje)
			x = url.split('-')
			con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
			cur = con.cursor()

			ce = cur.execute("SELECT CE_CLAVE FROM CICLO_ESCOLAR WHERE CE_DESC_CORTA = '"+str(self.combo_grupos.get())+"'").fetchall()
			
			if(len(ce)>0):
				f = open (os.getcwd()+'/auxHuella/docente.uaz','r')
				mensaje = f.read()
				x = mensaje.split('+')
				f.close()
				gr = str(claveGrupo[int(self.combo_ciclo.current())])
				try:
					cur.execute("UPDATE GRUPO SET GR_TOTAL_SESIONES = '"+self.ent_SES.get()+"' WHERE CE_CLAVE = '"+ce[0][0]+"' AND GR_CLAVE = '"+gr[0][0]+"'")
					f = open (os.getcwd()+'/auxHuella/docente.uaz','r')
					mensaje = f.read()
					x = mensaje.split('+')
					f.close()

					SESIONES = cur.execute("SELECT GR.GR_TOTAL_SESIONES FROM GRUPO_HORARIO GH JOIN  GRUPO GR ON GH.GR_CLAVE = GR.GR_CLAVE WHERE GR.CE_CLAVE = :1 AND GR.DO_CLAVE = :2 AND GR.GR_CLAVE = :3",(str(idsCiclo[int(self.combo_grupos.current())]), x[0], str(claveGrupo[int(self.combo_ciclo.current())]))).fetchall()
					
					self.ent_SES.delete(0,END)
					self.ent_SES.insert(0, str(SESIONES[0][0]))
					self.ent_SES['state'] = 'disabled'
					self.btnASES['state'] = 'normal'
					self.btnMSES['state'] = 'disabled'
				except:
					tkMessageBox.showerror("Error","NO SE ACTUALIZO EL NO. DE SESIONES",icon='warning')
			
				
				
				cur.close()
				con.commit()
				con.close()
			
		except:
			tkMessageBox.showerror("Error","ERROR DE BASE DE DATOS",icon='warning')
	else:
		tkMessageBox.showerror("Error","ERROR CAMPO VACIO O DATO ERRONEO",icon='warning')


    def HabilitaRetardo(self):
	self.ent_TOL['state'] = 'normal'
	self.btnMH['state'] = 'normal'
	self.btnAH['state'] = 'disabled'

    def HabilitaSesiones(self):
	self.ent_SES['state'] = 'normal'
	self.btnMSES['state'] = 'normal'
	self.btnASES['state'] = 'disabled'

    def HabilitaSesionesRetardo(self):
	self.ent_SRET['state'] = 'normal'
	self.btnMSRET['state'] = 'normal'
	self.btnHSRET['state'] = 'disabled'
	
    def SalirVentana(self):
	self.top.destroy()
        self.botonFrame.destroy()
	self.destroy()

    def EliminarGrupo(self):
	global idMatricula2
	#print("----"+self.combo_ciclo.get()+"---")
	#print(self.combo_grupos.get())
	#print idMatricula2
	if len(idMatricula2)>0:
		mbox = tkMessageBox.askquestion("warning","Desea eliminar al estudiante con matrícula "+idMatricula2[0],icon="warning")
		if mbox == 'yes':
			try:
				f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
				mensaje = f.read()
				f.close()
				url = base64.b64decode(mensaje)
				x = url.split('-')
				con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
				cur = con.cursor()

				ce = cur.execute("SELECT CE_CLAVE FROM CICLO_ESCOLAR WHERE CE_DESC_CORTA = '"+str(self.combo_grupos.get())+"'").fetchall()
				
				if(len(ce)>0 and len(idMatricula2)>0):
					f = open (os.getcwd()+'/auxHuella/docente.uaz','r')
					mensaje = f.read()
					x = mensaje.split('+')
					f.close()

					gr = str(claveGrupo[int(self.combo_ciclo.current())])

					try:
						cur.execute("DELETE FROM ASISTENCIA WHERE  AL_MATRICULA='"+str(idMatricula2[0])+"' AND GR_CLAVE = '"+str(gr)+"' AND CE_CLAVE='"+str(ce[0][0])+"'")
						cur.execute("DELETE FROM ASIGNATURA WHERE  AL_MATRICULA='"+str(idMatricula2[0])+"' AND GR_CLAVE = '"+str(gr)+"' AND CE_CLAVE='"+str(ce[0][0])+"'")
					except:
						tkMessageBox.showerror("Error","NO SE ELIMINO EL ALUMNO DEL GRUPO",icon='warning')
				
					del test_list[:]
				
					alumnos = cur.execute("SELECT AL.AL_MATRICULA, AL.AL_NOMBRE, AL.AL_APATERNO, AL.AL_AMATERNO FROM ALUMNO AL JOIN ASIGNATURA ASI ON AL.AL_MATRICULA = ASI.AL_MATRICULA WHERE ASI.CE_CLAVE = :1 AND GR_CLAVE = :2 ORDER BY AL.AL_APATERNO",(str(idsCiclo[int(self.combo_grupos.current())]), str(claveGrupo[int(self.combo_ciclo.current())]))).fetchall()

					count=0
					self.list_box.delete(0,END)

					for alumno in alumnos:
						if(str(alumno[3])!='None'):
							self.list_box.insert(count,str(alumno[0])+" - "+alumno[1]+" "+alumno[2]+" "+alumno[3])
							count += 1
							test_list.append((str(alumno[0])+" - "+alumno[1]+" "+alumno[2]+" "+alumno[3]))
						else:
							self.list_box.insert(count,str(alumno[0])+" - "+alumno[1]+" "+alumno[2])
							count += 1
							test_list.append((str(alumno[0])+" - "+alumno[1]+" "+alumno[2]))
					
					cur.close()
					con.commit()
					con.close()
					idMatricula2 = []
				
			except:
				tkMessageBox.showerror("Error","ERROR DE BASE DE DATOS",icon='warning')

    def EnrolarAlumno(self):
	global idMatricula
	try:
		f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
		mensaje = f.read()
		f.close()
		url = base64.b64decode(mensaje)
		x = url.split('-')
		con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
		cur = con.cursor()

		ce = cur.execute("SELECT CE_CLAVE FROM CICLO_ESCOLAR WHERE CE_DESC_CORTA = '"+str(self.combo_grupos.get())+"'").fetchall()
		#print(str(ce[0][0]))
		if(len(ce)>0 and len(idMatricula)>0):
			f = open (os.getcwd()+'/auxHuella/docente.uaz','r')
			mensaje = f.read()
			x = mensaje.split('+')
			f.close()

			gr = str(claveGrupo[int(self.combo_ciclo.current())])
			try:
				cur.execute("INSERT INTO ASIGNATURA(AL_MATRICULA,CE_CLAVE,GR_CLAVE,AS_STATUS,AS_FECHA_REGISTRO) VALUES('"+str(idMatricula[0])+"','"+str(ce[0][0])+"','"+str(gr)+"',1,to_date('" + str(datetime.datetime.now().replace(microsecond=0)) + "','yyyy-mm-dd hh24:mi:ss'))")
			except:
				tkMessageBox.showerror("Error","EL ALUMNO YA SE ENCUENTRA INSCRITO",icon='warning')
			del test_list[:]
		
			alumnos = cur.execute("SELECT AL.AL_MATRICULA, AL.AL_NOMBRE, AL.AL_APATERNO, AL.AL_AMATERNO FROM ALUMNO AL JOIN ASIGNATURA ASI ON AL.AL_MATRICULA = ASI.AL_MATRICULA WHERE ASI.CE_CLAVE = :1 AND GR_CLAVE = :2 ORDER BY AL.AL_APATERNO",(str(idsCiclo[int(self.combo_grupos.current())]), str(claveGrupo[int(self.combo_ciclo.current())]))).fetchall()

			count=0
			self.list_box.delete(0,END)

			for alumno in alumnos:
				if(str(alumno[3])!='None'):
					self.list_box.insert(count,str(alumno[0])+" - "+alumno[1]+" "+alumno[2]+" "+alumno[3])
					count += 1
					test_list.append((str(alumno[0])+" - "+alumno[1]+" "+alumno[2]+" "+alumno[3]))
				else:
					self.list_box.insert(count,str(alumno[0])+" - "+alumno[1]+" "+alumno[2])
					count += 1
					test_list.append((str(alumno[0])+" - "+alumno[1]+" "+alumno[2]))
			
			cur.close()
			con.commit()
			con.close()
			idMatricula = []

	except:
		tkMessageBox.showerror("Error","ERROR DE BASE DE DATOS",icon='warning')

	
