# -*- coding: utf-8 -*-
import Tkinter, tkMessageBox, os, base64, pyfprint, time
from Tkinter import *
import Tkinter as tk
import ttk, cx_Oracle
from ttk import *
import datetime, commands
from os import remove
import validacioncampos, reportestable, enrolarAlumno
import agregarestudiante
import agregardocente
import configurarconexion
import info
import Tkconstants, Login
import removeSilence
import sys
from ModeladoGMM import ModelarGMM


fecha = datetime.datetime.now().date()
test_list = []
test_listD = []
idsCiclo = []
nameCiclo = []
idsGrupos = []
nameMateria = []
claveGrupo = []
auxGR = 0
idgescolar = []

class Main(object):
    def __init__(self,master,admin):
        self.master = master
	self.ADMIN = admin
	def tabIndex(evt):
		if str(self.tabs.index(self.tabs.select())) == "0":
			displayAlumnos(self)
        		self.ent_search.bind('<KeyRelease>', on_keyrelease)
		if str(self.tabs.index(self.tabs.select())) == "1":
			displayDocentes(self)
        		self.ent_search.bind('<KeyRelease>', on_keyreleaseD)

        def displayDocentes(self):
		del test_listD[:]
		try:
			f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
			mensaje = f.read()
			f.close()
			url = base64.b64decode(mensaje)
			x = url.split('-')
			con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
			cur = con.cursor()
			DOcentes = cur.execute("SELECT * FROM DOCENTE ORDER BY DO_APATERNO").fetchall()
			count=0
			self.list_detailsD.delete(0,END)
			for docente in DOcentes:
				if(str(docente[3])!='None'):
	        			self.list_boxD.insert(count,str(docente[0])+" - "+docente[4]+" "+docente[2]+" "+docente[3])
	        			count += 1
					test_listD.append((str(docente[0])+" - "+docente[4]+" "+docente[2]+" "+docente[3]))
				else:
					self.list_boxD.insert(count,str(docente[0])+" - "+docente[4]+" "+docente[2])
	        			count += 1
					test_listD.append((str(docente[0])+" - "+docente[4]+" "+docente[2]))
			self.list_boxD.bind('<<ListboxSelect>>', on_select)
			listbox_updateD(test_listD)

			def DocenteInfo(evt):
				try:
		        		value = str(self.list_boxD.get(self.list_boxD.curselection()))
		        		id = value.split('-')[0]
		        		docente = cur.execute("SELECT * FROM DOCENTE WHERE DO_CLAVE = :1",(int(id),))
		        		docente_info = docente.fetchall()
		        		self.list_detailsD.delete(0, END)
					self.list_detailsD.insert(1, "                                              DETALLES                                              ")
		        		self.list_detailsD.insert(3, "Clave Docente: " + docente_info[0][0])
		        		self.list_detailsD.insert(4, "Apellido Paterno : " + docente_info[0][2])
					if(str(docente_info[0][3])!="None"):
						self.list_detailsD.insert(5, "Apellido Materno : " + docente_info[0][3])
					else:
						self.list_detailsD.insert(5, "Apellido Materno : ")
		        		self.list_detailsD.insert(6, "Nombre (s) : " + docente_info[0][4])
					if(str(docente_info[0][11])!="None"):
						self.list_detailsD.insert(7, "Email : " + docente_info[0][11])
					else:
						self.list_detailsD.insert(7, "Email : ")
					if(docente_info[0][12]==2):
						self.list_detailsD.insert(8, "Género : " + "FEMENINO")
					else:
						self.list_detailsD.insert(8, "Género : " + "MASCULINO")
				except:
					pass

				
			def doubleClick(evt):
                		global  given_idD
                		value=str(self.list_boxD.get(self.list_boxD.curselection()))
                		given_idD=value.split('-')[0]
                		deleteD=UpdateDocente()

            		self.list_boxD.bind('<<ListboxSelect>>',DocenteInfo)
            		
            		#self.tabs.bind('<ButtonRelease-1>',displayBooks)
            		self.list_boxD.bind('<Double-Button-1>',doubleClick)

            	except:
                	tkMessageBox.showerror("Error","No CONEXION a la base de datos!!!",icon='warning')
	
	def displayAlumnos(self):
		
		del test_list[:]
		try:
			f1 = open (os.getcwd()+'/auxHuella/docente.uaz','r')
			mensaje = f1.read()
			x1 = mensaje.split('+')
			f1.close()
			f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
			mensaje = f.read()
			f.close()
			url = base64.b64decode(mensaje)
			x = url.split('-')
			con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
			cur = con.cursor()
			#SELECT DISTINCT AL.AL_MATRICULA, AL.AL_NOMBRE, AL.AL_APATERNO, AL.AL_AMATERNO FROM ALUMNO AL JOIN ASIGNATURA ASI ON AL.AL_MATRICULA = ASI.AL_MATRICULA JOIN GRUPO GR ON GR.GR_CLAVE = ASI.GR_CLAVE AND GR.DO_CLAVE = '"++"'
			alumnos = cur.execute("SELECT DISTINCT AL.AL_MATRICULA, AL.AL_NOMBRE, AL.AL_APATERNO, AL.AL_AMATERNO FROM ALUMNO AL JOIN ASIGNATURA ASI ON AL.AL_MATRICULA = ASI.AL_MATRICULA JOIN GRUPO GR ON GR.GR_CLAVE = ASI.GR_CLAVE AND GR.DO_CLAVE = '"+x1[0]+"' ORDER BY AL.AL_APATERNO").fetchall()
			count=0
			self.list_box.delete(0,END)
			for alumno in alumnos:
				if(alumno[3]!=None):
	        			self.list_box.insert(count,str(alumno[0])+" - "+alumno[1]+" "+alumno[2]+" "+alumno[3])
	        			count += 1
					test_list.append((str(alumno[0])+" - "+alumno[1]+" "+alumno[2]+" "+alumno[3]))
				else:
					self.list_box.insert(count,str(alumno[0])+" - "+alumno[1]+" "+alumno[2])
	        			count += 1
					test_list.append((str(alumno[0])+" - "+alumno[1]+" "+alumno[2]))
			self.list_box.bind('<<ListboxSelect>>', on_select)
			listbox_update(test_list)

			def AlumnoInfo(evt):
				try:
		        		value = str(self.list_box.get(self.list_box.curselection()))
		        		id = value.split('-')[0]
		        		alumno = cur.execute("SELECT * FROM ALUMNO WHERE AL_MATRICULA = :1",(int(id),))
		        		alumno_info = alumno.fetchall()
		        		self.list_details.delete(0, END)
					self.list_details.insert(1, "                                              DETALLES                                              ")
		        		self.list_details.insert(3, "Matricula: " + alumno_info[0][0])
		        		self.list_details.insert(4, "Apellido Paterno : " + alumno_info[0][1])
					if(str(alumno_info[0][2])!="None"):
						self.list_details.insert(5, "Apellido Materno : " + alumno_info[0][2])
					else:
						self.list_details.insert(5, "Apellido Materno : ")
		        		self.list_details.insert(6, "Nombre (s) : " + alumno_info[0][3])
					if(str(alumno_info[0][9])!="None"):
						self.list_details.insert(7, "Email : " + alumno_info[0][9])
					else:
						self.list_details.insert(7, "Email : ")
					if(alumno_info[0][10]==2):
						self.list_details.insert(8, "Género : " + "FEMENINO")
					else:
						self.list_details.insert(8, "Género : " + "MASCULINO")
				except:
					pass

				
			def doubleClick(evt):
                		global  given_id
                		value=str(self.list_box.get(self.list_box.curselection()))
                		given_id=value.split('-')[0]
                		deletealumno=UpdateAlumno()

            		self.list_box.bind('<<ListboxSelect>>',AlumnoInfo)
            		
            		#self.tabs.bind('<ButtonRelease-1>',displayBooks)
            		self.list_box.bind('<Double-Button-1>',doubleClick)

            	except:
                	tkMessageBox.showerror("Error","No CONEXION a la base de datos!!!",icon='warning')
	
	def on_keyrelease(event):
	    # get text from entry
	    value = event.widget.get()
	    value = value.strip().lower()

	    # get data from test_list
	    if value == '':
		data = test_list
	    else:
		data = []
		for item in test_list:
		    if value in item.lower():
		        data.append(item)

	    # update data in listbox
	    listbox_update(data)


	def listbox_update(data):
	    # delete previous data
	    self.list_box.delete(0, 'end')

	    # sorting data
	    data = sorted(data, key=str.lower)

	    # put new data
	    for item in data:
		self.list_box.insert('end', item)

	def on_keyreleaseD(event):
	    # get text from entry
	    value = event.widget.get()
	    value = value.strip().lower()

	    # get data from test_list
	    if value == '':
		data = test_listD
	    else:
		data = []
		for item in test_listD:
		    if value in item.lower():
		        data.append(item)

	    # update data in listbox
	    listbox_updateD(data)


	def listbox_updateD(data):
	    # delete previous data
	    self.list_boxD.delete(0, 'end')

	    # sorting data
	    data = sorted(data, key=str.lower)

	    # put new data
	    for item in data:
		self.list_boxD.insert('end', item)


	def on_select(event):
	    pass
	    # display element selected on list
	    #print('(event) previous:', event.widget.get('active'))
	    #print('(event)  current:', event.widget.get(event.widget.curselection()))
	    #print('---')

	def comb1_selected(*args):
	    f = open (os.getcwd()+'/auxHuella/docente.uaz','r')
	    mensaje = f.read()
	    x1 = mensaje.split('+')
	    f.close()

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
	    
            
	    v = self.combo_ciclo.get()
	    if str(v) == ' ':
		pass
	    else:
		
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
			self.list_box.bind('<<ListboxSelect>>', on_select)
			listbox_update(test_list)
			cur.close()
			con.close()

			def AlumnoInfo(evt):
				f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
				mensaje = f.read()
				f.close()
				url = base64.b64decode(mensaje)
				x = url.split('-')
				con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
				cur = con.cursor()
                		value = str(self.list_box.get(self.list_box.curselection()))
                		id = value.split('-')[0]
				#print id
                		alumno = cur.execute("SELECT * FROM ALUMNO WHERE AL_MATRICULA = :1",(int(id),))
                		alumno_info = alumno.fetchall()
                		self.list_details.delete(0, END)
				self.list_details.insert(1, "                                              DETALLES                                              ")
                		self.list_details.insert(3, "Matricula: " + alumno_info[0][0])
                		self.list_details.insert(4, "Apellido Paterno : " + alumno_info[0][1])
				if(str(alumno_info[0][2])!="None"):
					self.list_details.insert(5, "Apellido Materno : " + alumno_info[0][2])
				else:
					self.list_details.insert(5, "Apellido Materno : ")
                		self.list_details.insert(6, "Nombre (s) : " + alumno_info[0][3])
				if(str(alumno_info[0][9])!="None"):
					self.list_details.insert(7, "Email : " + alumno_info[0][9])
				else:
					self.list_details.insert(7, "Email : ")
				if(alumno_info[0][10]==2):
					self.list_details.insert(8, "Género : " + "FEMENINO")
				else:
					self.list_details.insert(8, "Género : " + "MASCULINO")
				cur.close()
				con.close()
				
			def doubleClick(evt):
                		global  given_id
                		value=str(self.list_box.get(self.list_box.curselection()))
                		given_id=value.split('-')[0]
                		deletealumno=UpdateAlumno()

            		self.list_box.bind('<<ListboxSelect>>',AlumnoInfo)
            		
            		#self.tabs.bind('<ButtonRelease-1>',displayBooks)
            		self.list_box.bind('<Double-Button-1>',doubleClick)

			
            	except:
                	tkMessageBox.showerror("Error","Fallo la conexion de DB!!!",icon='warning')

		
		
		

	modelpath = os.getcwd()+"/MuestrasDeVoz/ModeloGMM/"
	files = [os.path.join(modelpath, fname) for fname in os.listdir(modelpath)]
	for fileA in files:
		remove(fileA)

	modelpath = os.getcwd()+"/auxHuella/HUELLA/"
	files = [os.path.join(modelpath, fname) for fname in os.listdir(modelpath)]
	for fileA in files:
		remove(fileA)

	modelpath = os.getcwd()+"/auxHuella/JUSTIFICACIONES/"
	files = [os.path.join(modelpath, fname) for fname in os.listdir(modelpath)]
	for fileA in files:
		remove(fileA)
        #Frames
        self.mainFrame =  tk.Frame(self.master)
        self.mainFrame.pack()
        #Top frames
        self.topFrame = tk.Frame(self.mainFrame,width=1350,height=70,bg='#f8f8f8',padx=0,relief=SUNKEN,borderwidth=2)
        self.topFrame.pack(side=TOP,fill=X)
        #Center frame
        self.centerFrame = tk.Frame(self.mainFrame,width=1350,relief=RIDGE,bg="#fdfff0",height=680)
        self.centerFrame.pack(side=TOP)
        #Center left frame
        self.centerLeftFrame = tk.Frame(self.centerFrame,width=900,height=700,bg='#fdfff0',relief='sunken',borderwidth=2)
        self.centerLeftFrame.pack(side=LEFT)
        #Center right frame
        self.centerRightFrame = tk.Frame(self.centerFrame, width=450, height=700, bg='#fdfff0', relief='sunken', borderwidth=2)
        self.centerRightFrame.pack()
        #Search bar
        self.search_bar = tk.LabelFrame(self.centerRightFrame,width=440,height=175,text="Búsqueda",bg='#fdfff0', font='arial 12 bold')
        self.search_bar.pack(fill=BOTH)
        self.lbl_search=tk.Label(self.search_bar,text="Buscar:", font='arial 13 bold', bg="#fdfff0", fg="black")
        self.lbl_search.grid(row=0,column=0,padx=20,pady=20)
        self.ent_search = tk.Entry(self.search_bar,width=36,bd=8)
        self.ent_search.grid(row=0,column=1,columnspan=3,padx=10,pady=10)
	self.lbl_grupos = tk.Label(self.search_bar,text="DOCENTE", font='arial 12 bold', bg="#fdfff0", fg="black")
        self.lbl_grupos.grid(row=1,column=0,padx=20,pady=20,columnspan=5)  
	self.img_library=tk.PhotoImage(file="icons/uaz4.png")
        self.lblImg=tk.Label(self.search_bar,image=self.img_library,bg="#fdfff0")
	self.lblImg.grid(row=2,column=0,padx=20,pady=20,columnspan=5) 
	self.lbl_grupos = tk.Label(self.search_bar,text='MODO ADMINISTRADOR', font='arial 12 bold', bg="#fdfff0", fg="black")
        self.lbl_grupos.grid(row=3,column=0,padx=20,pady=20,columnspan=5)

	self.mes1 = StringVar()
	self.mes2 = StringVar()

	self.lbl_grupo = tk.Label(self.search_bar,text="CICLO ESCOLAR", font='arial 12 bold', bg="#fdfff0", fg="black")
        self.lbl_grupo.grid(row=4,column=0,padx=20,pady=20,columnspan=5)
	self.combo_grupos = ttk.Combobox(self.search_bar, textvariable=self.mes1, values=(nameCiclo), state = 'readonly')
        self.combo_grupos.grid(row=5,column=0,padx=40,pady=20,columnspan=5)

	self.lbl_ciclo = tk.Label(self.search_bar,text="GRUPOS", font='arial 12 bold', bg="#fdfff0", fg="black")
        self.lbl_ciclo.grid(row=6,column=0,padx=20,pady=20,columnspan=5)
	self.combo_ciclo = ttk.Combobox(self.search_bar,textvariable=self.mes2, values=(nameMateria), state = 'readonly', width=30)
        self.combo_ciclo.grid(row=7,column=0,padx=30,pady=20,columnspan=5)
	
	self.btn_list=tk.Button(self.search_bar,text='Todos Los Alumnos', bg='#2488ff', fg='white', font='arial 16 bold', command = self.MostrarAlumno)
        self.btn_list.grid(row=8,column=0,padx=20,pady=20,columnspan=4)

	self.btn_salir=tk.Button(self.search_bar,text='Salir', bg='#2488ff', fg='white', font='arial 9 bold', command = self.SalirVentana)
        self.btn_salir.grid(row=9,column=0,padx=20,pady=20,columnspan=4)
        
        #add algo
        self.icon1 = tk.PhotoImage(file='icons/add.png')
        self.btn1 = tk.Button(self.topFrame,text='REGISTRAR ALUMNO', image=self.icon1,compound=LEFT,font='fixedsys 12 bold', foreground="#000000", background="#fef6fb",command=self.registroEstudiante)
	self.btn1.configure(image=self.icon1,compound=LEFT)   
	self.btn1.grid(row=0,column=0)  
	#add algo
        self.icon2 = tk.PhotoImage(file='icons/docente.png')
        self.btn2 = tk.Button(self.topFrame,text="REGISTRAR DOCENTE",font='fixedsys 12 bold', foreground="#000000",background="#fef6fb",command=self.claseAlumno)
        self.btn2.configure(image=self.icon2,compound=LEFT)
        self.btn2.grid(row=0,column=1)  
	#add algo
        self.icon3 = tk.PhotoImage(file='icons/clase.png')
        self.btn3 = tk.Button(self.topFrame,text="ASIGNACIÓN DE GRUPOS",font='fixedsys 12 bold', foreground="#000000", background="#fef6fb",command=self.claseDocente)
        self.btn3.configure(image=self.icon3,compound=LEFT)
        self.btn3.grid(row=0,column=2)  

	#add algo
        self.icon4 = tk.PhotoImage(file='icons/info.png')
        self.btn4 = tk.Button(self.topFrame,text="    ACERCA DE    ",font='fixedsys 12 bold', foreground="#000000", background="#fef6fb",command=self.Informacion)
        self.btn4.configure(image=self.icon4,compound=LEFT)
        self.btn4.grid(row=0,column=4)
	
	#add algo
        self.icon5 = tk.PhotoImage(file='icons/reporte.png')
        self.btn5 = tk.Button(self.topFrame,text="REPORTES DE ASISTENCIA",font='fixedsys 12 bold', foreground="#000000", background="#fef6fb",command=self.GenerarReportes)
        self.btn5.configure(image=self.icon5,compound=LEFT)
        self.btn5.grid(row=0,column=3)  

	self.tabs = ttk.Notebook(self.centerLeftFrame,width=980,height=685)
        self.tabs.pack()
        self.tab1_icon = PhotoImage(file='icons/estudiante-icono.png')
        self.tab2_icon = PhotoImage(file='icons/Docentes.png')
	self.tab3_icon = PhotoImage(file='icons/estadistica.png')
        self.tab1 = tk.Frame(self.tabs)
        self.tab2 = tk.Frame(self.tabs)
	self.tab3 = tk.Frame(self.tabs)
        self.tabs.add(self.tab1, text='Alumnado', image=self.tab1_icon, compound=LEFT)
        self.tabs.add(self.tab2, text='Docentes', image=self.tab2_icon, compound=LEFT)
        #list
        self.list_box = tk.Listbox(self.tab1,width=95,height=17,bd=7,font="times 12 bold")
        self.sb = tk.Scrollbar(self.tab1,orient=VERTICAL)
        self.list_box.grid(row=0,column=0,padx=(0,0),pady=0,sticky=N)
        self.sb.config(command=self.list_box.yview)
        self.list_box.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0,column=0,sticky=N+S+E)
        #detalles
        self.list_details = tk.Listbox(self.tab1,width=95,height=10,bd=7,font='times 12 bold')
        self.list_details.grid(row=1,column=0,padx=(0,0),pady=0,sticky=N)
	#list
        self.list_boxD = tk.Listbox(self.tab2,width=95,height=17,bd=7,font="times 12 bold")
        self.sbD = tk.Scrollbar(self.tab2,orient=VERTICAL)
        self.list_boxD.grid(row=0,column=0,padx=(0,0),pady=0,sticky=N)
        self.sbD.config(command=self.list_boxD.yview)
        self.list_boxD.config(yscrollcommand=self.sb.set)
        self.sbD.grid(row=0,column=0,sticky=N+S+E)
        #detalles
        self.list_detailsD = tk.Listbox(self.tab2,width=95,height=10,bd=7,font='times 12 bold')
        self.list_detailsD.grid(row=1,column=0,padx=(0,0),pady=0,sticky=N)
	del nameCiclo[:]
	del idsCiclo[:]
	if self.ADMIN != True: 	
		self.btn2['state'] = 'disabled'
		self.combo_grupos.bind("<<ComboboxSelected>>", comb1_selected)
		self.combo_ciclo.bind("<<ComboboxSelected>>", comb2_selected)	
		del test_list[:]
		f1 = open (os.getcwd()+'/auxHuella/docente.uaz','r')
		mensaje1 = f1.read()
		x1 = mensaje1.split('+')
		f1.close()
		self.lbl_grupos["text"] = x1[1]
		try:
			f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
			mensaje = f.read()
			f.close()
			url = base64.b64decode(mensaje)
			x = url.split('-')
			#print x
			con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
			cur = con.cursor()
			docentes = cur.execute("SELECT * FROM CICLO_ESCOLAR").fetchall()
			for alumnos in docentes:
				idsCiclo.append(str(alumnos[0]))
				nameCiclo.append(str(alumnos[5]))
			cur.close()
			con.close()
		except:
		        tkMessageBox.showerror("Error","No hay conexion a la base de datos!!!",icon='warning')
		self.tabs.bind('<<NotebookTabChanged>>',tabIndex)
		displayAlumnos(self)
		displayDocentes(self)
		self.combo_grupos['values']=nameCiclo
		self.combo_ciclo['values']=nameMateria
	else:
		self.btn1['state'] = 'disabled'
		self.btn3['state'] = 'disabled'
		self.btn4['state'] = 'disabled'
		self.btn5['state'] = 'disabled'
		self.btn_list['state'] = 'disabled'
		self.combo_grupos.config(state=DISABLED)
		self.combo_ciclo.config(state=DISABLED)

    def SalirVentana(self):
	self.master.destroy()
	l = Login.principal()
    def Informacion(self):
	l = info.Info()
    def registroEstudiante(self):
        agregarAlumno = agregarestudiante.AgregarEstudiante()
    def ConfigurarConexion(self):
        conexiondb = configurarconexion.ConfigurarConexion()
    def GenerarReportes(self):
	reportes = reportestable.ReporteStable()
    def claseAlumno(self):
	reportes = agregardocente.AgregarDocente()
    def claseDocente(self):
	docente = enrolarAlumno.EnrolarAlumno()
    def MostrarAlumno(self):
	f1 = open (os.getcwd()+'/auxHuella/docente.uaz','r')
	mensaje = f1.read()
	x1 = mensaje.split('+')
	f1.close()
	self.combo_grupos.set("")
	self.combo_ciclo.set("")
	# archivo-entrada.py
	f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
	mensaje = f.read()
	f.close()
	url = base64.b64decode(mensaje)
	x = url.split('-')
	con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
	cur = con.cursor()
	todos_alumnos = cur.execute("SELECT DISTINCT AL.AL_MATRICULA, AL.AL_NOMBRE, AL.AL_APATERNO, AL.AL_AMATERNO FROM ALUMNO AL JOIN ASIGNATURA ASI ON AL.AL_MATRICULA = ASI.AL_MATRICULA JOIN GRUPO GR ON GR.GR_CLAVE = ASI.GR_CLAVE AND GR.DO_CLAVE = '"+x1[0]+"' ORDER BY AL.AL_APATERNO").fetchall()
	self.list_box.delete(0,END)
	count=0
    	for alumno in todos_alumnos:
	        if(str(alumno[3])!='None'):
			self.list_box.insert(count,str(alumno[0])+" - "+alumno[1]+" "+alumno[2]+" "+alumno[3])
			count += 1
			test_list.append((str(alumno[0])+" - "+alumno[1]+" "+alumno[2]+" "+alumno[3]))
		else:
			self.list_box.insert(count,str(alumno[0])+" - "+alumno[1]+" "+alumno[2])
			count += 1
			test_list.append((str(alumno[0])+" - "+alumno[1]+" "+alumno[2]))

class DeleteDocente(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("500x400+550+200")
        self.title("¿Qué Hacer?")
        self.resizable(False,False)
        global given_idD

        # PANELES
        self.top = tk.Frame(self, height=150, bg='#05004e')
        self.top.pack(fill=X)
        self.botonFrame = tk.Frame(self, height=700, bg='#ffedc6')
        self.botonFrame.pack(fill=X)
        # ENCABEZADO, IMAGEN Y FECHA 
	self.top_image = PhotoImage(file='icons/uaz.png')
        self.top_image_lbl = tk.Label(self.top, image=self.top_image, bg="#05004e")
	self.top_image_lbl.place(x=0, y=10)
        self.encabezado = tk.Label(self.top, text='Docente', font='arial 20 bold', fg='white', bg="#05004e")
        self.encabezado.place(x=210, y=60)
        #ETIQUETAS Y ENTRADAS

	self.lbl_clave = tk.Label(self.botonFrame, text='Clave Administrador', font='arial 15 bold', fg='black', bg='#ffedc6')
        self.lbl_clave.place(x=50, y=50)

	self.ent_clave = tk.Entry(self.botonFrame, width=20, bd=2, font='arial 16 bold')
	self.ent_clave.config(show='*')
	
	
	self.ent_clave.place(x=120, y=100)
        
	
        #BOTON DE REGISTRO
        self.botonRegistro = tk.Button(self.botonFrame,text="Realizar Acción", font='arial 14 bold', command=self.realizarAccion)
        self.botonRegistro.place(x=130,y=170)
        self.lift() 

    def realizarAccion(self):
	if(self.ent_clave.get()!=""):
		
		url = self.ent_clave.get()
		con =  cx_Oracle.connect(url)
		cur = con.cursor()
		con.close()
		self.destroy()
		actualizar = UpdateDocente()
		#tkMessageBox.showerror("Error", "ERROR AL REALIZAR LA ACCIÓN", icon="warning")
	else:
        	tkMessageBox.showerror("Error", "DATO INVALIDO", icon="warning")
			
class UpdateDocente(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
	def comb1_selected(*args):
		NoAudios = []
		del NoAudios [:]
		for i in range(1, int(self.comboNoAudios.get().replace(" ", ""))+1):
		    NoAudios.append(i)
		self.comboAudios['values']=NoAudios
		self.comboAudios.current(0)
        self.geometry("1300x830+400+10")
        self.title("Editar Estudiante")
        self.resizable(False,False)
        # PANELES
        self.top = tk.Frame(self, height=100, bg='#05004e')
        self.top.pack(fill=X)
        self.botonFrame = tk.Frame(self, height=750, bg='#ffedc6')
        self.botonFrame.pack(fill=X)
        # ENCABEZADO, IMAGEN Y FECHA 
        self.top_image = PhotoImage(file='icons/uaz4.png')
        self.top_image_lbl = tk.Label(self.top, image=self.top_image, bg="#05004e")
        self.top_image_lbl.place(x=10, y=10)
        self.encabezado = tk.Label(self.top, text='EDITAR DATOS\nDE DOCENTE - UAZ', font='arial 20 bold', fg='white', bg="#05004e")
        self.encabezado.place(x=480, y=10)
        #ETIQUETAS Y ENTRADAS
	
	#AL_MATRICULA    NOT NULL    CHAR(8)
	self.lbl_matricula = tk.Label(self.botonFrame, text='Clave:', font='calibri 12 bold', fg='black', bg='#ffedc6')
	self.lbl_matricula.place(x=20, y=40)
	self.ent_matricula = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
	x = given_idD.split(' ')
	
	self.ent_matricula.insert(0, x[0])
	self.ent_matricula['state'] = 'disabled'
	self.ent_matricula.place(x=180, y=40)
	# archivo-entrada.py
	f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
	mensaje = f.read()
	f.close()
	url = base64.b64decode(mensaje)
	x = url.split('-')
	con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
	cur = con.cursor()

	alumno = cur.execute("SELECT * FROM DOCENTE WHERE DO_CLAVE = :1",(int(given_idD),))
	alumno_info = alumno.fetchall()
	
	#AL_APATERNO     NOT NULL    VARCHAR2(35)
	self.lbl_apaterno = tk.Label(self.botonFrame, text='A. Paterno:', font='calibri 12 bold', fg='black', bg='#ffedc6')
	self.lbl_apaterno.place(x=20, y=80)
	self.ent_apaterno = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
	self.ent_apaterno.insert(0, alumno_info[0][2])
	self.ent_apaterno.place(x=180, y=80)

	#AL_AMATERNO                 VARCHAR2(35)
	self.lbl_amaterno = tk.Label(self.botonFrame, text='A. Materno:', font='calibri 12 bold', fg='black', bg='#ffedc6')
	self.lbl_amaterno.place(x=20, y=120)
	self.ent_amaterno = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
	self.ent_amaterno.place(x=180, y=120)
	if(str(alumno_info[0][3]) != 'None'):
		self.ent_amaterno.insert(0, alumno_info[0][3])
	else:
		self.ent_amaterno.insert(0, "")
	#AL_NOMBRE       NOT NULL    VARCHAR2(35)
	self.lbl_anombre = tk.Label(self.botonFrame, text='Nombre:', font='calibri 12 bold', fg='black', bg='#ffedc6')
	self.lbl_anombre.place(x=20, y=160)
	self.ent_anombre = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
	self.ent_anombre.insert(0, alumno_info[0][4])
	self.ent_anombre.place(x=180, y=160)
	
	self.lbl_fecha = tk.Label(self.botonFrame, text='Nacimiento:', font='calibri 12 bold', fg='black', bg='#ffedc6')
	self.lbl_fecha.place(x=20, y=200)
	dias = []
	self.dia = StringVar()
	for i in range(1, 32):
	    dias.append(i)
	self.comboBox1 = ttk.Combobox(self.botonFrame, width=5, textvariable=self.dia, values=(dias), state='readonly')
	self.comboBox1.place(x=180, y=200)
	self.meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
      	self.mes = StringVar()
	self.comboBox2 = ttk.Combobox(self.botonFrame, width=10, textvariable=self.mes, values=(self.meses), state='readonly')
	self.comboBox2.place(x=260, y=200)
	anios = []
	self.anio = StringVar()
	x = datetime.datetime.now()
	for i in range(1949, x.year):
	    anios.append(i+1)
	self.comboBox3 = ttk.Combobox(self.botonFrame, width=5, textvariable=self.anio, values=(anios), state='readonly')
	self.comboBox3.place(x=395, y=200)
	if(str(alumno_info[0][5]) != 'None'):
		x = str(alumno_info[0][5])
		res = x.split(' ')
		aux = res[0].split('-')
		self.comboBox1.current(int(aux[2])-1)
		self.comboBox2.current(int(aux[1])-1)
		self.comboBox3.current(int(aux[0])-1950)
	else:
		self.comboBox1.current(30)
		self.comboBox2.current(1)
		self.comboBox3.current(35)
	
	#AL_CALLE                    VARCHAR2(50)
	self.lbl_calle = tk.Label(self.botonFrame, text='Calle:', font='calibri 12 bold', fg='black', bg='#ffedc6')
	self.lbl_calle.place(x=20, y=240)
	self.ent_calle = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
	self.ent_calle.place(x=180, y=240)
	if(str(alumno_info[0][6]) != 'None'):
		self.ent_calle.insert(0, alumno_info[0][6])
	else:
		self.ent_calle.insert(0, "")
	
	#AL_COLONIA                  VARCHAR2(50)
	self.lbl_colonia = tk.Label(self.botonFrame, text='Colonia:', font='calibri 12 bold', fg='black', bg='#ffedc6')
	self.lbl_colonia.place(x=20, y=280)
	self.ent_colonia = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
	self.ent_colonia.place(x=180, y=280)
	if(str(alumno_info[0][7]) != 'None'):
		self.ent_colonia.insert(0, alumno_info[0][7])
	else:
		self.ent_colonia.insert(0, "")
	
	#AL_CP                       CHAR(5)
	self.lbl_cp = tk.Label(self.botonFrame, text='C.P:', font='calibri 12 bold', fg='black', bg='#ffedc6')
	self.lbl_cp.place(x=20, y=320)
	self.ent_cp = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
	self.ent_cp.place(x=180, y=320)
	if(str(alumno_info[0][8]) != 'None'):
		self.ent_cp.insert(0, alumno_info[0][8])
	else:
		self.ent_cp.insert(0, "")
	#AL_TELEFONO                 VARCHAR2(20)
	self.lbl_telefono = tk.Label(self.botonFrame, text='Teléfono:', font='calibri 12 bold', fg='black', bg='#ffedc6')
	self.lbl_telefono.place(x=500, y=40)
	self.ent_telefono = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
	self.ent_telefono.place(x=640, y=40)
	if(str(alumno_info[0][9]) != 'None'):
		self.ent_telefono.insert(0, alumno_info[0][9])
	else:
		self.ent_telefono.insert(0, "")
	
	#AL_TELEFONOc                    VARCHAR2(50)
	self.lbl_telefonoc = tk.Label(self.botonFrame, text='T. Celular:', font='calibri 12 bold', fg='black', bg='#ffedc6')
	self.lbl_telefonoc.place(x=500, y=80)
	self.ent_telefonoc = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
	self.ent_telefonoc.place(x=640, y=80)
	if(str(alumno_info[0][10]) != 'None'):
		self.ent_telefonoc.insert(0, alumno_info[0][10])
	else:
		self.ent_telefonoc.insert(0, "")

	#AL_mail                VARCHAR2(50)
	self.lbl_mail = tk.Label(self.botonFrame, text='E-Mail:', font='calibri 12 bold', fg='black', bg='#ffedc6')
	self.lbl_mail.place(x=500, y=120)
	self.ent_mail = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
	self.ent_mail.place(x=640, y=120)
	if(str(alumno_info[0][11]) != 'None'):
		self.ent_mail.insert(0, alumno_info[0][11])
	else:
		self.ent_mail.insert(0, "")

	

	#AL_GENERO       NOT NULL    NUMBER(38)
	self.lbl_genero = tk.Label(self.botonFrame, text='Genéro:', font='calibri 12 bold', fg='black', bg='#ffedc6')
	self.lbl_genero.place(x=500, y=160)
	self.gender = IntVar(None, int(alumno_info[0][12]))
	self.rhombre = tk.Radiobutton(self.botonFrame, text='Hombre    ', value=1, var=self.gender, bg='#ffedc6', font='arial 10 bold')
	self.rhombre.place(x=640, y=165)
	self.rmujer = tk.Radiobutton(self.botonFrame, text='Mujer       ', value=2, var=self.gender, bg='#ffedc6', font='arial 10 bold')
	self.rmujer.place(x=780, y=165)
	
	#AL_MUNICIPIO                VARCHAR2(100)
	self.lbl_municipio = tk.Label(self.botonFrame, text='Título:', font='calibri 12 bold', fg='black', bg='#ffedc6')
	self.lbl_municipio.place(x=500, y=200)
	self.ent_municipio = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
	self.ent_municipio.place(x=640, y=200)
	if(str(alumno_info[0][13]) != 'None'):
		self.ent_municipio.insert(0, alumno_info[0][13])
	else:
		self.ent_municipio.insert(0, "")
	

	#AL_HUELLA                   BLOB
	self.lbl_huella = tk.Label(self.botonFrame, text='Huella Dactilar', font='calibri 18 bold', fg='black', bg='#ffedc6')
	self.lbl_huella.place(x=40, y=420)

	s = ttk.Style()
	s.theme_use('clam')
	s.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
	self.progbar = ttk.Progressbar(self.botonFrame, style="green.Horizontal.TProgressbar", orient=HORIZONTAL, length=200, mode = 'determinate')
	self.progbar.place(x=65, y=480)
	self.huellaOri = PhotoImage(file='icons/huella.png')
	self.huellaOri_lbl = tk.Label(self.botonFrame, image=self.huellaOri, bg="#ffedc6")
	self.huellaOri_lbl.place(x=100, y=520)
	 
	if(alumno_info[0][14] != None):
		self.progbar['value'] = 100
	else:
		self.progbar['value'] = 0

	#GE_CLAVE    NOT NULL NUMBER(38) 
	self.lbl_gescolar = tk.Label(self.botonFrame, text='G. Escolar:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_gescolar.place(x=500, y=240)
        try:
		del idgescolar[:]
		f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
		mensaje = f.read()
		f.close()
		url = base64.b64decode(mensaje)
		x = url.split('-')
		con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
		cur = con.cursor()
		grestudio = cur.execute("SELECT * FROM GRADO_ESTUDIO").fetchall()
		for estduio in grestudio:
			idgescolar.append(str(estduio[0])+'-'+str(estduio[1]))
		cur.close()
		con.close()
	except:
                tkMessageBox.showerror("Error","No hay conexion a la base de datos!!!",icon='warning')
	self.mes1 = StringVar()
	self.combo_grupos = ttk.Combobox(self.botonFrame, width=25, textvariable=self.mes1, values=(idgescolar), state = 'readonly')
        self.combo_grupos.place(x=640, y=240)
	self.combo_grupos.current(alumno_info[0][1]-1)

	
	#AL_VOZ                   BLOB
	self.lbl_VOZ = tk.Label(self.botonFrame, text='Plantilla\nDe Voz', font='calibri 15 bold', fg='black', bg='#ffedc6')
	self.lbl_VOZ.place(x=1080, y=400)
	self.progbarV = ttk.Progressbar(self.botonFrame, style="green.Horizontal.TProgressbar", orient=VERTICAL, length=150, mode = 'determinate')
	self.progbarV.place(x=1130, y=480)

	self.vozOri = PhotoImage(file='icons/voz.png')
	self.vozOri_lbl = tk.Label(self.botonFrame, image=self.vozOri, bg="#ffedc6")
	self.vozOri_lbl.place(x=320, y=510)

	self.lbl_Mvoz1 = tk.Label(self.botonFrame, text='Muestras de audio', font='calibri 10 bold', fg='black', bg='#ffedc6')
        self.lbl_Mvoz1.place(x=510, y=435)
	
	self.list_box1 = tk.Listbox(self.botonFrame,width=40,height=15,bd=1,font="times 9 bold")
        self.sb1 = tk.Scrollbar(self.botonFrame,orient=VERTICAL)
        self.list_box1.place(x=800, y=200)
        self.sb1.config(command=self.list_box1.yview)
        self.list_box1.config(yscrollcommand=self.sb1.set)
        self.list_box1.place(x=440, y=470)

	self.lbl_Mvoz2 = tk.Label(self.botonFrame, text='No. de muestras\na capturar', font='calibri 10 bold', fg='black', bg='#ffedc6')
        self.lbl_Mvoz2.place(x=780, y=470)
	muestrasAudio = []
	self.muestraAudio = StringVar()
	del muestrasAudio [:]
	for i in range(5, 31):
            muestrasAudio.append(i)
        self.comboNoAudios = ttk.Combobox(self.botonFrame, width=15, textvariable=self.muestraAudio, values=(muestrasAudio), state='readonly')
        self.comboNoAudios.place(x=780, y=535)
	self.comboNoAudios.current(0)
	self.comboNoAudios.bind("<<ComboboxSelected>>", comb1_selected)

	self.lbl_Mvoz3 = tk.Label(self.botonFrame, text='Muestra de audio\na capturar', font='calibri 10 bold', fg='black', bg='#ffedc6')
        self.lbl_Mvoz3.place(x=780, y=580)
	NoAudios = []
	for i in range(1, 6):
            NoAudios.append(i)
	self.NoMuestraAudio = StringVar()
        self.comboAudios = ttk.Combobox(self.botonFrame, width=15, textvariable=self.NoMuestraAudio, values=(NoAudios), state='readonly')
        self.comboAudios.place(x=780, y=635)
	self.comboAudios.current(0)

	self.botonGrabar = tk.Button(self.botonFrame,text="GRABAR", command=self.grabarAudio1, font='arial 10 bold')
	self.botonGrabar.configure(compound=LEFT)
        self.botonGrabar.place(x=780,y=680)

	self.botonGrabar['state'] = 'disabled'
	if(alumno_info[0][15] != None):
		self.progbarV['value'] = 100
	else:
		self.progbarV['value'] = 0

	#BOTON DE REGISTRO
	self.botonPlantillaVoz = tk.Button(self.botonFrame, command=self.ModelarMFCCGMM, text="Generar Plantilla\nDe Voz", font='arial 12 bold')
	self.botonPlantillaVoz.configure(compound=LEFT)
	self.botonPlantillaVoz.place(x=1050,y=640)
	self.botonPlantillaVoz['state'] = 'disabled'
	self.editarHuella = tk.Button(self.botonFrame,text="\n       Editar Huella      \n",command=self.HuellaCaptura, font='arial 14 bold')
	self.editarHuella.place(x=500,y=300)
	self.editarVoz = tk.Button(self.botonFrame,text="\n         Editar Voz         \n",command=self.HabilitarEdicionVoz, font='arial 14 bold')
	self.editarVoz.place(x=800,y=300)
	self.listo = tk.Button(self.botonFrame,text="\n  Actualizar Docente \n",command=self.addEstudiante, font='arial 14 bold')
      	self.listo.place(x=1000,y=40)
	self.salir = tk.Button(self.botonFrame,text="\n             SALIR             \n",command=self.SalirVentana, font='arial 14 bold')
      	self.salir.place(x=1000,y=180)
	self.lift()

    def SalirVentana(self):
	self.destroy()

    def HabilitarEdicionVoz(self):
	self.botonPlantillaVoz['state'] = 'disabled'
	self.botonGrabar['state'] = 'normal'
	self.progbarV['value'] = 0
	for name in os.listdir(os.getcwd()+"/MuestrasDeVoz/MuestrasAudio/"):
		remove(os.getcwd() + "/MuestrasDeVoz/MuestrasAudio/" + name)
    def editarMatricula(self):
	self.ent_matricula.configure(state="normal")

    def ModelarMFCCGMM(self):
	#va una condicion que pregunta si hay en el entry de matricula datos
	if(self.ent_matricula.get() != "" and self.ent_apaterno.get() != "" and self.ent_anombre.get() != ""):
		if(validacioncampos.Entero(self.ent_matricula.get()) == True and validacioncampos.Nombres(self.ent_apaterno.get()) == True and validacioncampos.Nombres(self.ent_anombre.get()) == True):
			modelpath = os.getcwd()+"/MuestrasDeVoz/MuestrasAudio/"
			files = [os.path.join(modelpath, fname) for fname in os.listdir(modelpath) if fname.endswith('.wav')]
			if len(files) == int(self.comboNoAudios.get().replace(" ", "")):
				for fileA in files:
					removeSilence.remover_silencio(fileA)	
				contador = 0
				f = open (os.getcwd()+"/MuestraDeAudio.txt",'w')
				for i in range(self.list_box1.size()):
					f.write(self.list_box1.get(i)+'\n')
				f.close()
				resultado = ModelarGMM(self.ent_matricula.get().replace(" ", ""),int(self.comboNoAudios.get().replace(" ", "")))
				self.progbarV['value'] = 100
				tkMessageBox.showinfo("ÉXITO","PLANTILLA DE VOZ GENERADA "+resultado,icon='info')
			else:
				tkMessageBox.showerror("ERROR","NO HAY SUFICIENTES MUESTRAS DE AUDIO PARA GENERAR LA PLANTILLA",icon='warning')
		else:
			tkMessageBox.showerror("ERROR","FORMATO DE DATOS INCORRECTO",icon='warning')
	else:
		tkMessageBox.showerror("ERROR","DATOS OBLIGATORIOS SIN COMPLETAR",icon='warning')

    
    def grabarAudio1(self):
	self.botonPlantillaVoz['state'] = 'disabled'
	r = os.system('arecord -D plughw:1 -d 5 -f cd '+os.getcwd()+'/MuestrasDeVoz/MuestrasAudio/Audio'+self.comboAudios.get().replace(" ", "")+'.wav')
	if r != 0:
		tkMessageBox.showerror("ERROR","MICRÓFONO DESCONECTADO",icon='warning')	

	modelpath = "MuestrasDeVoz/MuestrasAudio/"
	files = [os.path.join(modelpath, fname) for fname in os.listdir(modelpath) if fname.endswith('.wav')]
	
	count=0
	self.list_box1.delete(0,END)
	for name in os.listdir(os.getcwd()+"/MuestrasDeVoz/MuestrasAudio/"):
		self.list_box1.insert(count,str(name))
		count += 1
	#for file1 in files:
	self.botonFrame.update_idletasks()
	self.botonPlantillaVoz['state'] = 'normal'

    def addEstudiante(self):
    	status = "NULL"
	extranjero = "NULL"
	#print 'gender'+str(self.gender.get())
        if(self.ent_matricula.get() != "" and self.ent_apaterno.get() != "" and self.ent_anombre.get() != "" and self.gender.get() != 0 ):
		if(validacioncampos.Entero(self.ent_matricula.get()) == True and validacioncampos.Nombres(self.ent_apaterno.get()) == True and validacioncampos.Nombres(self.ent_anombre.get()) == True):
			if(validacioncampos.comprobar_fecha(int(self.anio.get()),int(self.meses.index(self.mes.get())+1),int(self.dia.get())) == True):
				grado = str(self.combo_grupos.get()).split('-')
				
				if self.ent_municipio.get() == "":

					f = open (os.getcwd()+"/auxHuella/datos.uaz",'w')
					
						
					f.write(base64.b64encode(self.ent_matricula.get().replace(" ", "") +","+grado[0]+","+self.ent_apaterno.get()+","+self.ent_amaterno.get()+","+self.ent_anombre.get()+","+str(self.dia.get()+"/"+self.mes.get()+"/"+self.anio.get())+","+self.ent_calle.get()+","+self.ent_colonia.get()+","+self.ent_cp.get()+","+self.ent_telefono.get()+","+self.ent_telefonoc.get()+","+self.ent_mail.get()+","+str(self.gender.get())+","+str('NULL')))
					f.close()
				else:
					f = open (os.getcwd()+"/auxHuella/datos.uaz",'w')
					
						
					f.write(base64.b64encode(self.ent_matricula.get().replace(" ", "") +","+grado[0]+","+self.ent_apaterno.get()+","+self.ent_amaterno.get()+","+self.ent_anombre.get()+","+str(self.dia.get()+"/"+self.mes.get()+"/"+self.anio.get())+","+self.ent_calle.get()+","+self.ent_colonia.get()+","+self.ent_cp.get()+","+self.ent_telefono.get()+","+self.ent_telefonoc.get()+","+self.ent_mail.get()+","+str(self.gender.get())+","+str(self.ent_municipio.get())))
					f.close()
				fd = commands.getoutput('java -classpath ./ojdbcfull/ojdbc6.jar:./ojdbcfull/ojdbc5.jar:./ojdbcfull/ons.jar:./ojdbcfull/orai18n.jar:./ojdbcfull/simplefan.jar:./ojdbcfull/ucp.jar:./ojdbcfull/xdb6.jar:. ActualizarDocente')
				if(fd != ""):
					tkMessageBox.showerror("ERROR","No se pudo agregar nada a la base de datos!!!",icon='warning')
					self.destroy()
				else:
					tkMessageBox.showinfo("ÉXITO","Los Datos Se Almacenaron Correctamente",icon='info')
					self.destroy()
			else:
				grado = str(self.combo_grupos.get()).split('-')
          			if self.ent_municipio.get() == "":

					f = open (os.getcwd()+"/auxHuella/datos.uaz",'w')
					
						
					f.write(base64.b64encode(self.ent_matricula.get().replace(" ", "") +","+grado[0]+","+self.ent_apaterno.get()+","+self.ent_amaterno.get()+","+self.ent_anombre.get()+",NULL,"+self.ent_calle.get()+","+self.ent_colonia.get()+","+self.ent_cp.get()+","+self.ent_telefono.get()+","+self.ent_telefonoc.get()+","+self.ent_mail.get()+","+str(self.gender.get())+","+str('NULL')))
					f.close()
				else:
					f = open (os.getcwd()+"/auxHuella/datos.uaz",'w')
					
						
					f.write(base64.b64encode(self.ent_matricula.get().replace(" ", "") +","+grado[0]+","+self.ent_apaterno.get()+","+self.ent_amaterno.get()+","+self.ent_anombre.get()+","+str(self.dia.get()+"/"+self.mes.get()+"/"+self.anio.get())+","+self.ent_calle.get()+","+self.ent_colonia.get()+","+self.ent_cp.get()+","+self.ent_telefono.get()+","+self.ent_telefonoc.get()+","+self.ent_mail.get()+","+str(self.gender.get())+","+str(self.ent_municipio.get())))
					f.close()
				fd = commands.getoutput('java -classpath ./ojdbcfull/ojdbc6.jar:./ojdbcfull/ojdbc5.jar:./ojdbcfull/ons.jar:./ojdbcfull/orai18n.jar:./ojdbcfull/simplefan.jar:./ojdbcfull/ucp.jar:./ojdbcfull/xdb6.jar:. ActualizarDocente')
				if(fd != ""):
					tkMessageBox.showerror("ERROR","NO SE ACTULIZARON LOS DATOS",icon='warning')
					self.destroy()
				else:
					tkMessageBox.showinfo("ÉXITO","SE ACTULIZARON CORRECTAMENTE LOS DATOS",icon='info')	
					self.destroy()					
		else:
          		tkMessageBox.showerror("ERROR","DATOS NO VALIDOS",icon='warning')
	else:
          	tkMessageBox.showerror("ERROR","DATOS INCOMPLETOS",icon='warning')

    def HuellaCaptura(self):
	pyfprint.fp_init()
	devs = pyfprint.discover_devices()
	if str(devs) != '[]':
		dev = devs[0]
		dev.open()
		fp, img = dev.enroll_finger()
		tkMessageBox.showinfo("Éxito","Huella Capturada Temporalmente \n Se verificara Ahora",icon='info')
		self.progbar['value'] = 40
		self.botonFrame.update_idletasks() 
		time.sleep(1)
		name = "huella"+self.ent_matricula.get()
		b = fp.data()
		with open(os.getcwd()+"/auxHuella/HUELLA/" + name, "wb") as file:
			file.write(bytes(b))
		i, fp1 = dev.verify_finger(fp)
		self.progbar['value'] = 60
		self.botonFrame.update_idletasks() 
		time.sleep(1) 
		i2, fp2 = dev.verify_finger(fp)
		self.progbar['value'] = 80
		self.botonFrame.update_idletasks() 
		time.sleep(1) 
		if(str(i)=='True' or str(i2)=='True'):
			self.progbar['value'] = 100
			self.botonFrame.update_idletasks() 
			time.sleep(1) 
			dev.close()
			pyfprint.fp_exit()
			tkMessageBox.showinfo("Éxito","Huella Capturada",icon='info')
			time.sleep(1) 
		else:
			tkMessageBox.showerror("Error","No coincide huella",icon='warning')
			self.progbar['value'] = 0
			self.botonFrame.update_idletasks() 
			time.sleep(1) 
			dev.close()
			pyfprint.fp_exit()		
	else:
		tkMessageBox.showerror("Error","No se encuentra conectado el lector",icon='info')
    	
    	      

class UpdateAlumno(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
	def comb1_selected(*args):
		NoAudios = []
		del NoAudios [:]
		for i in range(1, int(self.comboNoAudios.get().replace(" ", ""))+1):
		    NoAudios.append(i)
		self.comboAudios['values']=NoAudios
		self.comboAudios.current(0)
        self.geometry("1300x830+400+10")
        self.title("Editar Estudiante")
        self.resizable(False,False)
        # PANELES
        self.top = tk.Frame(self, height=100, bg='#05004e')
        self.top.pack(fill=X)
        self.botonFrame = tk.Frame(self, height=750, bg='#ffedc6')
        self.botonFrame.pack(fill=X)
        # ENCABEZADO, IMAGEN Y FECHA 
        self.top_image = PhotoImage(file='icons/uaz4.png')
        self.top_image_lbl = tk.Label(self.top, image=self.top_image, bg="#05004e")
        self.top_image_lbl.place(x=10, y=10)
        self.encabezado = tk.Label(self.top, text='EDITAR DATOS\nDE ESTUDIANTE - UAZ', font='arial 20 bold', fg='white', bg="#05004e")
        self.encabezado.place(x=460, y=10)
        #ETIQUETAS Y ENTRADAS
	try:
		#AL_MATRICULA    NOT NULL    CHAR(8)
		self.lbl_matricula = tk.Label(self.botonFrame, text='Matrícula:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_matricula.place(x=20, y=40)
		self.ent_matricula = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
		x = given_id.split(' ')
		
		self.ent_matricula.insert(0, x[0])
		self.ent_matricula['state'] = 'disabled'
		self.ent_matricula.place(x=180, y=40)
		# archivo-entrada.py
		f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
		mensaje = f.read()
		f.close()
		url = base64.b64decode(mensaje)
		x = url.split('-')
		con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
		cur = con.cursor()

		alumno = cur.execute("SELECT * FROM ALUMNO WHERE AL_MATRICULA = :1",(int(given_id),))
		alumno_info = alumno.fetchall()
		
		#AL_APATERNO     NOT NULL    VARCHAR2(35)
		self.lbl_apaterno = tk.Label(self.botonFrame, text='A. Paterno:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_apaterno.place(x=20, y=80)
		self.ent_apaterno = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
		self.ent_apaterno.insert(0, alumno_info[0][1])
		self.ent_apaterno.place(x=180, y=80)
		#AL_AMATERNO                 VARCHAR2(35)
		self.lbl_amaterno = tk.Label(self.botonFrame, text='A. Materno:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_amaterno.place(x=20, y=120)
		self.ent_amaterno = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
		self.ent_amaterno.place(x=180, y=120)
		if(str(alumno_info[0][2]) != 'None'):
			self.ent_amaterno.insert(0, alumno_info[0][2])
		else:
			self.ent_amaterno.insert(0, "")
		#AL_NOMBRE       NOT NULL    VARCHAR2(35)
		self.lbl_anombre = tk.Label(self.botonFrame, text='Nombre:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_anombre.place(x=20, y=160)
		self.ent_anombre = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
		self.ent_anombre.insert(0, alumno_info[0][3])
		self.ent_anombre.place(x=180, y=160)
		self.lbl_fecha = tk.Label(self.botonFrame, text='Nacimiento:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_fecha.place(x=20, y=200)
		dias = []
		self.dia = StringVar()
		for i in range(1, 32):
		    dias.append(i)
		self.comboBox1 = ttk.Combobox(self.botonFrame, width=5, textvariable=self.dia, values=(dias), state='readonly')
		self.comboBox1.place(x=180, y=200)
		self.meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
	      	self.mes = StringVar()
		self.comboBox2 = ttk.Combobox(self.botonFrame, width=10, textvariable=self.mes, values=(self.meses), state='readonly')
		self.comboBox2.place(x=260, y=200)
		anios = []
		self.anio = StringVar()
		x = datetime.datetime.now()
		for i in range(1949, x.year):
		    anios.append(i+1)
		self.comboBox3 = ttk.Combobox(self.botonFrame, width=5, textvariable=self.anio, values=(anios), state='readonly')
		self.comboBox3.place(x=395, y=200)
		if(str(alumno_info[0][4]) != 'None'):
			x = str(alumno_info[0][4])
			res = x.split(' ')
			aux = res[0].split('-')
			self.comboBox1.current(int(aux[2])-1)
			self.comboBox2.current(int(aux[1])-1)
			self.comboBox3.current(int(aux[0])-1950)
		else:
			self.comboBox1.current(30)
			self.comboBox2.current(1)
			self.comboBox3.current(35)
		#AL_CALLE                    VARCHAR2(50)
		self.lbl_calle = tk.Label(self.botonFrame, text='Calle:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_calle.place(x=20, y=240)
		self.ent_calle = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
		self.ent_calle.place(x=180, y=240)
		if(str(alumno_info[0][5]) != 'None'):
			self.ent_calle.insert(0, alumno_info[0][5])
		else:
			self.ent_calle.insert(0, "")
		#AL_COLONIA                  VARCHAR2(50)
		self.lbl_colonia = tk.Label(self.botonFrame, text='Colonia:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_colonia.place(x=20, y=280)
		self.ent_colonia = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
		self.ent_colonia.place(x=180, y=280)
		if(str(alumno_info[0][6]) != 'None'):
			self.ent_colonia.insert(0, alumno_info[0][6])
		else:
			self.ent_colonia.insert(0, "")
		#AL_CP                       CHAR(5)
		self.lbl_cp = tk.Label(self.botonFrame, text='C.P:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_cp.place(x=20, y=320)
		self.ent_cp = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
		self.ent_cp.place(x=180, y=320)
		if(str(alumno_info[0][7]) != 'None'):
			self.ent_cp.insert(0, alumno_info[0][7])
		else:
			self.ent_cp.insert(0, "")
		#AL_TELEFONO                 VARCHAR2(20)
		self.lbl_telefono = tk.Label(self.botonFrame, text='Teléfono:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_telefono.place(x=500, y=40)
		self.ent_telefono = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
		self.ent_telefono.place(x=640, y=40)
		if(str(alumno_info[0][8]) != 'None'):
			self.ent_telefono.insert(0, alumno_info[0][8])
		else:
			self.ent_telefono.insert(0, "")
		#AL_EMAIL                    VARCHAR2(50)
		self.lbl_email = tk.Label(self.botonFrame, text='E-Mail:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_email.place(x=500, y=80)
		self.ent_email = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
		self.ent_email.place(x=640, y=85)
		if(str(alumno_info[0][9]) != 'None'):
			self.ent_email.insert(0, alumno_info[0][9])
		else:
			self.ent_email.insert(0, "")
		#AL_GENERO       NOT NULL    NUMBER(38)
		self.lbl_genero = tk.Label(self.botonFrame, text='Genéro:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_genero.place(x=500, y=120)
		self.gender = IntVar(None, int(alumno_info[0][10]))
		self.rhombre = tk.Radiobutton(self.botonFrame, text='Hombre    ', value=1, var=self.gender, bg='#ffedc6', font='arial 10 bold')
		self.rhombre.place(x=640, y=125)
		self.rmujer = tk.Radiobutton(self.botonFrame, text='Mujer       ', value=2, var=self.gender, bg='#ffedc6', font='arial 10 bold')
		self.rmujer.place(x=780, y=125)
		#AL_STATUS                   NUMBER(38)
		if(str(alumno_info[0][11]) != 'None'):
			self.isActivo = IntVar(None, int(alumno_info[0][11]))
		else:
			self.isActivo = IntVar(None, 0)
		self.lbl_status = tk.Label(self.botonFrame, text='Status:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_status.place(x=500, y=160)
		self.ractivo = tk.Radiobutton(self.botonFrame, text='Activo      ', value=1, var=self.isActivo, bg='#ffedc6', font='arial 10 bold')
		self.ractivo.place(x=640, y=165)
		self.rinactivo = tk.Radiobutton(self.botonFrame, text='Desactivo', value=2, var=self.isActivo, bg='#ffedc6', font='arial 10 bold')
		self.rinactivo.place(x=780, y=165)
		#AL_EXTRANJERO               NUMBER(38)
		if(str(alumno_info[0][12]) != 'None'):
			self.isExtranjero = IntVar(None, int(alumno_info[0][12]))
		else:
			self.isExtranjero = IntVar(None, 0)
		self.lbl_extranjero = tk.Label(self.botonFrame, text='Extranjero:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_extranjero.place(x=500, y=200)
		self.risextranejero = tk.Radiobutton(self.botonFrame, text='Extranjero', value=1, var=self.isExtranjero, bg='#ffedc6', font='arial 10 bold')
		self.risextranejero.place(x=640, y=205)
		self.rinoextranjero = tk.Radiobutton(self.botonFrame, text='Nacional  ', value=2, var=self.isExtranjero, bg='#ffedc6',font='arial 10 bold')
		self.rinoextranjero.place(x=780, y=205)
		#AL_MUNICIPIO                VARCHAR2(100)
		self.lbl_municipio = tk.Label(self.botonFrame, text='Municipio:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_municipio.place(x=500, y=240)
		self.ent_municipio = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
		self.ent_municipio.place(x=640, y=245)
		if(str(alumno_info[0][13]) != 'None'):
			self.ent_municipio.insert(0, alumno_info[0][13])
		else:
			self.ent_municipio.insert(0, "")
		#AL_ESTADO                   VARCHAR2(100)
		self.lbl_estado = tk.Label(self.botonFrame, text='Estado:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_estado.place(x=500, y=280)
		self.ent_estado = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
		self.ent_estado.place(x=640, y=285)
		if(str(alumno_info[0][14]) != 'None'):
			self.ent_estado.insert(0, alumno_info[0][14])
		else:
			self.ent_estado.insert(0, "")
		
		
		#AL_FINGRESO                 DATE
		self.lbl_fecha2 = tk.Label(self.botonFrame, text='Ingreso:', font='calibri 12 bold', fg='black', bg='#ffedc6')
		self.lbl_fecha2.place(x=500, y=320)
		dias1 = []
		self.dia1 = StringVar()
		for i in range(1, 32):
		    dias1.append(i)
		self.comboBox4 = ttk.Combobox(self.botonFrame, width=5, textvariable=self.dia1, values=(dias1), state='readonly')
		self.comboBox4.place(x=640, y=325)
		self.meses1 = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
		self.mes1 = StringVar()
		self.comboBox5 = ttk.Combobox(self.botonFrame, width=10, textvariable=self.mes1, values=(self.meses1), state='readonly')
		self.comboBox5.place(x=720, y=325)
		
		anios1 = []
		self.anio1 = StringVar()
		x1 = datetime.datetime.now()
		for i in range(1949, x1.year):
		    anios1.append(i + 1)
		self.comboBox6 = ttk.Combobox(self.botonFrame, width=5, textvariable=self.anio1, values=(anios1), state='readonly')
		self.comboBox6.place(x=855, y=325)
		if(str(alumno_info[0][15]) != 'None'):
			x1 = str(alumno_info[0][15])
			res1 = x1.split(' ')
			aux1 = res1[0].split('-')
			self.comboBox4.current(int(aux1[2])-1)
			self.comboBox5.current(int(aux1[1])-1)
			self.comboBox6.current(int(aux1[0])-1950)
		else:
			self.comboBox4.current(30)
			self.comboBox5.current(1)
			self.comboBox6.current(35)

		#AL_HUELLA                   BLOB
		self.lbl_huella = tk.Label(self.botonFrame, text='Huella Dactilar', font='calibri 18 bold', fg='black', bg='#ffedc6')
		self.lbl_huella.place(x=40, y=420)

		s = ttk.Style()
		s.theme_use('clam')
		s.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
		self.progbar = ttk.Progressbar(self.botonFrame, style="green.Horizontal.TProgressbar", orient=HORIZONTAL, length=200, mode = 'determinate')
		self.progbar.place(x=65, y=480)
		self.huellaOri = PhotoImage(file='icons/huella.png')
		self.huellaOri_lbl = tk.Label(self.botonFrame, image=self.huellaOri, bg="#ffedc6")
		self.huellaOri_lbl.place(x=100, y=520)
		 
		if(alumno_info[0][16] != None):
			self.progbar['value'] = 100
		else:
			self.progbar['value'] = 0

		#AL_VOZ                   BLOB
		self.lbl_VOZ = tk.Label(self.botonFrame, text='Plantilla\nDe Voz', font='calibri 15 bold', fg='black', bg='#ffedc6')
		self.lbl_VOZ.place(x=1080, y=400)
		self.progbarV = ttk.Progressbar(self.botonFrame, style="green.Horizontal.TProgressbar", orient=VERTICAL, length=150, mode = 'determinate')
		self.progbarV.place(x=1130, y=480)

		self.vozOri = PhotoImage(file='icons/voz.png')
		self.vozOri_lbl = tk.Label(self.botonFrame, image=self.vozOri, bg="#ffedc6")
		self.vozOri_lbl.place(x=320, y=510)

		self.lbl_Mvoz1 = tk.Label(self.botonFrame, text='Muestras de audio', font='calibri 10 bold', fg='black', bg='#ffedc6')
		self.lbl_Mvoz1.place(x=510, y=435)
		
		self.list_box1 = tk.Listbox(self.botonFrame,width=40,height=15,bd=1,font="times 9 bold")
		self.sb1 = tk.Scrollbar(self.botonFrame,orient=VERTICAL)
		self.list_box1.place(x=800, y=200)
		self.sb1.config(command=self.list_box1.yview)
		self.list_box1.config(yscrollcommand=self.sb1.set)
		self.list_box1.place(x=440, y=470)

		self.lbl_Mvoz2 = tk.Label(self.botonFrame, text='No. de muestras\na capturar', font='calibri 10 bold', fg='black', bg='#ffedc6')
		self.lbl_Mvoz2.place(x=780, y=470)
		muestrasAudio = []
		self.muestraAudio = StringVar()
		del muestrasAudio [:]
		for i in range(5, 31):
		    muestrasAudio.append(i)
		self.comboNoAudios = ttk.Combobox(self.botonFrame, width=15, textvariable=self.muestraAudio, values=(muestrasAudio), state='readonly')
		self.comboNoAudios.place(x=780, y=535)
		self.comboNoAudios.current(0)
		self.comboNoAudios.bind("<<ComboboxSelected>>", comb1_selected)

		self.lbl_Mvoz3 = tk.Label(self.botonFrame, text='Muestra de audio\na capturar', font='calibri 10 bold', fg='black', bg='#ffedc6')
		self.lbl_Mvoz3.place(x=780, y=580)
		NoAudios = []
		for i in range(1, 6):
		    NoAudios.append(i)
		self.NoMuestraAudio = StringVar()
		self.comboAudios = ttk.Combobox(self.botonFrame, width=15, textvariable=self.NoMuestraAudio, values=(NoAudios), state='readonly')
		self.comboAudios.place(x=780, y=635)
		self.comboAudios.current(0)

		self.botonGrabar = tk.Button(self.botonFrame,text="GRABAR", command=self.grabarAudio1, font='arial 10 bold')
		self.botonGrabar.configure(compound=LEFT)
		self.botonGrabar.place(x=780,y=680)
		self.botonGrabar['state'] = 'disabled'

		

		if(alumno_info[0][17] != None):
			self.progbarV['value'] = 100
			
		else:
			self.progbarV['value'] = 0
			

		#BOTON DE REGISTRO
		self.botonPlantillaVoz = tk.Button(self.botonFrame, command=self.ModelarMFCCGMM, text="Generar Plantilla\nDe Voz", font='arial 12 bold')
		self.botonPlantillaVoz.configure(compound=LEFT)
		self.botonPlantillaVoz.place(x=1050,y=640)
		self.botonPlantillaVoz['state'] = 'disabled'
		self.editarHuella = tk.Button(self.botonFrame,text="       Salir       ",command=self.SalirVentana, font='arial 14 bold')
		self.editarHuella.place(x=1000,y=40)
		self.editarHuella = tk.Button(self.botonFrame,text="       Editar Huella       ",command=self.HuellaCaptura, font='arial 14 bold')
		self.editarHuella.place(x=1000,y=140)
		self.editarVoz = tk.Button(self.botonFrame,text="         Editar Voz         ",command=self.HabilitarEdicionVoz, font='arial 14 bold')
		self.editarVoz.place(x=1000,y=240)
		self.listo = tk.Button(self.botonFrame,text="Actualizar Estudiante",command=self.addEstudiante, font='arial 14 bold')
	      	self.listo.place(x=1000,y=340)
		self.lift()
    	except:
        	tkMessageBox.showerror("Error","Fallo la conexion de DB!!!",icon='warning')

    def SalirVentana(self):
	self.destroy()
	sys.exit()
        
    def HabilitarEdicionVoz(self):
	self.botonPlantillaVoz['state'] = 'disabled'
	self.botonGrabar['state'] = 'normal'
	self.progbarV['value'] = 0
	for name in os.listdir(os.getcwd()+"/MuestrasDeVoz/MuestrasAudio/"):
		remove(os.getcwd() + "/MuestrasDeVoz/MuestrasAudio/" + name)

    def grabarAudio1(self):
	self.botonPlantillaVoz['state'] = 'disabled'
	r = os.system('arecord -D plughw:1 -d 5 -f cd '+os.getcwd()+'/MuestrasDeVoz/MuestrasAudio/Audio'+self.comboAudios.get().replace(" ", "")+'.wav')
	if r != 0:
		tkMessageBox.showerror("ERROR","MICRÓFONO DESCONECTADO",icon='warning')	

	modelpath = "MuestrasDeVoz/MuestrasAudio/"
	files = [os.path.join(modelpath, fname) for fname in os.listdir(modelpath) if fname.endswith('.wav')]
	
	count=0
	self.list_box1.delete(0,END)
	for name in os.listdir(os.getcwd()+"/MuestrasDeVoz/MuestrasAudio/"):
		self.list_box1.insert(count,str(name))
		count += 1
	#for file1 in files:
	self.botonFrame.update_idletasks()
	self.botonPlantillaVoz['state'] = 'normal'
	

    def editarMatricula(self):
	self.ent_matricula.configure(state="normal")
    def ModelarMFCCGMM(self):
	#va una condicion que pregunta si hay en el entry de matricula datos
	if(self.ent_matricula.get() != "" and self.ent_apaterno.get() != "" and self.ent_anombre.get() != ""):
		if(validacioncampos.Entero(self.ent_matricula.get()) == True and validacioncampos.Nombres(self.ent_apaterno.get()) == True and validacioncampos.Nombres(self.ent_anombre.get()) == True):
			modelpath = os.getcwd()+"/MuestrasDeVoz/MuestrasAudio/"
			files = [os.path.join(modelpath, fname) for fname in os.listdir(modelpath) if fname.endswith('.wav')]
			if len(files) == int(self.comboNoAudios.get().replace(" ", "")):
				for fileA in files:
					removeSilence.remover_silencio(fileA)	
				contador = 0
				f = open (os.getcwd()+"/MuestraDeAudio.txt",'w')
				for i in range(self.list_box1.size()):
					f.write(self.list_box1.get(i)+'\n')
				f.close()
				resultado = ModelarGMM(self.ent_matricula.get().replace(" ", ""),int(self.comboNoAudios.get().replace(" ", "")))
				self.progbarV['value'] = 100
				tkMessageBox.showinfo("ÉXITO","PLANTILLA DE VOZ GENERADA "+resultado,icon='info')
			else:
				tkMessageBox.showerror("ERROR","NO HAY SUFICIENTES MUESTRAS DE AUDIO PARA GENERAR LA PLANTILLA",icon='warning')
		else:
			tkMessageBox.showerror("ERROR","FORMATO DE DATOS INCORRECTO",icon='warning')
	else:
		tkMessageBox.showerror("ERROR","DATOS OBLIGATORIOS SIN COMPLETAR",icon='warning')

    

    def addEstudiante(self):
    	status = "NULL"
	extranjero = "NULL"
        if(self.ent_matricula.get() != "" and self.ent_apaterno.get() != "" and self.ent_anombre.get() != "" and self.gender.get() != 0 ):
		if(validacioncampos.Entero(self.ent_matricula.get()) == True and validacioncampos.Nombres(self.ent_apaterno.get()) == True and validacioncampos.Nombres(self.ent_anombre.get()) == True):
			
			if(validacioncampos.comprobar_fecha(int(self.anio.get()),int(self.meses.index(self.mes.get())+1),int(self.dia.get())) == True and validacioncampos.comprobar_fecha(int(self.anio1.get()),int(self.meses1.index(self.mes1.get())+1),int(self.dia1.get())) == True):
				if(self.isExtranjero.get()==0):
					status = "NULL"
				else:
					status = self.isExtranjero.get()
				if(self.isExtranjero.get()==0):
					extranjero = "NULL"
				else:
					extranjero = self.isExtranjero.get()
				f = open (os.getcwd()+"/auxHuella/datos.uaz",'w')
				f.write(base64.b64encode(self.ent_matricula.get().replace(" ", "") +","+self.ent_apaterno.get()+","+self.ent_amaterno.get()+","+self.ent_anombre.get()+","+str(self.dia.get()+"/"+self.mes.get()+"/"+self.anio.get())+","+self.ent_calle.get()+","+self.ent_colonia.get()+","+self.ent_cp.get()+","+self.ent_telefono.get()+","+self.ent_email.get()+","+str(self.gender.get())+","+str(status)+","+str(extranjero)+","+self.ent_municipio.get()+","+self.ent_estado.get()+","+str(self.dia1.get()+"/"+self.mes1.get()+"/"+self.anio1.get())))
				f.close()
				fd = commands.getoutput('java -classpath ./ojdbcfull/ojdbc6.jar:./ojdbcfull/ojdbc5.jar:./ojdbcfull/ons.jar:./ojdbcfull/orai18n.jar:./ojdbcfull/simplefan.jar:./ojdbcfull/ucp.jar:./ojdbcfull/xdb6.jar:. Actualizar')
				if(fd != ""):
					tkMessageBox.showerror("ERROR","No se pudo agregar nada a la base de datos!!!",icon='warning')
					self.destroy()
				else:
					tkMessageBox.showinfo("ÉXITO","Los Datos Se Almacenaron Correctamente",icon='info')
					self.destroy()
					
					
			else:
				status = "NULL"
				extranjero = "NULL"
				if(self.isExtranjero.get()==0):
					status = "NULL"
				else:
					status = self.isExtranjero.get()
				if(self.isExtranjero.get()==0):
					extranjero = "NULL"
				else:
					extranjero = self.isExtranjero.get()
          			f = open (os.getcwd()+"/auxHuella/datos.uaz",'w')
				f.write(base64.b64encode(self.ent_matricula.get().replace(" ", "") +","+self.ent_apaterno.get()+","+self.ent_amaterno.get()+","+self.ent_anombre.get()+",NULL,"+self.ent_calle.get()+","+self.ent_colonia.get()+","+self.ent_cp.get()+","+self.ent_telefono.get()+","+self.ent_email.get()+","+str(self.gender.get())+","+str(status)+","+str(extranjero)+","+self.ent_municipio.get()+","+self.ent_estado.get()+",NULL"))
				f.close()
				fd = commands.getoutput('java -classpath ./ojdbcfull/ojdbc6.jar:./ojdbcfull/ojdbc5.jar:./ojdbcfull/ons.jar:./ojdbcfull/orai18n.jar:./ojdbcfull/simplefan.jar:./ojdbcfull/ucp.jar:./ojdbcfull/xdb6.jar:. Actualizar')
				if(fd != ""):
					tkMessageBox.showerror("ERROR","NO SE ACTULIZARON LOS DATOS",icon='warning')
					self.destroy()
				else:
					tkMessageBox.showinfo("ÉXITO","SE ACTULIZARON CORRECTAMENTE LOS DATOS",icon='info')	
					self.destroy()
					
		else:
          		tkMessageBox.showerror("ERROR","DATOS NO VALIDOS",icon='warning')
	else:
          	tkMessageBox.showerror("ERROR","DATOS INCOMPLETOS",icon='warning')

    def HuellaCaptura(self):
	self.progbar['value'] = 0
	pyfprint.fp_init()
	devs = pyfprint.discover_devices()
	if str(devs) != '[]':
		dev = devs[0]
		dev.open()
		fp, img = dev.enroll_finger()
		tkMessageBox.showinfo("Éxito","Huella Capturada Temporalmente \n Se verificara Ahora",icon='info')
		self.progbar['value'] = 40
		self.botonFrame.update_idletasks() 
		time.sleep(1)
		name = "huella"+self.ent_matricula.get()
		b = fp.data()
		with open(os.getcwd()+"/auxHuella/HUELLA/" + name, "wb") as file:
			file.write(bytes(b))
		i, fp1 = dev.verify_finger(fp)
		self.progbar['value'] = 60
		self.botonFrame.update_idletasks() 
		time.sleep(1) 
		i2, fp2 = dev.verify_finger(fp)
		self.progbar['value'] = 80
		self.botonFrame.update_idletasks() 
		time.sleep(1) 
		if(str(i)=='True' or str(i2)=='True'):
			self.progbar['value'] = 100
			self.botonFrame.update_idletasks() 
			time.sleep(1) 
			dev.close()
			pyfprint.fp_exit()
			tkMessageBox.showinfo("Éxito","Huella Capturada",icon='info')
			time.sleep(1) 
			dev.close()
			pyfprint.fp_exit()
		else:
			tkMessageBox.showerror("Error","No coincide huella",icon='warning')
			self.progbar['value'] = 0
			self.botonFrame.update_idletasks() 
			time.sleep(1) 
			dev.close()
			pyfprint.fp_exit()		
	else:
		tkMessageBox.showerror("Error","No se encuentra conectado el lector",icon='info')

def Principal(admin):
    root = Tk()
    app = Main(root, admin)
    root.title("SISTEMA DE ASISTENCIA ESCOLAR - UNIVERSIDAD AUTÓNOMA DE ZACATECAS")
    #root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.geometry("1550x850+220+100")
    root.resizable(False,False)
    #root.iconbitmap('icons/icon.ico')
    #root.attributes('-fullscreen', True)
    #root.bind("<Escape>", lambda e: e.widget.quit())
    root.mainloop()


