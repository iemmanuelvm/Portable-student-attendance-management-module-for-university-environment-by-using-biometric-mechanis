# -*- coding: utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib, os

def EnviarCorreo(clave, correoDestinatario, Nombre, Asignatura):
	try:
		msg = MIMEMultipart()
		message = "Estimado(a) "+Nombre+":\nHa solicitado solicitado su reporte de asistencia de la asignatura "+Asignatura
		password = clave
		msg['From'] = "gestoracademico.ic.is@uaz.edu.mx"
		msg['To'] = correoDestinatario
		msg['Subject'] = "REPORTE DE ASISTENCIAS"
		part = MIMEApplication(open(os.getcwd()+"/Reportes/reporte.pdf","rb").read())
		part.add_header('Content-Disposition', 'attachment', filename="reporte.pdf")
		msg.attach(MIMEText(message, 'plain'))
		msg.attach(part)
		server = smtplib.SMTP('smtp.gmail.com: 587')
		server.starttls()
		server.login(msg['From'], password)	 
		server.sendmail(msg['From'], msg['To'], msg.as_string())
		server.quit()
		return True
	except:
		return False
