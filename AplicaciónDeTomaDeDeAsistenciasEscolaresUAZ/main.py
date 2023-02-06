# -*- coding: utf-8 -*-
from __future__ import print_function
import Tkinter as tk
import Tkinter, tkMessageBox, os, time, datetime, ttk, pyfprint, commands, threading, sys, cPickle, warnings
import IdentificacionUSUARIOSHUELLA, Consultas, IdentificacionUSUARIOSVOZ, removeSilence
from Tkinter import *
from ttk import *
from os import remove
from django.utils.encoding import smart_str, smart_unicode
from datetime import datetime
import RPi.GPIO as GPIO
warnings.filterwarnings("ignore")

#FALTA CAMBIAR LA CONSULTA PARA CONSULTAR TODOS LOS ALUMNOS QUE TIENE EL DOCENTE EN UN CICLO ESCOLAR

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.setup(38, GPIO.OUT)
GPIO.output(38, True)
GPIO.setup(37, GPIO.OUT)
GPIO.output(37, True)
GPIO.setup(33, GPIO.OUT)
GPIO.output(33, True)
GPIO.setup(32, GPIO.OUT)
GPIO.output(32, True)
class Aplicacion(object):
    def __init__(self,master):
        self.master = master
        self.claveDocente = ""
        self.CE = ""
        self.DI = ""
        self.DF = ""
        self.DIA = 0
        self.HORA = ""
	self.FECHA = ""
        self.clase = ["MX.UAZ.Ing.Compu"]
        self.nombreDoc = ["MX.UAZ.Ing.Compu"]
        self.USER = ["MX.UAZ.Ing.Compu"]
        self.HayClase = False
        self.EsAlumno = False
        self.EstaConsultando = False
        self.MatriculaALU = ""
        self.GR_CLAVE = 0
        self.LectorActivo = False
        self.TipoBiometria = False
        self.IntReporte = False

        def MostrarMensajesDeValidacion(tipoValidacion, NombreAlumno, Matricula):
            #A tiempo
            if(tipoValidacion==1):
                self.lbl_matriucla.config(fg="#20716a") 
                self.lbl_alumno.config(fg="#20716a") 			
                self.lbl_ESTADO.config(fg="#20716a")
                self.lbl_matriucla.configure(text=Matricula)
                self.lbl_alumno.configure(text=NombreAlumno)
                self.lbl_ESTADO.configure(text='HA TIEMPO')
            #Con retardo
            elif(tipoValidacion==2):
                self.lbl_matriucla.config(fg="#f77754") 
                self.lbl_alumno.config(fg="#f77754") 			
                self.lbl_ESTADO.config(fg="#f77754")
                self.lbl_matriucla.configure(text=Matricula)
                self.lbl_alumno.configure(text=NombreAlumno)
                self.lbl_ESTADO.configure(text='RETARDO')
            #Fuera de clase
            elif(tipoValidacion==3):
                self.lbl_matriucla.config(fg="#170a19") 
                self.lbl_alumno.config(fg="#170a19") 			
                self.lbl_ESTADO.config(fg="#170a19")
                self.lbl_matriucla.configure(text=Matricula)
                self.lbl_alumno.configure(text=NombreAlumno)
                self.lbl_ESTADO.configure(text='ADIOS')
            #REGISTRO COMPLETO
            elif(tipoValidacion==4):
                self.lbl_matriucla.config(fg="#F0134D") 
                self.lbl_alumno.config(fg="#F0134D") 			
                self.lbl_ESTADO.config(fg="#F0134D")
                self.lbl_matriucla.configure(text=Matricula)
                self.lbl_alumno.configure(text='YA HA REGISTRADO ASISTENCIA')
                self.lbl_ESTADO.configure(text='EN ESTA CLASE')
            #Mensaje Default
            elif(tipoValidacion==5):
                self.lbl_matriucla.config(fg="#420000") 
                self.lbl_alumno.config(fg="#420000") 			
                self.lbl_ESTADO.config(fg="#420000")
                self.lbl_matriucla.configure(text="REALICE SU PASE LISTA")
                self.lbl_alumno.configure(text="COLOQUE SU DEDO O SOLICITE")
                self.lbl_ESTADO.configure(text="EL RECONOCIMIENTO DE VOZ, GRACIAS ;)")
            #Mensaje sin coincidencias
            elif(tipoValidacion==6):
                self.lbl_matriucla.config(fg="#851D41") 
                self.lbl_alumno.config(fg="#851D41") 
                self.lbl_ESTADO.config(fg="#851D41")
                self.lbl_matriucla.configure(text='SIN COINCIDENCIAS')
                self.lbl_alumno.configure(text='PARA GENERACIÓN DE REPORTE')
                self.lbl_ESTADO.configure(text='INTENTE DE NUEVO')
            #Mensaje error de lector
            elif(tipoValidacion==7):
                self.lbl_matriucla.config(fg="#AF460F") 
                self.lbl_alumno.config(fg="#AF460F") 
                self.lbl_ESTADO.config(fg="#AF460F")
                self.lbl_matriucla.configure(text='ERROR LECTOR')
                self.lbl_alumno.configure(text='DESCONECTADO')
                self.lbl_ESTADO.configure(text=' ')
            #Mensaje error de db
            elif(tipoValidacion==8):
                self.lbl_matriucla.config(fg="#851D41") 
                self.lbl_alumno.config(fg="#851D41") 
                self.lbl_ESTADO.config(fg="#851D41")
                self.lbl_matriucla.configure(text='ERROR DB')
                self.lbl_alumno.configure(text='SIN CONEXIÓN')
                self.lbl_ESTADO.configure(text=' ')
                
            elif(tipoValidacion==9):
                self.lbl_matriucla.config(fg="#272727") 
                self.lbl_alumno.config(fg="#272727") 
                self.lbl_ESTADO.config(fg="#272727")
                self.lbl_matriucla.configure(text='SOLICITANDO REPORTE')
                self.lbl_alumno.configure(text='DE ASISTENCIAS DEL ALUMNO')
                self.lbl_ESTADO.configure(text='CON MATRÍCULA:'+Matricula)
            
            elif(tipoValidacion==10):
                self.lbl_matriucla.config(fg="#420000") 
                self.lbl_alumno.config(fg="#420000") 
                self.lbl_ESTADO.config(fg="#420000")
                self.lbl_matriucla.configure(text='SOLICITO RECONOCIMIENTO')
                self.lbl_alumno.configure(text='DE VOZ')
                self.lbl_ESTADO.configure(text='GRABANDO AUDIO...')
                
            #Mensaje error de lector
            elif(tipoValidacion==11):
                self.lbl_matriucla.config(fg="#AF460F") 
                self.lbl_alumno.config(fg="#AF460F") 
                self.lbl_ESTADO.config(fg="#AF460F")
                self.lbl_matriucla.configure(text='ERROR MICROFONO')
                self.lbl_alumno.configure(text='DESCONECTADO')
                self.lbl_ESTADO.configure(text=' ')
                
            #Mensaje error de lector
            elif(tipoValidacion==12):
                self.lbl_matriucla.config(fg="#333366") 
                self.lbl_alumno.config(fg="#333366") 
                self.lbl_ESTADO.config(fg="#333366")
                self.lbl_matriucla.configure(text='¿USTED ES EL DOCENTE')
                self.lbl_alumno.configure(text='CON CLAVE:'+NombreAlumno+'?')
                self.lbl_ESTADO.configure(text='REALICE LA CONFIRMACIÓN')
            
            #Mensaje error de lector
            elif(tipoValidacion==13):
                self.lbl_matriucla.config(fg="#333366") 
                self.lbl_alumno.config(fg="#333366") 
                self.lbl_ESTADO.config(fg="#333366")
                self.lbl_matriucla.configure(text='¿USTED ES EL ALUMNO')
                self.lbl_alumno.configure(text='CON MATRÍCULA:'+NombreAlumno+'?')
                self.lbl_ESTADO.configure(text='REALICE LA CONFIRMACIÓN')
            
            #Mensaje error de lector
            elif(tipoValidacion==14):
                self.lbl_matriucla.config(fg="#550A46") 
                self.lbl_alumno.config(fg="#550A46") 
                self.lbl_ESTADO.config(fg="#550A46")
                self.lbl_matriucla.configure(text='NO SE GENERO EL REPORTE')
                self.lbl_alumno.configure(text='PARA SU ENVIO PARA')
                self.lbl_ESTADO.configure(text='EL ALUMNO CON MATRÍCULA: '+NombreAlumno)
            
            #Mensaje error de lector
            elif(tipoValidacion==15):
                self.lbl_matriucla.config(fg="#50D890") 
                self.lbl_alumno.config(fg="#50D890") 
                self.lbl_ESTADO.config(fg="#50D890")
                self.lbl_matriucla.configure(text='SE ENVIO SATISFACTORIMEMTE')
                self.lbl_alumno.configure(text='EL REPORTE PARA EL ALUMNO')
                self.lbl_ESTADO.configure(text='CON MATRÍCULA: '+NombreAlumno)
            
            elif(tipoValidacion==16):
                self.lbl_matriucla.config(fg="#90303D") 
                self.lbl_alumno.config(fg="#90303D") 
                self.lbl_ESTADO.config(fg="#90303D")
                self.lbl_matriucla.configure(text='USTED NO PUEDE SOLICITAR')
                self.lbl_alumno.configure(text='EL REPORTE DE ASISTENCIAS')
                self.lbl_ESTADO.configure(text='EN ESTE MOMENTO')
            
            elif(tipoValidacion==17):
                self.lbl_matriucla.config(fg="#420000") 
                self.lbl_alumno.config(fg="#420000") 
                self.lbl_ESTADO.config(fg="#420000")
                self.lbl_matriucla.configure(text='SOLICITUD DE GENERACIÓN')
                self.lbl_alumno.configure(text='DE REPORTE DE ASISTENCIAS')
                self.lbl_ESTADO.configure(text=NombreAlumno)
            
            elif(tipoValidacion==18):
                self.lbl_matriucla.config(fg="#363F44") 
                self.lbl_alumno.config(fg="#363F44") 
                self.lbl_ESTADO.config(fg="#363F44")
                self.lbl_matriucla.configure(text='SALIENDO DEL MODO')
                self.lbl_alumno.configure(text='DE REPORTE DE ASISTENCIAS')
                self.lbl_ESTADO.configure(text=' ')
            
            #Mensaje error de lector
            elif(tipoValidacion==19):
                self.lbl_matriucla.config(fg="#333366") 
                self.lbl_alumno.config(fg="#333366") 
                self.lbl_ESTADO.config(fg="#333366")
                self.lbl_matriucla.configure(text='¿USTED ES EL ALUMNO CON')
                self.lbl_alumno.configure(text='MATRÍCULA:'+NombreAlumno+'?')
                self.lbl_ESTADO.configure(text='REALICE LA CONFIRMACIÓN PARA REPORTE')
                
            #Mensaje error de lector
            elif(tipoValidacion==20):
                self.lbl_matriucla.config(fg="#FF7315") 
                self.lbl_alumno.config(fg="#FF7315") 
                self.lbl_ESTADO.config(fg="#FF7315")
                self.lbl_matriucla.configure(text='EL ALUMNO CON MATRÍCULA:')
                self.lbl_alumno.configure(text=NombreAlumno+' NO TIENE REGISTRO')
                self.lbl_ESTADO.configure(text='DE CORREO PARA ENVIO DE REPORTE')
            
            elif(tipoValidacion==21):
                self.lbl_matriucla.config(fg="#00BD56") 
                self.lbl_alumno.config(fg="#00BD56") 
                self.lbl_ESTADO.config(fg="#00BD56")
                self.lbl_matriucla.configure(text='SE ENVIO EL REPORTE')
                self.lbl_alumno.configure(text='DE ASISTENCIAS AL ALUMNO CON ')
                self.lbl_ESTADO.configure(text='MATRÍCULA: '+NombreAlumno+' SATISFACTORIAMENTE')
                
            elif(tipoValidacion==22):
                self.lbl_matriucla.config(fg="#560D0D") 
                self.lbl_alumno.config(fg="#560D0D") 
                self.lbl_ESTADO.config(fg="#560D0D")
                self.lbl_matriucla.configure(text='NO SE ENVIO EL REPORTE')
                self.lbl_alumno.configure(text='DE ASISTENCIAS DEL ALUMNO CON MATRÍCULA:')
                self.lbl_ESTADO.configure(text=NombreAlumno)
                
            elif(tipoValidacion==23):
                self.lbl_matriucla.config(fg="#FF6337") 
                self.lbl_alumno.config(fg="#FF6337") 
                self.lbl_ESTADO.config(fg="#FF6337")
                self.lbl_matriucla.configure(text='SUCEDIO UN ERROR')
                self.lbl_alumno.configure(text='INESPERADO AL GENERAR/ENVIAR')
                self.lbl_ESTADO.configure(text='EL REPORTE')

            elif(tipoValidacion==24):
                self.lbl_matriucla.config(fg="#FF6337") 
                self.lbl_alumno.config(fg="#FF6337") 
                self.lbl_ESTADO.config(fg="#FF6337")
                self.lbl_matriucla.configure(text='NO HAY MAESTRO')
                self.lbl_alumno.configure(text='ASOCIADO AL MÓDULO')
                self.lbl_ESTADO.configure(text='DE ASISTENCIAS')

        def DiaActual():
	    #QUITAR LAS 4 LINEAS SIGUIENTES 
            self.CE = "2021SNON"
            self.DI = "GH_LUNESINI"
            self.DF = "GH_LUNESTR"
            self.DIA = 1
            """
            DESCOMENTAR ESTO
            diaSemana = str(smart_str(Consultas.ConsultasGenerales10(10))).replace(" ", "")
            self.CE = Consultas.ConsultasGenerales1(1,Consultas.ConsultasGenerales8(8,1))
            if(diaSemana=='LUNES'):
                self.DI = "GH_LUNESINI"
                self.DF = "GH_LUNESTR"
                self.DIA = 1
            elif(diaSemana=='MARTES'):
                self.DI = "GH_MARTESINI"
                self.DF = "GH_MARTESTER"
                self.DIA = 2
            elif(diaSemana=='MIÉRCOLES'):
                self.DI = "GH_MIERCOLESINI"
                self.DF = "GH_MIERCOLESTER"
                self.DIA = 3
            elif(diaSemana=='JUEVES'):
                self.DI = "GH_JUEVESINI"
                self.DF = "GH_JUEVESTER"
                self.DIA = 4
            elif(diaSemana=='VIERNES'):
                self.DI = "GH_VIERNESINI"
                self.DF = "GH_VIERNESTER"
                self.DIA = 5
            elif(diaSemana=='SÁBADO'):
                self.DI = "GH_SABADOINI"
                self.DF = "GH_SABADOTER"
                self.DIA = 6
            else:
                self.DI = "GH_SABADOINI"
                self.DF = "GH_SABADOTER"
                self.DIA = 6
            """
        def identificacionUsuariosVoz(*args):
            cout = 0
            while True:
                self.IntReporte = False
                master.update_idletasks()
                if GPIO.input(31) == GPIO.LOW:
                    self.IntReporte = True
                    if self.GR_CLAVE != 0:
                        count = 0
                        MostrarMensajesDeValidacion(17, '', '')
                        time.sleep(1)
                        while True:
                            master.update_idletasks()
                            if GPIO.input(31) == GPIO.LOW:
                                MostrarMensajesDeValidacion(18, '', '')
                                time.sleep(1)
                                break
                            
                            if self.EsAlumno == True:
                                self.EsAlumno = False
                                MostrarMensajesDeValidacion(9, '', self.MatriculaALU)
                                #AQUI VAN LA CONSULTA DEL REPORTE DE ASISTENCIAS
                                RESULTADO = Consultas.ConsultasReportes(self.CE,self.MatriculaALU,str(self.GR_CLAVE))
                                if(RESULTADO == 1):
                                    MostrarMensajesDeValidacion(20, self.MatriculaALU, '')
                                elif(RESULTADO == 2):
                                    MostrarMensajesDeValidacion(21, self.MatriculaALU, '')
                                elif(RESULTADO == 3):
                                    MostrarMensajesDeValidacion(22, self.MatriculaALU, '')
                                elif(RESULTADO == 4):
                                    MostrarMensajesDeValidacion(23, '', '')
                                break
                            
                            if count >= 5:
                                MostrarMensajesDeValidacion(18, '', '')
                                break
                            
                            
                            if GPIO.input(36) == GPIO.LOW:
                                MostrarMensajesDeValidacion(17, 'VOZ', '')
                                grabar = os.system('arecord -D plughw:1 -d 5 -f cd '+os.getcwd()+'/MUESTRA_VOZ/AUDIO_TEST.wav')
                                removeSilence.remover_silencio(os.getcwd()+'/MUESTRA_VOZ/AUDIO_TEST.wav')
                                if int(grabar) == 0:
                                    master.update_idletasks()
                                    self.USER = IdentificacionUSUARIOSVOZ.user()
                                    if self.USER[0] == 2:
                                        self.MatriculaALU = self.USER[1]
                                        MostrarMensajesDeValidacion(19, self.MatriculaALU, '')
                                        count = 0
                                        while True:
                                            master.update_idletasks()
                                            if GPIO.input(35) == GPIO.LOW:
                                                #AQUI VAN LA CONSULTA DEL REPORTE DE ASISTENCIAS
                                                #RESULTADO = Consultas.ConsultasReportes(self.CE,self.MatriculaALU,str(self.GR_CLAVE))
                                                MostrarMensajesDeValidacion(9, '', self.MatriculaALU)
                                                RESULTADO = Consultas.ConsultasReportes(self.CE,self.MatriculaALU,str(self.GR_CLAVE))
                                                if(RESULTADO == 1):
                                                    MostrarMensajesDeValidacion(20, self.MatriculaALU, '')
                                                elif(RESULTADO == 2):
                                                    MostrarMensajesDeValidacion(21, self.MatriculaALU, '')
                                                elif(RESULTADO == 3):
                                                    MostrarMensajesDeValidacion(22, self.MatriculaALU, '')
                                                elif(RESULTADO == 4):
                                                    MostrarMensajesDeValidacion(23, '', '')
                                                break
                                            
                                            if GPIO.input(40) == GPIO.LOW:
                                                self.EsAlumno == False
                                                MostrarMensajesDeValidacion(18, '', '')
                                                break
                                            
                                            if GPIO.input(31) == GPIO.LOW:
                                                MostrarMensajesDeValidacion(18, '', '')
                                                time.sleep(1)
                                                break
                                            
                                            if count >= 5:
                                                self.IntReporte = False
                                                MostrarMensajesDeValidacion(18, '', '')
                                                break
                                            
                                            time.sleep(1)
                                            count = count + 1
                                    else:
                                        MostrarMensajesDeValidacion(6, '', '')
                                        break
                                else:
                                    MostrarMensajesDeValidacion(11, '', '')
                                    break
                                break
                            #############################################################################
                                    
                            
                            time.sleep(1)
                            count = count + 1
                        
                        
                    else:
                        MostrarMensajesDeValidacion(16, '', '')
                
                
                
                
                
                if GPIO.input(36) == GPIO.LOW:
                    self.IntReporte = False
                    MostrarMensajesDeValidacion(10, '', '')
                    grabar = os.system('arecord -D plughw:1 -d 5 -f cd '+os.getcwd()+'/MUESTRA_VOZ/AUDIO_TEST.wav')
                    removeSilence.remover_silencio(os.getcwd()+'/MUESTRA_VOZ/AUDIO_TEST.wav')
                    if int(grabar) == 0:
                        master.update_idletasks()
                        self.USER = IdentificacionUSUARIOSVOZ.user()
                        if self.USER[0] == 1:
                            MostrarMensajesDeValidacion(12, self.USER[1], '')
                            count = 0
                            while True:
                                master.update_idletasks()
                                if GPIO.input(35) == GPIO.LOW:
                                    self.claveDocente = self.USER[1]
                                    f = open (os.getcwd() + "/LOGIN/LOGIN.txt",'w')
                                    f.write(self.claveDocente.replace('\n', ' ').replace('\r', '').replace(" ", ""))
                                    f.close()
                                    for name in os.listdir(os.getcwd()+"/HUELLAS/"):
                                        if len(name.replace('\n', ' ').replace('\r', '').replace(" ", "")) == 8:
                                            remove(os.getcwd() + "/HUELLAS/" + name)
                                    for name in os.listdir(os.getcwd()+"/VOCES/"):
                                        if len(name.replace('\n', ' ').replace('\r', '').replace(" ", "")) == 12:
                                            remove(os.getcwd() + "/VOCES/" + name)
                                    #HuellasAlumnos = commands.getoutput("java -classpath ./ojdbcfull/ojdbc6.jar:. ConsultaHuellasAlumnos "+str(2)+" "+str(1111)+" "+str('1920SNON'))
                                    #VocesAlumnos = commands.getoutput("java -classpath ./ojdbcfull/ojdbc6.jar:. ConsultaVocesAlumnos "+str(2)+" "+str(1111)+" "+str('1920SNON'))
                                    HuellasA = commands.getoutput("java -classpath ./ojdbcfull/ojdbc6.jar:. ConsultaHuellasAlumnos "+str(self.DIA)+" "+str(self.claveDocente)+" "+str(self.CE))
                                    VocesAlumnos = commands.getoutput("java -classpath ./ojdbcfull/ojdbc6.jar:. ConsultaVocesAlumnos "+str(self.DIA)+" "+str(self.claveDocente)+" "+str(self.CE))
                                    if(HuellasAlumnos.replace('\n', ' ').replace('\r', '').replace(" ", "") == "TRUE-HUELLAS-ALUMNOS" and VocesAlumnos.replace('\n', ' ').replace('\r', '').replace(" ", "") == "TRUE-VOCES-ALUMNOS"):
                                        MostrarMensajesDeValidacion(5, '', '')
                                    else:
                                        MostrarMensajesDeValidacion(8, '', '')
                                    break
                                if GPIO.input(40) == GPIO.LOW:
                                    MostrarMensajesDeValidacion(5, '', '')
                                    time.sleep(1)
                                    break
                                if count >= 5:
                                    MostrarMensajesDeValidacion(5, '', '')
                                    time.sleep(1)
                                    break
                                time.sleep(1)
                                count = count + 1

                        else:
                            MostrarMensajesDeValidacion(13, self.USER[1], '')
                            count = 0
                            while True:
                                master.update_idletasks()
                                if GPIO.input(35) == GPIO.LOW:
                                    if(self.HayClase == True):
                                        self.MatriculaALU = self.USER[1]
                                        self.EsAlumno = True
                                        self.TipoBiometria = True
                                    else:
                                        self.EsAlumno = False
                                        if self.IntReporte==False:
                                            pass#MMostrarMensajesDeValidacion(6, '', '')
                                    break
                                if GPIO.input(40) == GPIO.LOW:
                                    MostrarMensajesDeValidacion(5, '', '')
                                    break
                                if count >= 5:
                                    MostrarMensajesDeValidacion(5, '', '')
                                    break
                                time.sleep(1)
                                count = count + 1
                    else:
                        MostrarMensajesDeValidacion(11, '', '')
                        

        def identificacionUsuariosHuella(*args):
            while True:
                master.update_idletasks()
                self.USER = IdentificacionUSUARIOSHUELLA.user()
                if(self.USER[0]!=0):
                    if(self.USER[0]==1):
                        self.claveDocente = self.USER[1]
			f = open (os.getcwd() + "/LOGIN/LOGIN.txt",'w')
			f.write(self.claveDocente.replace('\n', ' ').replace('\r', '').replace(" ", ""))
			f.close()
                        for name in os.listdir(os.getcwd()+"/HUELLAS/"):
                            if len(name.replace('\n', ' ').replace('\r', '').replace(" ", "")) == 8:
                                remove(os.getcwd() + "/HUELLAS/" + name)
                        for name in os.listdir(os.getcwd()+"/VOCES/"):
                            if len(name.replace('\n', ' ').replace('\r', '').replace(" ", "")) == 12:
                                remove(os.getcwd() + "/VOCES/" + name)
                        #HuellasAlumnos = commands.getoutput("java -classpath ./ojdbcfull/ojdbc6.jar:. ConsultaHuellasAlumnos "+str(2)+" "+str(1111)+" "+str('1920SNON'))
                        #VocesAlumnos = commands.getoutput("java -classpath ./ojdbcfull/ojdbc6.jar:. ConsultaVocesAlumnos "+str(2)+" "+str(1111)+" "+str('1920SNON'))
                        HuellasAlumnos = commands.getoutput("java -classpath ./ojdbcfull/ojdbc6.jar:. ConsultaHuellasAlumnos "+str(self.DIA)+" "+str(self.claveDocente)+" "+str(self.CE))
                        VocesAlumnos = commands.getoutput("java -classpath ./ojdbcfull/ojdbc6.jar:. ConsultaVocesAlumnos "+str(self.DIA)+" "+str(self.claveDocente)+" "+str(self.CE))
			if(HuellasAlumnos.replace('\n', ' ').replace('\r', '').replace(" ", "") == "TRUE-HUELLAS-ALUMNOS" and VocesAlumnos.replace('\n', ' ').replace('\r', '').replace(" ", "") == "TRUE-VOCES-ALUMNOS"):
                            MostrarMensajesDeValidacion(5, '', '')
                        else:
                            MostrarMensajesDeValidacion(8, '', '')
                    if(self.USER[0]==2):
                        if(self.HayClase == True):
                            self.MatriculaALU = self.USER[1]
                            self.EsAlumno = True
                            self.TipoBiometria = False
                        else:
                            if self.IntReporte==False:
                                pass#MMostrarMensajesDeValidacion(6, '', '')
                    if(self.USER[0]==3):
                        if self.IntReporte==False:
                            pass#MMostrarMensajesDeValidacion(6, '', '')
                else:
                    MostrarMensajesDeValidacion(7, '', '')

        def Clase(*args):
            hiloUsuariosHuella = threading.Thread(target=identificacionUsuariosHuella)
            hiloUsuariosHuella.start()
            hiloUsuariosVoz = threading.Thread(target=identificacionUsuariosVoz)
            hiloUsuariosVoz.start()
            #POR DEFAULT SE ESTABLECEN CONFIGURACIONES POR DEFAULT
            HuellasDocentes = commands.getoutput('java -classpath ./ojdbcfull/ojdbc6.jar:. ConsultaHuellasDocentes')
            VocesDocentes = commands.getoutput('java -classpath ./ojdbcfull/ojdbc6.jar:. ConsultaVocesDocentes')
            if(HuellasDocentes.replace('\n', ' ').replace('\r', '').replace(" ", "") == "TRUE-HUELLAS-DOCENTES" and VocesDocentes.replace('\n', ' ').replace('\r', '').replace(" ", "") == "TRUE-VOCES-DOCENTES"):
                MostrarMensajesDeValidacion(5, '', '')
            else:
                MostrarMensajesDeValidacion(8, '', '')
            f = open (os.getcwd() + "/LOGIN/LOGIN.txt",'r')
            self.claveDocente = str(f.read().replace('\n', ' ').replace('\r', '').replace(" ", ""))
            f.close()
            self.nombreDoc = Consultas.ConsultasGenerales7(7,self.claveDocente)


	    if self.nombreDoc == '':
		while True:
			master.update_idletasks()
			self.HORA = Consultas.ConsultasGenerales8(8,0)
			self.lbl_hora.configure (text='HORA: ' +str(self.HORA))
			self.FECHA = Consultas.ConsultasGenerales8(8,3)
			self.lbl_fecha.configure (text='FECHA: ' +str(self.FECHA))
			f = open (os.getcwd() + "/LOGIN/LOGIN.txt",'r')
                        self.claveDocente = str(f.read().replace('\n', ' ').replace('\r', '').replace(" ", ""))
                        f.close()
                        self.nombreDoc = Consultas.ConsultasGenerales7(7,self.claveDocente)
			if self.nombreDoc != '':
				if self.nombreDoc[2] != None:
					self.lbl_ndocente.configure(text="DOCENTE: "+str(self.nombreDoc[0])+" "+str(self.nombreDoc[1])+" "+str(self.nombreDoc[2]))
				else:
					self.lbl_ndocente.configure(text="DOCENTE: "+str(self.nombreDoc[0])+" "+str(self.nombreDoc[1]))
				break
			else:
				MostrarMensajesDeValidacion(24, '', '')	
	    else:
		if self.nombreDoc[2] != None:
		        self.lbl_ndocente.configure(text="DOCENTE: "+str(self.nombreDoc[0])+" "+str(self.nombreDoc[1])+" "+str(self.nombreDoc[2]))
		else:
		        self.lbl_ndocente.configure(text="DOCENTE: "+str(self.nombreDoc[0])+" "+str(self.nombreDoc[1]))


            DiaActual()
            HuellasAlumnos = commands.getoutput("java -classpath ./ojdbcfull/ojdbc6.jar:. ConsultaHuellasAlumnos "+str(self.DIA)+" "+str(self.claveDocente)+" "+str(self.CE))
            VocesAlumnos = commands.getoutput("java -classpath ./ojdbcfull/ojdbc6.jar:. ConsultaVocesAlumnos "+str(self.DIA)+" "+str(self.claveDocente)+" "+str(self.CE))
            if(HuellasAlumnos.replace('\n', ' ').replace('\r', '').replace(" ", "") == "TRUE-HUELLAS-ALUMNOS" and VocesAlumnos.replace('\n', ' ').replace('\r', '').replace(" ", "") == "TRUE-VOCES-ALUMNOS"):
                MostrarMensajesDeValidacion(5, '', '')
            else:
                MostrarMensajesDeValidacion(8, '', '')
            self.HORA = Consultas.ConsultasGenerales8(8,0)
            self.clase = Consultas.ConsultasGenerales2(2,self.claveDocente,self.CE,self.DI,self.DF,self.HORA)
            self.lbl_hora.configure(text="HORA: "+str(self.HORA))
	    self.FECHA = Consultas.ConsultasGenerales8(8,3)
	    self.lbl_fecha.configure (text='FECHA: ' +str(self.FECHA))
            if self.clase != '':
                self.lbl_nmateria.configure(text="MATERIA: "+str(self.clase[0]) +' - ' + str(self.clase[5]))
            else:
                self.lbl_nmateria.configure(text="MATERIA: NO HAY CLASE A ESTA HORA")
            while True:
                DiaActual()
                master.update_idletasks()
		#DESCOMENTAR ESTA LINEA
                #self.HORA = Consultas.ConsultasGenerales8(8,0)
		self.FECHA = Consultas.ConsultasGenerales8(8,3)
		self.lbl_fecha.configure (text='FECHA: ' +str(self.FECHA))
                HORA_SERVIDOR = datetime.strptime(self.HORA, "%X").time()
                HORA_FIJA_CAMBIO1 = datetime.strptime("00:45:00", "%X").time()
                HORA_FIJA_CAMBIO2 = datetime.strptime("00:48:00", "%X").time()
                if HORA_SERVIDOR >= HORA_FIJA_CAMBIO1 and HORA_SERVIDOR <= HORA_FIJA_CAMBIO2:
                    HuellasAlumnos = commands.getoutput("java -classpath ./ojdbcfull/ojdbc6.jar:. ConsultaHuellasAlumnos "+str(self.DIA)+" "+str(self.claveDocente)+" "+str(self.CE))
                    VocesAlumnos = commands.getoutput("java -classpath ./ojdbcfull/ojdbc6.jar:. ConsultaVocesAlumnos "+str(self.DIA)+" "+str(self.claveDocente)+" "+str(self.CE))
                    if(HuellasAlumnos.replace('\n', ' ').replace('\r', '').replace(" ", "") == "TRUE-HUELLAS-ALUMNOS" and VocesAlumnos.replace('\n', ' ').replace('\r', '').replace(" ", "") == "TRUE-VOCES-ALUMNOS"):
                        MostrarMensajesDeValidacion(5, '', '')
                    else:
                        MostrarMensajesDeValidacion(8, '', '')
                    time.sleep(180)
                            
                self.lbl_hora.configure (text='HORA: ' +str(self.HORA))

		#QUITAR ESTA LINEA
                self.HORA = '07:30:00'

                self.nombreDoc = Consultas.ConsultasGenerales7(7,self.claveDocente)
                
                if self.nombreDoc[2] != None:
                    self.lbl_ndocente.configure(text="DOCENTE: "+str(self.nombreDoc[0])+" "+str(self.nombreDoc[1])+" "+str(self.nombreDoc[2]))
                else:
                    self.lbl_ndocente.configure(text="DOCENTE: "+str(self.nombreDoc[0])+" "+str(self.nombreDoc[1]))
                self.clase = Consultas.ConsultasGenerales2(2,self.claveDocente,self.CE,self.DI,self.DF,self.HORA)
                if self.clase != '':
                    if self.clase[4] != None and self.clase[4] != 0:
                        self.lbl_RETARDO.configure(text="R. "+str(self.clase[4]))
                    else:
                        self.clase[4] = 1000               
                        self.lbl_RETARDO.configure(text="R. N/A")
                    self.GR_CLAVE = self.clase[3]
                    self.lbl_nmateria.configure(text="MATERIA: "+str(self.clase[0]) +' - ' + str(self.clase[5]))
                    self.HayClase = True
                    if(self.EsAlumno == True and self.HayClase == True and self.IntReporte==False):
                        self.EsAlumno = False
                        inClass = Consultas.ConsultasGenerales3(3,self.CE,self.claveDocente,self.MatriculaALU,self.clase[3],self.HORA,self.DI,self.DF)
                        if(inClass[0]==True):
                            ASISTENCIA = Consultas.ConsultasGenerales5(5,self.CE,self.claveDocente,inClass[1],self.clase[3],self.HORA,self.DI,self.DF,Consultas.ConsultasGenerales8(8,1))
                            if(ASISTENCIA[0] == True):
                                if(ASISTENCIA[1] != None and ASISTENCIA[2] != None and ASISTENCIA[3] == None):
                                    if self.TipoBiometria == True:
                                        Consultas.ConsultasGenerales12(12, ASISTENCIA[4],self.HORA,Consultas.ConsultasGenerales8(8,1))
                                        self.TipoBiometria = False
                                    else:
                                        Consultas.ConsultasGenerales6(6, ASISTENCIA[4],self.HORA,Consultas.ConsultasGenerales8(8,1))
                                        self.TipoBiometria = False
                                    if inClass[4] != None:
                                        MostrarMensajesDeValidacion(3, inClass[1], inClass[2] + ' ' + inClass[3] + ' ' + inClass[4])
                                    else:
                                        MostrarMensajesDeValidacion(3, inClass[1], inClass[2] + ' ' + inClass[3])
                                elif(ASISTENCIA[1] != None and ASISTENCIA[2] != None and ASISTENCIA[3] != None):
                                    if inClass[4] != None:
                                        MostrarMensajesDeValidacion(4, inClass[1], inClass[2] + ' ' + inClass[3] + ' ' + inClass[4])
                                    else:
                                        MostrarMensajesDeValidacion(4, inClass[1], inClass[2] + ' ' + inClass[3])
                            else:
                                if(Consultas.ConsultasGenerales9(9, self.CE, self.claveDocente, inClass[1], self.clase[3], self.HORA, self.DI, inClass[5])):
                                    if self.TipoBiometria == True:
                                        Consultas.ConsultasGenerales11(11, self.CE, inClass[1], str(self.clase[3]), self.HORA, Consultas.ConsultasGenerales8(8,1), True)
                                        self.TipoBiometria = False
                                        if inClass[4] != None:
                                            MostrarMensajesDeValidacion(2, inClass[1], inClass[2] + ' ' + inClass[3] + ' ' + inClass[4])
                                        else:
                                            MostrarMensajesDeValidacion(2, inClass[1], inClass[2] + ' ' + inClass[3])
                                    else:
                                        Consultas.ConsultasGenerales4(4, self.CE, inClass[1], str(self.clase[3]), self.HORA, Consultas.ConsultasGenerales8(8,1), True)
                                        self.TipoBiometria = False
                                        if inClass[4] != None:
                                            MostrarMensajesDeValidacion(2, inClass[1], inClass[2] + ' ' + inClass[3] + ' ' + inClass[4])
                                        else:
                                            MostrarMensajesDeValidacion(2, inClass[1], inClass[2] + ' ' + inClass[3])
                                else:
                                    if self.TipoBiometria == True:
                                        Consultas.ConsultasGenerales11(11, self.CE, inClass[1], str(self.clase[3]), self.HORA, Consultas.ConsultasGenerales8(8,1), False)
                                        self.TipoBiometria = False
                                        if inClass[4] != None:
                                            MostrarMensajesDeValidacion(1, inClass[1], inClass[2] + ' ' + inClass[3] + ' ' + inClass[4])
                                        else:
                                            MostrarMensajesDeValidacion(1, inClass[1], inClass[2] + ' ' + inClass[3])
                                    else:
                                        Consultas.ConsultasGenerales4(4, self.CE, inClass[1], str(self.clase[3]), self.HORA, Consultas.ConsultasGenerales8(8,1), False)
                                        self.TipoBiometria = False
                                        if inClass[4] != None:
                                            MostrarMensajesDeValidacion(1, inClass[1], inClass[2] + ' ' + inClass[3] + ' ' + inClass[4])
                                        else:
                                            MostrarMensajesDeValidacion(1, inClass[1], inClass[2] + ' ' + inClass[3])
                        else:
                            if self.IntReporte==False:
                                pass#MostrarMensajesDeValidacion(6, '', '')
                else:
                    #user = IdentificacionUSUARIOSHUELLA.user(self.CE,self.claveDocente,str(self.clase[3]),self.DI,self.DF)
                    self.nombreDoc = Consultas.ConsultasGenerales7(7,self.claveDocente)
                    if self.nombreDoc[2] != None:
                        self.lbl_ndocente.configure(text="DOCENTE: "+str(self.nombreDoc[0])+" "+str(self.nombreDoc[1])+" "+str(self.nombreDoc[2]))
                    else:
                        self.lbl_ndocente.configure(text="DOCENTE: "+str(self.nombreDoc[0])+" "+str(self.nombreDoc[1]))
                    self.lbl_RETARDO.configure(text="R. NT")
                    self.GR_CLAVE = 0
                    self.lbl_nmateria.configure(text="MATERIA: NO HAY CLASE A ESTA HORA")
                    self.HayClase = False

        #Ventanas
        self.top = tk.Frame(master,height=90,bg='#113a5d')
        self.top.pack(fill=X)
        self.boton = tk.Frame(master,height=500,bg='#feffdf')
        self.boton.pack(fill=X)
        #Encabezado, imagen y fecha
        self.top_image = PhotoImage(file='icons/uaz4.png')
        self.top_image_lbl = tk.Label(self.top,image=self.top_image,bg="#113a5d")
        self.top_image_lbl.place(x=5,y=5)
        self.encabezado=tk.Label(self.top,text='CONTROL DE ASISTENCIA - UAZ',font='arial 12 bold', fg='white', bg="#113a5d")
        self.encabezado.place(x=120,y=20)
        #formulario 
        self.lbl_fecha = tk.Label(self.top, text='FECHA: ', font='arial 11 bold', fg='white', bg='#113a5d')
        self.lbl_fecha.place(x=130,y=60)
        self.lbl_hora = tk.Label(self.top, text='HORA: ', font='arial 11 bold', fg='white', bg='#113a5d')
        self.lbl_hora.place(x=265,y=60)
        
        self.lbl_RETARDO = tk.Label(self.boton, text='R. N/A', font='arial 11 bold', fg='black', bg='#feffdf')
        self.lbl_RETARDO.place(x=380,y=5)
        
        self.lbl_ndocente = tk.Label(self.boton, text='DOCENTE:', font='arial 10 bold', fg='black', bg='#feffdf')
        self.lbl_ndocente.place(x=5,y=10) 
        self.lbl_nmateria = tk.Label(self.boton, text='MATERIA:', font='arial 10 bold', fg='black', bg='#feffdf')
        self.lbl_nmateria.place(x=5,y=40) 
        self.lbl_MAT = tk.Label(self.boton, text='', font='arial 10 bold', fg='black', bg='#feffdf')
        self.lbl_MAT.place(x=5,y=40) 
        self.lbl_susuario = tk.Label(self.boton, text='ESTADO DE USUARIO:', font='arial 10 bold', fg='black', bg='#feffdf')
        self.lbl_susuario.place(x=5,y=70) 
        self.lbl_matriucla = tk.Label(self.boton, text='REALICE SU PASE LISTA', font='fixedsys 16 bold', fg='#420000', bg='#feffdf')
        self.lbl_matriucla.place(x=20,y=110) 
        self.lbl_alumno = tk.Label(self.boton, text='COLOQUE SU DEDO', font='fixedsys 12 bold', fg='#420000', bg='#feffdf')
        self.lbl_alumno.place(x=20,y=160)
        self.lbl_ESTADO = tk.Label(self.boton, text='POR SU ATENCIÓN GRACIAS', font='fixedsys 11 bold', fg='#420000', bg='#feffdf')
        self.lbl_ESTADO.place(x=20,y=200) 
        hiloClase = threading.Thread(target=Clase)	
        hiloClase.start()

def principal():
    root = Tk()
    app = Aplicacion(root)
    root.title("MÓDULO DE ASISTENCIA - UAZ")
    root.geometry("480x320+0+0")
    #DESCOMENTAR LAS SIGUIENTES 2 LINEAS	
    #root.resizable(False,False)
    #root.overrideredirect(1)
    root.mainloop()

if __name__ == '__main__':
    principal()
