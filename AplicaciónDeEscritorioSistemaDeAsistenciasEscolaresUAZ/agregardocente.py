# -*- coding: utf-8 -*-
import Tkinter, ttk, tkMessageBox, time, pyfprint, datetime, os, base64, commands, cx_Oracle
from Tkinter import *
import Tkinter as tk
from ttk import *
from os import remove
import validacioncampos
from ModeladoGMM import ModelarGMM
import removeSilence
idgescolar = []
nomgescolar = []
class AgregarDocente(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
	def comb1_selected(*args):
		NoAudios = []
		del NoAudios [:]
		
		for i in range(1, int(self.comboNoAudios.get().replace(" ", ""))+1):
		    NoAudios.append(i)
		self.comboAudios['values']=NoAudios
		self.comboAudios.current(0)

	for name in os.listdir(os.getcwd()+"/MuestrasDeVoz/MuestrasAudio/"):
		remove(os.getcwd() + "/MuestrasDeVoz/MuestrasAudio/" + name)

        self.geometry("1300x830+400+10")
        self.title("REGISTRO DE DOCENTE")
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
        self.encabezado = tk.Label(self.top, text='REGISTRO DE DOCENTES - UAZ', font='arial 20 bold', fg='white', bg="#05004e")
        self.encabezado.place(x=390, y=30)

        #ETIQUETAS Y ENTRADAS
	#DO_CLAVE    NOT NULL CHAR(4)
	self.lbl_clave = tk.Label(self.botonFrame, text='(*) Clave:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_clave.place(x=40, y=40)
        self.ent_clave = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
        self.ent_clave.place(x=210, y=40)   
   
	#GE_CLAVE    NOT NULL NUMBER(38) 
	self.lbl_gescolar = tk.Label(self.botonFrame, text='(*) G. Escolar:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_gescolar.place(x=40, y=80)
        try:
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
        self.combo_grupos.place(x=210, y=80)
	self.combo_grupos.current(0)
	 
	#DO_APATERNO NOT NULL VARCHAR2(35) 
	self.lbl_apaterno = tk.Label(self.botonFrame, text='(*) A. Paterno:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_apaterno.place(x=40, y=120)
        self.ent_apaterno = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
        self.ent_apaterno.place(x=210, y=120)

	#DO_AMATERNO          VARCHAR2(35) 
	self.lbl_amaterno = tk.Label(self.botonFrame, text='A. Materno:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_amaterno.place(x=40, y=160)
        self.ent_amaterno = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
        self.ent_amaterno.place(x=210, y=160)
	
	#DO_NOMBRE   NOT NULL VARCHAR2(35) 
	self.lbl_anombre = tk.Label(self.botonFrame, text='(*) Nombre:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_anombre.place(x=40, y=200)
        self.ent_anombre = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
        self.ent_anombre.place(x=210, y=200)
	
	#DO_FECHANAC          DATE   
	self.lbl_fecha = tk.Label(self.botonFrame, text='Nacimiento:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_fecha.place(x=40, y=240)
        self.dias = []
        self.dia = StringVar()
        for i in range(1, 32):
            self.dias.append(i)
        self.comboBox1 = ttk.Combobox(self.botonFrame, width=5, textvariable=self.dia, values=(self.dias), state='readonly')
        self.comboBox1.place(x=210, y=240)
	self.comboBox1.current(30)
        self.meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
      	self.mes = StringVar()
        self.comboBox2 = ttk.Combobox(self.botonFrame, width=10, textvariable=self.mes, values=(self.meses), state='readonly')
        self.comboBox2.place(x=290, y=240)
	self.comboBox2.current(1)
        self.anios = []
        self.anio = StringVar()
        x = datetime.datetime.now()
        for i in range(1949, x.year):
            self.anios.append(i+1)
        self.comboBox3 = ttk.Combobox(self.botonFrame, width=5, textvariable=self.anio, values=(self.anios), state='readonly')
        self.comboBox3.place(x=425, y=240)
	self.comboBox3.current(35) 
	      
	#DO_CALLE             VARCHAR2(50) 
	self.lbl_calle = tk.Label(self.botonFrame, text='Calle:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_calle.place(x=40, y=280)
        self.ent_calle = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
        self.ent_calle.place(x=210, y=280)

	#DO_COLONIA           VARCHAR2(50) 
	self.lbl_colonia = tk.Label(self.botonFrame, text='Colonia:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_colonia.place(x=40, y=320)
        self.ent_colonia = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
        self.ent_colonia.place(x=210, y=320)
	
	#DO_CP                CHAR(5)     
	self.lbl_cp = tk.Label(self.botonFrame, text='C.P:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_cp.place(x=40, y=360)
        self.ent_cp = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
        self.ent_cp.place(x=210, y=360)
	
	#DO_TELEFONO          VARCHAR2(20) 
	self.lbl_telefono = tk.Label(self.botonFrame, text='Teléfono:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_telefono.place(x=520, y=40)
        self.ent_telefono = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
        self.ent_telefono.place(x=680, y=40)

	#DO_TELCELL           VARCHAR2(20) 
	self.lbl_telefonoc = tk.Label(self.botonFrame, text='Teléfono C:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_telefonoc.place(x=520, y=85)
        self.ent_telefonoc = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
        self.ent_telefonoc.place(x=680, y=85)

	#DO_EMAIL             VARCHAR2(50) 
	self.lbl_email = tk.Label(self.botonFrame, text='E-Mail:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_email.place(x=520, y=125)
        self.ent_email = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
        self.ent_email.place(x=680, y=125)

	#DO_GENERO   NOT NULL NUMBER(38)   
	self.lbl_genero = tk.Label(self.botonFrame, text='(*) Genéro:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_genero.place(x=520, y=160)
	self.gender = IntVar(None, 1)
        self.rhombre = tk.Radiobutton(self.botonFrame, text='Hombre    ', value=1, var=self.gender, bg='#ffedc6', font='arial 10 bold')
        self.rhombre.place(x=680, y=165)
        self.rmujer = tk.Radiobutton(self.botonFrame, text='Mujer       ', value=2, var=self.gender, bg='#ffedc6', font='arial 10 bold')
        self.rmujer.place(x=820, y=165)

	#DO_TITULO            CHAR(5)   
	self.lbl_titulo = tk.Label(self.botonFrame, text='Título:', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_titulo.place(x=520, y=205)
        self.ent_titulo = tk.Entry(self.botonFrame, width=31, bd=3, font='arial 10 bold')
        self.ent_titulo.place(x=680, y=205) 
  
	#AL_HUELLA                   BLOB
        self.lbl_huella = tk.Label(self.botonFrame, text='Estado De Captura De Huella', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_huella.place(x=20, y=400)

	s = ttk.Style()
	s.theme_use('clam')
	s.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
        self.progbar = ttk.Progressbar(self.botonFrame, style="green.Horizontal.TProgressbar", orient=HORIZONTAL, length=200, mode = 'determinate')
        self.progbar.place(x=90, y=450)

	self.huellaOri = PhotoImage(file='icons/huella.png')
        self.huellaOri_lbl = tk.Label(self.botonFrame, image=self.huellaOri, bg="#ffedc6")
        self.huellaOri_lbl.place(x=120, y=490)

	self.lbl_voz = tk.Label(self.botonFrame, text='Estado De Captura De Muestras De Voz', font='calibri 12 bold', fg='black', bg='#ffedc6')
        self.lbl_voz.place(x=440, y=400)
	self.vozOri = PhotoImage(file='icons/voz.png')
        self.vozOri_lbl = tk.Label(self.botonFrame, image=self.vozOri, bg="#ffedc6")
        self.vozOri_lbl.place(x=320, y=510)
	#NOTA
        self.lbl_NOTA = tk.Label(self.botonFrame, text='(*) DATOS\nOBLIGATORIOS', font='calibri 12 bold', fg='red', bg='#ffedc6')
        self.lbl_NOTA.place(x=1040, y=40)

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
	

	"""self.lbl_Mvoz1 = tk.Label(self.botonFrame, text='Muestra 1', font='calibri 10 bold', fg='black', bg='#ffedc6')
        self.lbl_Mvoz1.place(x=400, y=450)
	self.barMVoz1 = ttk.Progressbar(self.botonFrame, style="green.Horizontal.TProgressbar", orient=VERTICAL, length=140, mode = 'determinate')
        self.barMVoz1.place(x=435, y=480)
	self.botonGrabar1 = tk.Button(self.botonFrame,text="Grabar 1", command=self.grabarAudio1, font='arial 10 bold')
	self.botonGrabar1.configure(compound=LEFT)
        self.botonGrabar1.place(x=400,y=630)
	
	self.lbl_Mvoz2 = tk.Label(self.botonFrame, text='Muestra 2', font='calibri 10 bold', fg='black', bg='#ffedc6')
        self.lbl_Mvoz2.place(x=520, y=450)
	self.barMVoz2 = ttk.Progressbar(self.botonFrame, style="green.Horizontal.TProgressbar", orient=VERTICAL, length=140, mode = 'determinate')
        self.barMVoz2.place(x=555, y=480)
	self.botonGrabar2 = tk.Button(self.botonFrame,text="Grabar 2", command=self.grabarAudio2, font='arial 10 bold')
	self.botonGrabar2.configure(compound=LEFT)
        self.botonGrabar2.place(x=520,y=630)

	self.lbl_Mvoz3 = tk.Label(self.botonFrame, text='Muestra 3', font='calibri 10 bold', fg='black', bg='#ffedc6')
        self.lbl_Mvoz3.place(x=640, y=450)
	self.barMVoz3 = ttk.Progressbar(self.botonFrame, style="green.Horizontal.TProgressbar", orient=VERTICAL, length=140, mode = 'determinate')
        self.barMVoz3.place(x=675, y=480)
	self.botonGrabar3 = tk.Button(self.botonFrame,text="Grabar 3", command=self.grabarAudio3, font='arial 10 bold')
	self.botonGrabar3.configure(compound=LEFT)
        self.botonGrabar3.place(x=640,y=630)

	self.lbl_Mvoz4 = tk.Label(self.botonFrame, text='Muestra 4', font='calibri 10 bold', fg='black', bg='#ffedc6')
        self.lbl_Mvoz4.place(x=760, y=450)
	self.barMVoz4 = ttk.Progressbar(self.botonFrame, style="green.Horizontal.TProgressbar", orient=VERTICAL, length=140, mode = 'determinate')
        self.barMVoz4.place(x=795, y=480)
	self.botonGrabar4 = tk.Button(self.botonFrame,text="Grabar 4", command=self.grabarAudio4, font='arial 10 bold')
	self.botonGrabar4.configure(compound=LEFT)
        self.botonGrabar4.place(x=760,y=630)

	self.lbl_Mvoz5 = tk.Label(self.botonFrame, text='Muestra 5', font='calibri 10 bold', fg='black', bg='#ffedc6')
        self.lbl_Mvoz5.place(x=880, y=450)
	self.barMVoz5 = ttk.Progressbar(self.botonFrame, style="green.Horizontal.TProgressbar", orient=VERTICAL, length=140, mode = 'determinate')
        self.barMVoz5.place(x=915, y=480)
	self.botonGrabar5 = tk.Button(self.botonFrame,text="Grabar 5", command=self.grabarAudio5, font='arial 10 bold')
	self.botonGrabar5.configure(compound=LEFT)
        self.botonGrabar5.place(x=880,y=630)"""
        
        #BOTON DE REGISTRO
	#self.icon1 = tk.PhotoImage(file='icons/estudiante.png')
        self.botonPlantillaHuella = tk.Button(self.botonFrame,command=self.HuellaCaptura,text="Generar Plantilla De Huella", font='arial 14 bold')
	self.botonPlantillaHuella.configure(compound=LEFT)
        self.botonPlantillaHuella.place(x=20,y=640)
	self.botonPlantillaVoz = tk.Button(self.botonFrame, command=self.ModelarMFCCGMM, text="Generar Plantilla\nDe Voz", font='arial 15 bold')
	self.botonPlantillaVoz.configure(compound=LEFT)
        self.botonPlantillaVoz.place(x=1010,y=580)
	self.botonRegistrar = tk.Button(self.botonFrame,text="REGISTRAR", command=self.addDocente, font='arial 18 bold')
	self.botonRegistrar.configure(compound=LEFT)
        self.botonRegistrar.place(x=1020,y=200)
	self.botonLimpiar = tk.Button(self.botonFrame,text="LIMPIAR\nREGISTROS", command=self.LimpiarRegistros, font='arial 18 bold')
	self.botonLimpiar.configure(compound=LEFT)
        self.botonLimpiar.place(x=1020,y=300)
	self.botonSalir = tk.Button(self.botonFrame,text="      SALIR     ", command=self.Salir, font='arial 18 bold')
	self.botonSalir.configure(compound=LEFT)
        self.botonSalir.place(x=1020,y=440)
        self.lift()

    def grabarAudio1(self):
	self.botonPlantillaHuella['state'] = 'disabled'
	self.botonPlantillaVoz['state'] = 'disabled'
	self.botonRegistrar['state'] = 'disabled'
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
	self.botonPlantillaHuella['state'] = 'normal'
	self.botonPlantillaVoz['state'] = 'normal'
	self.botonRegistrar['state'] = 'normal'

    def LimpiarRegistros(self):
	self.list_box1.delete(0,END)

	for name in os.listdir(os.getcwd()+"/MuestrasDeVoz/MuestrasAudio/"):
		remove(os.getcwd() + "/MuestrasDeVoz/MuestrasAudio/" + name)
	try:
		remove(os.getcwd()+"/auxHuella/datos.uaz")
		remove(os.getcwd()+"/auxHuella/HUELLA/huella"+self.ent_clave.get().replace(" ", ""))	
		remove(os.getcwd()+"/MuestrasDeVoz/ModeloGMM/voz"+self.ent_clave.get().replace(" ", "")+".gmm")
	except:
		self.ent_clave.delete(first=0,last=50)
		self.combo_grupos.current(0)
		self.ent_amaterno.delete(first=0,last=50)
		self.ent_apaterno.delete(first=0,last=50)
		self.ent_anombre.delete(first=0,last=50)
		self.comboBox1.current(30)
		self.comboBox2.current(1)
		self.comboBox3.current(35)
		self.ent_calle.delete(first=0,last=50)
		self.ent_colonia.delete(first=0,last=50)
		self.ent_cp.delete(first=0,last=50)
		self.ent_telefono.delete(first=0,last=50)
		self.ent_telefonoc.delete(first=0,last=50)
		self.ent_email.delete(first=0,last=50)
		self.gender = IntVar(None, 1)
		self.ent_titulo.delete(first=0,last=50)
		self.progbar['value'] = 0
	self.ent_clave.delete(first=0,last=50)
	self.combo_grupos.current(0)
	self.ent_amaterno.delete(first=0,last=50)
	self.ent_apaterno.delete(first=0,last=50)
	self.ent_anombre.delete(first=0,last=50)
	self.comboBox1.current(30)
	self.comboBox2.current(1)
	self.comboBox3.current(35)
	self.ent_calle.delete(first=0,last=50)
	self.ent_colonia.delete(first=0,last=50)
	self.ent_cp.delete(first=0,last=50)
	self.ent_telefono.delete(first=0,last=50)
	self.ent_telefonoc.delete(first=0,last=50)
	self.ent_email.delete(first=0,last=50)
	self.gender = IntVar(None, 1)
	self.ent_titulo.delete(first=0,last=50)
	self.progbar['value'] = 0
	
    def Salir(self):
	self.top.destroy()
        self.botonFrame.destroy()
	self.destroy()

    def ModelarMFCCGMM(self):
	#va una condicion que pregunta si hay en el entry de matricula datos
	if(self.ent_clave.get() != "" and self.ent_apaterno.get() != "" and self.ent_anombre.get() != ""):
		if(validacioncampos.Entero(self.ent_clave.get()) == True and validacioncampos.Nombres(self.ent_apaterno.get()) == True and validacioncampos.Nombres(self.ent_anombre.get()) == True and len(self.ent_clave.get().replace(" ", ""))==4):
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
				resultado = ModelarGMM(self.ent_clave.get().replace(" ", ""),int(self.comboNoAudios.get().replace(" ", "")))
				tkMessageBox.showinfo("ÉXITO","PLANTILLA DE VOZ GENERADA "+resultado,icon='info')
			else:
				tkMessageBox.showerror("ERROR","NO HAY SUFICIENTES MUESTRAS DE AUDIO PARA GENERAR LA PLANTILLA",icon='warning')
		else:
			tkMessageBox.showerror("ERROR","FORMATO DE DATOS INCORRECTO",icon='warning')
	else:
		tkMessageBox.showerror("ERROR","DATOS OBLIGATORIOS SIN COMPLETAR",icon='warning')

    def addDocente(self):
	status = "NULL"
	extranjero = "NULL"
	#validacioncampos.comprobar_fecha(self.anio.get(),self.meses.index(self.mes.get())+1,self.dia.get()) == True and validacioncampos.comprobar_fecha(self.anio1.get(),self.meses1.index(self.mes1.get())+1,self.dia1.get()) == True
        if(self.ent_clave.get() != "" and self.ent_apaterno.get() != "" and self.ent_anombre.get() != "" and self.gender.get() != 0 ):
		if(validacioncampos.Entero(self.ent_clave.get()) == True and validacioncampos.Nombres(self.ent_apaterno.get()) == True and validacioncampos.Nombres(self.ent_anombre.get()) == True and len(self.ent_clave.get().replace(" ", ""))==4):
			mbox = tkMessageBox.askquestion("warning","CONFIRMACIÓN DE CLAVE DOCENTE:"+self.ent_clave.get(),icon="warning")
			if mbox == 'yes':
				if(validacioncampos.comprobar_fecha(int(self.anio.get()),int(self.meses.index(self.mes.get())+1),int(self.dia.get()))):
					x=self.combo_grupos.get()
					y=x.split("-")	
					f = open (os.getcwd()+"/auxHuella/datosDocente.uaz",'w')
					f.write(base64.b64encode(self.ent_clave.get().replace(" ", "") +","+y[0]+","+self.ent_apaterno.get()+","+self.ent_amaterno.get()+","+self.ent_anombre.get()+","+str(self.dia.get()+"/"+self.mes.get()+"/"+self.anio.get())+","+self.ent_calle.get()+","+self.ent_colonia.get()+","+self.ent_cp.get()+","+self.ent_telefono.get()+","+self.ent_telefonoc.get()+","+self.ent_email.get()+","+self.ent_titulo.get()+","+str(self.gender.get())))
					f.close()			

					fd = commands.getoutput('java -classpath ./ojdbcfull/ojdbc6.jar:./ojdbcfull/ojdbc5.jar:./ojdbcfull/ons.jar:./ojdbcfull/orai18n.jar:./ojdbcfull/simplefan.jar:./ojdbcfull/ucp.jar:./ojdbcfull/xdb6.jar:. InsertarDocente')
					if(fd != ""):
						tkMessageBox.showerror("ERROR","No se pudo agregar nada a la base de datos!!!",icon='warning')
					else:
						tkMessageBox.showinfo("ÉXITO","Los Datos Se Almacenaron Correctamente",icon='info')
						for name in os.listdir(os.getcwd()+"/MuestrasDeVoz/MuestrasAudio/"):
							remove(os.getcwd() + "/MuestrasDeVoz/MuestrasAudio/" + name)
						try:
							remove(os.getcwd()+"/auxHuella/datosDocente.uaz")
							remove(os.getcwd()+"/auxHuella/HUELLA/huella"+self.ent_clave.get().replace(" ", ""))	
							remove(os.getcwd()+"/MuestrasDeVoz/ModeloGMM/voz"+self.ent_clave.get().replace(" ", "")+".gmm")
						except:
							self.ent_clave.delete(first=0,last=50)
							self.combo_grupos.current(0)
							self.ent_amaterno.delete(first=0,last=50)
							self.ent_apaterno.delete(first=0,last=50)
							self.ent_anombre.delete(first=0,last=50)
							self.comboBox1.current(30)
							self.comboBox2.current(1)
							self.comboBox3.current(35)
							self.ent_calle.delete(first=0,last=50)
							self.ent_colonia.delete(first=0,last=50)
							self.ent_cp.delete(first=0,last=50)
							self.ent_telefono.delete(first=0,last=50)
							self.ent_telefonoc.delete(first=0,last=50)
							self.ent_email.delete(first=0,last=50)
							self.gender = IntVar(None, 1)
							self.ent_titulo.delete(first=0,last=50)
							self.list_box1.delete(0,END)
							self.progbar['value'] = 0
						self.ent_clave.delete(first=0,last=50)
						self.combo_grupos.current(0)
						self.ent_amaterno.delete(first=0,last=50)
						self.ent_apaterno.delete(first=0,last=50)
						self.ent_anombre.delete(first=0,last=50)
						self.comboBox1.current(30)
						self.comboBox2.current(1)
						self.comboBox3.current(35)
						self.ent_calle.delete(first=0,last=50)
						self.ent_colonia.delete(first=0,last=50)
						self.ent_cp.delete(first=0,last=50)
						self.ent_telefono.delete(first=0,last=50)
						self.ent_telefonoc.delete(first=0,last=50)
						self.ent_email.delete(first=0,last=50)
						self.gender = IntVar(None, 1)
						self.ent_titulo.delete(first=0,last=50)
						self.list_box1.delete(0,END)
						self.progbar['value'] = 0
				else:
					x=self.combo_grupos.get()
					y=x.split("-")	
		  			f = open (os.getcwd()+"/auxHuella/datosDocente.uaz",'w')
					f.write(base64.b64encode(self.ent_clave.get().replace(" ", "") +","+y[0]+","+self.ent_apaterno.get()+","+self.ent_amaterno.get()+","+self.ent_anombre.get()+",NULL,"+self.ent_calle.get()+","+self.ent_colonia.get()+","+self.ent_cp.get()+","+self.ent_telefono.get()+","+self.ent_telefonoc.get()+","+self.ent_email.get()+","+self.ent_titulo.get()+","+str(self.gender.get())))
					f.close()
					fd = commands.getoutput('java -classpath ./ojdbcfull/ojdbc6.jar:./ojdbcfull/ojdbc5.jar:./ojdbcfull/ons.jar:./ojdbcfull/orai18n.jar:./ojdbcfull/simplefan.jar:./ojdbcfull/ucp.jar:./ojdbcfull/xdb6.jar:. InsertarDocente')
					if(fd != ""):
						tkMessageBox.showerror("ERROR","No se pudo agregar nada a la base de datos!!!",icon='warning')
					else:
						tkMessageBox.showinfo("ÉXITO","Los Datos Se Almacenaron Correctamente",icon='info')
						for name in os.listdir(os.getcwd()+"/MuestrasDeVoz/MuestrasAudio/"):
							remove(os.getcwd() + "/MuestrasDeVoz/MuestrasAudio/" + name)
						try:
							remove(os.getcwd()+"/auxHuella/datosDocente.uaz")
							remove(os.getcwd()+"/auxHuella/HUELLA/huella"+self.ent_clave.get().replace(" ", ""))	
							remove(os.getcwd()+"/MuestrasDeVoz/ModeloGMM/voz"+self.ent_clave.get().replace(" ", "")+".gmm")
						except:
							self.ent_clave.delete(first=0,last=50)
							self.combo_grupos.current(0)
							self.ent_amaterno.delete(first=0,last=50)
							self.ent_apaterno.delete(first=0,last=50)
							self.ent_anombre.delete(first=0,last=50)
							self.comboBox1.current(30)
							self.comboBox2.current(1)
							self.comboBox3.current(35)
							self.ent_calle.delete(first=0,last=50)
							self.ent_colonia.delete(first=0,last=50)
							self.ent_cp.delete(first=0,last=50)
							self.ent_telefono.delete(first=0,last=50)
							self.ent_telefonoc.delete(first=0,last=50)
							self.ent_email.delete(first=0,last=50)
							self.gender = IntVar(None, 1)
							self.ent_titulo.delete(first=0,last=50)
							self.list_box1.delete(0,END)
							self.progbar['value'] = 0
						self.ent_clave.delete(first=0,last=50)
						self.combo_grupos.current(0)
						self.ent_amaterno.delete(first=0,last=50)
						self.ent_apaterno.delete(first=0,last=50)
						self.ent_anombre.delete(first=0,last=50)
						self.comboBox1.current(30)
						self.comboBox2.current(1)
						self.comboBox3.current(35)
						self.ent_calle.delete(first=0,last=50)
						self.ent_colonia.delete(first=0,last=50)
						self.ent_cp.delete(first=0,last=50)
						self.ent_telefono.delete(first=0,last=50)
						self.ent_telefonoc.delete(first=0,last=50)
						self.ent_email.delete(first=0,last=50)
						self.gender = IntVar(None, 1)
						self.ent_titulo.delete(first=0,last=50)
						self.list_box1.delete(0,END)
						self.progbar['value'] = 0
		else:
          		tkMessageBox.showerror("ERROR","DATOS NO VALIDOS",icon='warning')
	else:
          	tkMessageBox.showerror("ERROR","DATOS INCOMPLETOS",icon='warning')

    def HuellaCaptura(self):
	pyfprint.fp_init()
	devs = pyfprint.discover_devices()
	if str(devs) != '[]':
		if(self.ent_clave.get() != "" and self.ent_apaterno.get() != "" and self.ent_anombre.get() != "" and self.gender.get() != 0 ):
			if(validacioncampos.Entero(self.ent_clave.get()) == True and validacioncampos.Nombres(self.ent_apaterno.get()) == True and validacioncampos.Nombres(self.ent_anombre.get()) == True and len(self.ent_clave.get().replace(" ", ""))==4):
				
				self.botonPlantillaVoz['state'] = 'disabled'
				self.botonRegistrar['state'] = 'disabled'
				dev = devs[0]
				dev.open()
				fp, img = dev.enroll_finger()
				tkMessageBox.showinfo("Éxito","Huella Capturada Temporalmente \n Se verificara Ahora",icon='info')
				self.progbar['value'] = 40
				self.botonFrame.update_idletasks() 
				time.sleep(1)
				name = "huella"+self.ent_clave.get().replace(" ", "")
				
				b = fp.data()
				with open(os.getcwd()+"/auxHuella/HUELLA" + "/" + name, "wb") as file:
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
					self.progbar['value'] = 0
					self.botonFrame.update_idletasks() 
					dev.close()
					pyfprint.fp_exit()
					time.sleep(1) 
					
				else:
					self.progbar['value'] = 0
					dev.close()
					pyfprint.fp_exit()
					tkMessageBox.showerror("Error","No coincide huella",icon='warning')
					
					self.botonFrame.update_idletasks() 
					time.sleep(1) 		
				
				self.botonPlantillaVoz['state'] = 'normal'
				self.botonRegistrar['state'] = 'normal'
			else:
				tkMessageBox.showerror("Error","FORMATO DE DATOS INCORRECTO",icon='warning')
		else:
			tkMessageBox.showerror("Error","DATOS OBLIGATORIOS SIN COMPLETAR",icon='warning')
	else:
		
		self.botonPlantillaVoz['state'] = 'normal'
		self.botonRegistrar['state'] = 'normal'
		tkMessageBox.showerror("Error","No se encuentra conectado el lector",icon='info')



