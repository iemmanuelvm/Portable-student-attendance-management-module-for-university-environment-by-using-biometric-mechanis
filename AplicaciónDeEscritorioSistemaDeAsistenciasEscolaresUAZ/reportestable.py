# -*- coding: utf-8 -*-
import Tkinter, tkMessageBox
from Tkinter import *
import Tkinter as tk
import ttk, cx_Oracle, os, base64, datetime, commands
from datetime import date
from ttk import *
import reportviewsend
import reportesasistencia
import IdentificacionUSUARIOS
test_list = []
test_list1 = []
idsCiclo = []
nameCiclo = []
idsGrupos = []
nameMateria = []
claveGrupo = []
idMatricula = []
class ReporteStable(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
	self.matricula = ""
	self.cicloE = ""
	self.cGrupo = ""
	def selectItem(a):
	    curItem = self.tree.focus()
	    dic = self.tree.item(curItem)
	    try:
		    self.btnGenREporte['state'] = 'normal'
		    if dic['values'][5] == "JUSTIFICADO" or dic['values'][5] == "ASISTIO":
			    self.btnJustificar['state'] = 'disabled'
			    
		    else:
			    self.btnJustificar['state'] = 'normal'
			    
		    if self.ciclo_escolarcbx.get().replace(' ', '')!="" and self.ciclo_gruposcbx.get().replace(' ', '')!="":
			    self.matricula = dic['text']
			    self.cicloE = str(idsCiclo[int(self.ciclo_escolarcbx.current())])
			    self.cGrupo = str(claveGrupo[int(self.ciclo_gruposcbx.current())])
		    else:
			    self.matricula = ""
			    self.cicloE = ""
			    self.cGrupo = ""
	    except:
		    pass
	    

	def comb1_selected(*args):
	    f = open (os.getcwd()+'/auxHuella/docente.uaz','r')
	    mensaje = f.read()
	    x1 = mensaje.split('+')
	    f.close()

	    

	    if (self.ciclo_escolarcbx.current() != -1 ):
		f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
		mensaje = f.read()
		f.close()
		url = base64.b64decode(mensaje)
		x = url.split('-')

		del idsGrupos[:]
		del nameMateria[:]

		con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
		cur = con.cursor()

		docentes = cur.execute("SELECT PA.MT_CLAVE, PA.MT_NOMBRE, ME.DO_APATERNO, ME.DO_AMATERNO, ME.DO_NOMBRE, RE.GR_CLAVE, RE.GR_GRUPO FROM MATERIA PA JOIN GRUPO RE ON PA.MT_CLAVE = RE.MT_CLAVE JOIN DOCENTE ME ON ME.DO_CLAVE = RE.DO_CLAVE WHERE ME.DO_CLAVE = :1 AND RE.CE_CLAVE = :2",(str(x1[0]), str(idsCiclo[int(self.ciclo_escolarcbx.current())]))).fetchall()

		for alumno in docentes:
			claveGrupo.append(str(alumno[5]))
			idsGrupos.append(str(alumno[0]))
			nameMateria.append(str(alumno[1])+' - '+str(alumno[6]))

		s = docentes
		
		if str(s) != '[]':
			self.ciclo_gruposcbx.set(" ")
			self.ciclo_escolarcbx['values']=nameCiclo
			self.ciclo_escolarcbx.config(state='readonly')
			self.ciclo_escolarcbx.current(0)
			self.ciclo_gruposcbx['values']=nameMateria
			self.ciclo_gruposcbx.config(state='readonly')
			
			
		else:	
			
			self.ciclo_gruposcbx.set(" ")
			s = []
			s.append(str(' '))
			self.ciclo_gruposcbx['values']=s
			self.ciclo_gruposcbx.config(state='readonly')
			self.ciclo_escolarcbx['values']=nameCiclo
			self.ciclo_escolarcbx.config(state='readonly')
			

		cur.close()
		con.close()

        self.geometry("1800x752+220+100")
        self.title("Asistencia De Alumnos")
        self.resizable(False,False)
	x = []
	
	try:
		f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
		mensaje = f.read()
		f.close()
		url = base64.b64decode(mensaje)
		x = url.split('-')
		con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
		cur = con.cursor()
		fecha = cur.execute("SELECT TO_CHAR(SYSDATE, 'DD-MM-YYYY') FROM DUAL").fetchall()
		x = str(fecha[0][0]).split('-')
		
    	except:
        	tkMessageBox.showerror("Error","Fallo la conexion de DB!!!",icon='warning')

    	del claveGrupo[:]	
        # Ventanas
        self.top = tk.Frame(self, height=150, bg='#05004e')
        self.top.pack(fill=X)
        self.botonFrame = tk.Frame(self, height=600, bg='#ffedc6')
        self.botonFrame.pack(fill=X)
	
        # Encabezado, imagen y fecha
        self.top_image = tk.PhotoImage(file='icons/uaz.png')
        self.top_image_lbl = tk.Label(self.top, image=self.top_image, bg="#05004e")
        self.top_image_lbl.place(x=10, y=10)
        self.encabezado = tk.Label(self.top, text='REPORTES DE ASISTENCIAS ESCOLARES', font='arial 30 bold', fg='white', bg="#05004e")
        self.encabezado.place(x=400, y=40)

	panel_consultas = tk.LabelFrame(self.botonFrame,width=440,height=175,text="CONSULTA DE ASISTENCIAS",bg='#ffedc6', font='arial 12 bold')
        panel_consultas.place(x=20, y=20)

	#FECHA
	self.fecha = tk.Label(panel_consultas,text="FECHA:", font='arial 12 bold', bg="#ffedc6", fg="black")
        self.fecha.grid(row=0,column=0,padx=20,pady=20) 
	dias = []
        self.dia = StringVar()
        for i in range(1, 32):
            dias.append(i)
        self.comboBox1 = ttk.Combobox(panel_consultas, width=5, textvariable=self.dia, values=(dias), state='readonly')
        self.comboBox1.grid(row=0,column=1,padx=20,pady=20) 
	self.comboBox1.current(int(x[0])-1)
        meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
      	self.mes = StringVar()
        self.comboBox2 = ttk.Combobox(panel_consultas, width=10, textvariable=self.mes, values=(meses), state='readonly')
        self.comboBox2.grid(row=0,column=2,padx=20,pady=20) 
	self.comboBox2.current(int(x[1])-1)
        anios = []
        self.anio = StringVar()
        x2 = datetime.datetime.now()
        for i in range(1949, int(x[2])):
            anios.append(i+1)
        self.comboBox3 = ttk.Combobox(panel_consultas, width=5, textvariable=self.anio, values=(anios), state='readonly')
        self.comboBox3.grid(row=0,column=3,padx=20,pady=20) 
	self.comboBox3.current(int(x[2])-1950)
		
	self.CE = tk.Label(panel_consultas,text="CE:", font='arial 12 bold', bg="#ffedc6", fg="black")
        self.CE.grid(row=0,column=4,padx=20,pady=20) 
	del nameCiclo[:]
	f = open (os.getcwd()+'/auxHuella/docente.uaz','r')
	mensaje = f.read()
	x = mensaje.split('+')
	f.close()
	try:
		f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
		mensaje = f.read()
		f.close()
		url = base64.b64decode(mensaje)
		x = url.split('-')
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
	
      	self.gr = StringVar()
        self.ciclo_escolarcbx = ttk.Combobox(panel_consultas, width=12, textvariable=self.gr, values=(nameCiclo), state='readonly')
        self.ciclo_escolarcbx.grid(row=0,column=5,padx=20,pady=20) 
	self.ciclo_escolarcbx.current(0)
	self.ciclo_escolarcbx.bind("<<ComboboxSelected>>", comb1_selected)
	
	self.GRUPO = tk.Label(panel_consultas,text="GRUPO:", font='arial 12 bold', bg="#ffedc6", fg="black")
        self.GRUPO.grid(row=0,column=6,padx=20,pady=20) 

	grs = [""]

      	self.gr = StringVar()
        self.ciclo_gruposcbx = ttk.Combobox(panel_consultas, width=55, textvariable=self.gr, values=(grs), state='readonly')
        self.ciclo_gruposcbx.grid(row=0,column=7,padx=20,pady=20) 
	self.ciclo_gruposcbx.current(0)
	
        self.btn4 = tk.Button(panel_consultas,text="CONSULTAR",font='fixedsys 12 bold', foreground="#000000", background="#fcf9ea",command=self.HistorialAsistencias)
        self.btn4.grid(row=0,column=8,padx=20,pady=20) 

	self.btnJustificar = tk.Button(self.botonFrame,text="JUSTIFICAR ASISTENCIA ",font='fixedsys 12 bold', foreground="#000000", background="#fcf9ea",command=self.Justificar)
	self.btnJustificar['state'] = 'disabled'
        self.btnJustificar.place(x=1450, y=150)
	self.lbl_REPORTE = tk.Label(self.botonFrame, text='GENERAR REPORTE', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_REPORTE.place(x=1450, y=250)
	

	self.btnGenREporte = tk.Button(self.botonFrame,text="\nREPORTE GLOBAL\nDE ASISTENCIAS\n",font='fixedsys 13 bold', foreground="#000000", background="#fcf9ea",command=self.GenerarReporte)
        self.btnGenREporte.place(x=1480, y=300)
	self.btnGenREporte['state'] = 'normal'

	self.btnSalir = tk.Button(self.botonFrame,text="\nSALIR\n",font='fixedsys 13 bold', foreground="#000000", background="#fcf9ea",command=self.SalirVentana)
        self.btnSalir.place(x=1480, y=490)
        #NumeroPuerto
        self.tree = ttk.Treeview(self.botonFrame, height = 24)
        self.tree.place(x=0, y=150)
	self.tree["columns"]=("1","2","3","4","5","6")
        self.tree.heading('#0', text = 'MATRÍCULA',anchor = CENTER)
	self.tree.heading('1', text = 'NOMBRE (S)',anchor = CENTER)
        self.tree.heading('2', text = 'APELLIDO P.', anchor = CENTER)
	self.tree.heading('3', text = 'APELLIDO M.', anchor = CENTER)
	self.tree.heading('4', text = 'HORA DE ENTRADA', anchor = CENTER)
	self.tree.heading('5', text = 'HORA DE SALIDA', anchor = CENTER)
	self.tree.heading('6', text = 'ASISTENCIA', anchor = CENTER)
	self.tree.bind('<ButtonRelease-1>', selectItem)
    def GenerarReporte(self):
	
	
	if self.matricula != "":
		try:
			f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
			mensaje = f.read()
			f.close()
			url = base64.b64decode(mensaje)
			x = url.split('-')
			con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
			cur = con.cursor()
			HISTORIALES = ['SIN DATOS','SIN DATOS','SIN DATOS','SIN DATOS','SIN DATOS','SIN DATOS']
			HISTORIALES = cur.execute("SELECT AL_MATRICULA, AA_CONSECUTIVO, TO_CHAR(FECHA_ENTRADA,'DD/MM/YYYY HH24:MI:SS') , TO_CHAR(FECHA_SALIDA,'DD/MM/YYYY HH24:MI:SS'), RETARDO, JUSTIFICACION FROM ASISTENCIA WHERE CE_CLAVE = '"+self.cicloE+"' AND AL_MATRICULA = '"+self.matricula+"' AND GR_CLAVE = '"+self.cGrupo+"'").fetchall()	

			RANGO_CE = cur.execute("SELECT TO_CHAR(CE_FECHAINI, 'DD/MM/YY'), TO_CHAR(CE_FECHATER, 'DD/MM/YY') FROM CICLO_ESCOLAR WHERE CE_CLAVE='"+self.cicloE+"'").fetchall()

			
			RETARDOS_PARA_AISTENCIA = cur.execute("SELECT GH_TOTAL_RETARDO_ASISTENCIA FROM GRUPO_HORARIO WHERE CE_CLAVE = '"+self.cicloE+"' AND GR_CLAVE = '"+self.cGrupo+"'").fetchall()
			RPA = 0
			if RETARDOS_PARA_AISTENCIA[0][0] != None:
				RPA = RETARDOS_PARA_AISTENCIA[0][0]
			
			
			
		
			ASISTENCIAS = cur.execute("SELECT A.AL_MATRICULA , COUNT(*) FROM ALUMNO A JOIN ASISTENCIA AC ON A.AL_MATRICULA = AC.AL_MATRICULA WHERE AC.CE_CLAVE = '"+self.cicloE+"'  AND AC.GR_CLAVE = '"+self.cGrupo+"' AND  A.AL_MATRICULA = '"+self.matricula+"' AND AC.JUSTIFICACION IS NULL AND AC.RETARDO IS NULL AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0][0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[0][1])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0][0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[0][1])+"', 'DD/MM/YY') GROUP BY A.AL_MATRICULA").fetchall()

			JUSTIFICACIONES = cur.execute("SELECT A.AL_MATRICULA , COUNT(*) FROM ALUMNO A JOIN ASISTENCIA AC ON A.AL_MATRICULA = AC.AL_MATRICULA WHERE AC.CE_CLAVE = '"+self.cicloE+"'  AND AC.GR_CLAVE = '"+self.cGrupo+"' AND  A.AL_MATRICULA = '"+self.matricula+"' AND AC.JUSTIFICACION IS NOT NULL AND AC.RETARDO IS NULL AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0][0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[0][1])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0][0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[0][1])+"', 'DD/MM/YY') GROUP BY A.AL_MATRICULA").fetchall()

			RETARDOS = cur.execute("SELECT A.AL_MATRICULA , COUNT(*) FROM ALUMNO A JOIN ASISTENCIA AC ON A.AL_MATRICULA = AC.AL_MATRICULA WHERE AC.CE_CLAVE = '"+self.cicloE+"'  AND AC.GR_CLAVE = '"+self.cGrupo+"' AND  A.AL_MATRICULA = '"+self.matricula+"' AND AC.RETARDO IS NOT NULL AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0][0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[0][1])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0][0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[0][1])+"', 'DD/MM/YY') GROUP BY A.AL_MATRICULA").fetchall()
			TOTAL_ASISTENCIAS = 0
			TOTAL_JUSTIFICACIONES = 0
			TOTAL_RETARDOS = 0
			if len(ASISTENCIAS)>0:
				TOTAL_ASISTENCIAS = int(ASISTENCIAS[0][1])
			else:
				TOTAL_ASISTENCIAS = 0
			if len(JUSTIFICACIONES)>0:
				TOTAL_JUSTIFICACIONES = int(JUSTIFICACIONES[0][1])
			else:
				TOTAL_JUSTIFICACIONES = 0
			if len(RETARDOS)>0:
				TOTAL_RETARDOS = int(RETARDOS[0][1])
			else:
				TOTAL_RETARDOS = 0
			NOMBRE = cur.execute("SELECT AL_NOMBRE, AL_APATERNO, AL_AMATERNO FROM ALUMNO WHERE AL_MATRICULA = '"+self.matricula+"'").fetchall()
			NOMBRE_ALUMNO = ""

			CORREO = cur.execute("SELECT AL_EMAIL FROM ALUMNO WHERE AL_MATRICULA = '"+self.matricula+"'").fetchall()
			CORREO_ALUMNO = CORREO[0][0]

			DOCENTE = cur.execute("SELECT DO.DO_NOMBRE, DO.DO_APATERNO, DO.DO_AMATERNO FROM DOCENTE DO JOIN GRUPO GR ON DO.DO_CLAVE = GR.DO_CLAVE WHERE GR.CE_CLAVE = '"+self.cicloE+"' AND GR.GR_CLAVE = '"+self.cGrupo+"'").fetchall()
			NOMBRE_DOCENTE = ""

			PROGRAMA = cur.execute("SELECT PE.PL_NOMBRE FROM PLAN_ESTUDIO PE JOIN GRUPO GR ON GR.PL_CLAVE = PE.PL_CLAVE WHERE GR.CE_CLAVE = '"+self.cicloE+"' AND GR.GR_CLAVE = '"+self.cGrupo+"'").fetchall()
			PROGRAMA_ACADEMICO = PROGRAMA[0][0]

			MATERIA = cur.execute("SELECT MT.MT_NOMBRE FROM MATERIA MT JOIN  GRUPO GR ON MT.MT_CLAVE = GR.MT_CLAVE WHERE GR.CE_CLAVE = '"+self.cicloE+"' AND GR.GR_CLAVE = '"+self.cGrupo+"'").fetchall()
			NOMBRE_MATERIA = MATERIA[0][0]

			CEF = cur.execute("SELECT CE_DESCRIPCION FROM CICLO_ESCOLAR WHERE CE_CLAVE = '"+self.cicloE+"'").fetchall()
			CICLO_ESCOLAR = CEF[0][0]

			SES = cur.execute("SELECT GR_TOTAL_SESIONES FROM GRUPO WHERE CE_CLAVE = '"+self.cicloE+"' AND GR_CLAVE = '"+self.cGrupo+"'").fetchall()
			
			if(SES[0][0]!=None):
				SESIONES = SES[0][0]
			else:
				SESIONES = 0

			if(NOMBRE[0][2]!=None):
				NOMBRE_ALUMNO = NOMBRE[0][0]+" "+NOMBRE[0][1]+" "+NOMBRE[0][2]
			else:
				NOMBRE_ALUMNO = NOMBRE[0][0]+" "+NOMBRE[0][1]
			
			if(DOCENTE[0][2]!=None):
				NOMBRE_DOCENTE = DOCENTE[0][0]+" "+DOCENTE[0][1]+" "+DOCENTE[0][2]
			else:
				NOMBRE_DOCENTE = DOCENTE[0][0]+" "+DOCENTE[0][1]
			reportesasistencia.generarReporteAlumno(str(self.matricula), str(NOMBRE_ALUMNO), str(NOMBRE_DOCENTE), str(NOMBRE_MATERIA), str(CICLO_ESCOLAR), int(TOTAL_ASISTENCIAS) + int(TOTAL_JUSTIFICACIONES), str(PROGRAMA_ACADEMICO), int(TOTAL_RETARDOS), int(SESIONES), int(RPA), HISTORIALES)
			cur.close()
			con.commit()
			con.close()
			reportes = reportviewsend.reportes(CORREO_ALUMNO,NOMBRE_ALUMNO,NOMBRE_MATERIA)
		except:
			tkMessageBox.showerror("Error","SE PRODUJO UN ERROR, NO SE GENERO EL REPORTE",icon='warning')

    def Justificar(self):
	fd = commands.getoutput('java -classpath ./ojdbcfull/ojdbc6.jar:./ojdbcfull/ojdbc5.jar:./ojdbcfull/ons.jar:./ojdbcfull/orai18n.jar:./ojdbcfull/simplefan.jar:./ojdbcfull/ucp.jar:./ojdbcfull/xdb6.jar:. JustificarAsistencia')
	if(fd != ""):
		tkMessageBox.showerror("ERROR","NO SE PUEDE JUSTIFICAR ERROR DB",icon='warning')
	else:	
		RES = IdentificacionUSUARIOS.user()
		if RES != 'LD':
			if RES == self.matricula:
				try:
					f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
					mensaje = f.read()
					f.close()
					url = base64.b64decode(mensaje)
					x = url.split('-')
					con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
					cur = con.cursor()
					fecha = cur.execute("SELECT SYSDATE FROM DUAL").fetchall()
					fecha1 = cur.execute("SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD') FROM DUAL").fetchall()

					fechaJustificacion = datetime.datetime(int(self.comboBox3.get()), int(self.comboBox2.current())+1, int(self.comboBox1.get()))
					fechaFInal = str(fechaJustificacion).split(' ')
					
					maxAsistencia = cur.execute("SELECT MAX (AA_CONSECUTIVO) FROM ASISTENCIA WHERE CE_CLAVE = '" + self.cicloE + "' AND AL_MATRICULA='" + self.matricula+"' AND GR_CLAVE='"+self.cGrupo+"'").fetchall()
					if maxAsistencia[0][0] == None:
						statement = 'INSERT INTO ASISTENCIA(CE_CLAVE, AL_MATRICULA, GR_CLAVE, AA_CONSECUTIVO, FECHA_ENTRADA, FECHA_SALIDA, JUSTIFICACION) VALUES(:1,:2,:3,:4,:5,:6,:7)'
						cur.execute(statement, (self.cicloE, self.matricula, self.cGrupo, 1, fechaJustificacion, fechaJustificacion, 1))
					else:
						statement = 'INSERT INTO ASISTENCIA(CE_CLAVE, AL_MATRICULA, GR_CLAVE, AA_CONSECUTIVO, FECHA_ENTRADA, FECHA_SALIDA, JUSTIFICACION) VALUES(:1,:2,:3,:4,:5,:6,:7)'
						cur.execute(statement, (self.cicloE, self.matricula, self.cGrupo, int(maxAsistencia[0][0])+1, fechaJustificacion, fechaJustificacion, 1))
					con.commit()
					for i in self.tree.get_children():
				    		self.tree.delete(i)
					alumnos = cur.execute("SELECT AL.AL_MATRICULA, AL.AL_NOMBRE, AL.AL_APATERNO, AL.AL_AMATERNO, TO_CHAR(ASIS.FECHA_ENTRADA, 'yyyy-mm-dd HH24:MI:SS'), TO_CHAR(ASIS.FECHA_SALIDA, 'yyyy-mm-dd HH24:MI:SS'), ASIS.RETARDO, ASIS.JUSTIFICACION FROM GRUPO GR JOIN  ASIGNATURA ASIG ON GR.GR_CLAVE = ASIG.GR_CLAVE JOIN  ALUMNO AL ON AL.AL_MATRICULA = ASIG.AL_MATRICULA LEFT OUTER JOIN  ASISTENCIA ASIS ON ASIS.AL_MATRICULA = AL.AL_MATRICULA AND TO_CHAR(ASIS.FECHA_ENTRADA, 'yyyy-mm-dd') >= '"+str(fechaFInal[0])+"' AND TO_CHAR(ASIS.FECHA_SALIDA, 'yyyy-mm-dd') <= '"+str(fechaFInal[0])+"' WHERE ASIG.CE_CLAVE = '"+str(idsCiclo[int(self.ciclo_escolarcbx.current())])+"' AND GR.GR_CLAVE = '"+str(claveGrupo[int(self.ciclo_gruposcbx.current())])+"' ORDER BY AL.AL_APATERNO").fetchall()
					for alumno in alumnos:
						if(alumno[4]==None or alumno[5]==None):
							self.tree.insert('', 'end', text=str(alumno[0]),values=(str(alumno[1]),str(alumno[2]),str(alumno[3]),str(''),str(''),str('NO ASISTIO')))
						else:
							if(alumno[6]==None):
								if(alumno[7]!=None):
									self.tree.insert('', 'end', text=str(alumno[0]),values=(str(alumno[1]),str(alumno[2]),str(alumno[3]),str(alumno[4]),str(alumno[5]),str('JUSTIFICADO')))
								else:
									self.tree.insert('', 'end', text=str(alumno[0]),values=(str(alumno[1]),str(alumno[2]),str(alumno[3]),str(alumno[4]),str(alumno[5]),str('ASISTIO')))
							else:
								self.tree.insert('', 'end', text=str(alumno[0]),values=(str(alumno[1]),str(alumno[2]),str(alumno[3]),str(alumno[4]),str(alumno[5]),str('RETARDO')))
					cur.close()
					con.commit()
					con.close()
					tkMessageBox.showinfo("ÉXITO","SE JUSTIFICO LA FALTA",icon='info')	
				except:
					tkMessageBox.showerror("Error","Fallo la conexion de DB!!!",icon='warning')
			else:
				tkMessageBox.showerror("Error","NO SE PUDO JUSTIFICAR LA ASISTENCIA DEL ALUMNO\nNO HAY HUELLA ASOCIADA",icon='warning')
		else:
			tkMessageBox.showerror("Error","CONECTE EL LECTOR",icon='warning')
	
    def HistorialAsistencias(self):
	if(self.ciclo_escolarcbx.get().replace(' ', '')!="" and self.ciclo_gruposcbx.get().replace(' ', '')!=""):
		fechaJustificacion = datetime.datetime(int(self.comboBox3.get()), int(self.comboBox2.current())+1, int(self.comboBox1.get()))
		fechaFInal = str(fechaJustificacion).split(' ')
		
		for i in self.tree.get_children():
	    		self.tree.delete(i)
		try:
			# archivo-entrada.py
			f = open (os.getcwd()+"/auxHuella/conexiondb.uaz",'r')
			mensaje = f.read()
			f.close()
			url = base64.b64decode(mensaje)
			x = url.split('-')
			con =  cx_Oracle.connect(x[0]+'/'+x[1]+'@'+x[2]+'/'+x[3])
			cur = con.cursor()
			fecha = cur.execute("SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD') FROM DUAL").fetchall()
			alumnos = cur.execute("SELECT AL.AL_MATRICULA, AL.AL_NOMBRE, AL.AL_APATERNO, AL.AL_AMATERNO, TO_CHAR(ASIS.FECHA_ENTRADA, 'yyyy-mm-dd HH24:MI:SS'), TO_CHAR(ASIS.FECHA_SALIDA, 'yyyy-mm-dd HH24:MI:SS'), ASIS.RETARDO, ASIS.JUSTIFICACION FROM GRUPO GR JOIN  ASIGNATURA ASIG ON GR.GR_CLAVE = ASIG.GR_CLAVE JOIN  ALUMNO AL ON AL.AL_MATRICULA = ASIG.AL_MATRICULA LEFT OUTER JOIN  ASISTENCIA ASIS ON ASIS.AL_MATRICULA = AL.AL_MATRICULA AND TO_CHAR(ASIS.FECHA_ENTRADA, 'yyyy-mm-dd') >= '"+str(fechaFInal[0])+"' AND TO_CHAR(ASIS.FECHA_SALIDA, 'yyyy-mm-dd') <= '"+str(fechaFInal[0])+"' WHERE ASIG.CE_CLAVE = '"+str(idsCiclo[int(self.ciclo_escolarcbx.current())])+"' AND GR.GR_CLAVE = '"+str(claveGrupo[int(self.ciclo_gruposcbx.current())])+"' ORDER BY AL.AL_APATERNO").fetchall()
	    		for alumno in alumnos:
				if(alumno[4]==None or alumno[5]==None):
					if(alumno[3]==None):
						self.tree.insert('', 'end', text=str(alumno[0]),values=(str(alumno[1]),str(alumno[2]),'',str(''),str(''),str('NO ASISTIO')))
					else:
						self.tree.insert('', 'end', text=str(alumno[0]),values=(str(alumno[1]),str(alumno[2]),str(alumno[3]),str(''),str(''),str('NO ASISTIO')))
				else:
					if(alumno[6]==None):
						if(alumno[7]!=None):
							if(alumno[3]==None):
								self.tree.insert('', 'end', text=str(alumno[0]),values=(str(alumno[1]),str(alumno[2]),'',str(alumno[4]),str(alumno[5]),str('JUSTIFICADO')))
							else:
								self.tree.insert('', 'end', text=str(alumno[0]),values=(str(alumno[1]),str(alumno[2]),str(alumno[3]),str(alumno[4]),str(alumno[5]),str('JUSTIFICADO')))
						else:
							if(alumno[3]==None):
								self.tree.insert('', 'end', text=str(alumno[0]),values=(str(alumno[1]),str(alumno[2]),'',str(alumno[4]),str(alumno[5]),str('ASISTIO')))
							else:
								self.tree.insert('', 'end', text=str(alumno[0]),values=(str(alumno[1]),str(alumno[2]),str(alumno[3]),str(alumno[4]),str(alumno[5]),str('ASISTIO')))
					
					else:
						if(alumno[3]==None):
							self.tree.insert('', 'end', text=str(alumno[0]),values=(str(alumno[1]),str(alumno[2]),'',str(alumno[4]),str(alumno[5]),str('RETARDO')))
						else:
							self.tree.insert('', 'end', text=str(alumno[0]),values=(str(alumno[1]),str(alumno[2]),str(alumno[3]),str(alumno[4]),str(alumno[5]),str('RETARDO')))
			cur.close()
			con.commit()
			con.close()			
	    	except:
			tkMessageBox.showerror("Error","Fallo la conexion de DB!!!",icon='warning')
	else:
		self.btnGenREporte['state'] = 'disabled'
		self.matricula = ""
		self.cicloE = ""
		self.cGrupo = ""
    def SalirVentana(self):
	self.top.destroy()
        self.botonFrame.destroy()
	self.destroy()
