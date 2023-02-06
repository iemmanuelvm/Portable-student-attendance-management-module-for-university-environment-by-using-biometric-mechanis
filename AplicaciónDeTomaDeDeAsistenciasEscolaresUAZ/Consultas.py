# -*- coding: utf-8 -*-
import jpype, os, time, datetime, base64
from jpype import *
import reportesasistencia, envioReportes

f = open (os.getcwd() + "/CONFIGURACION_DB/conexiondb.uaz",'r')
clave = f.read()
f.close()
clave = base64.b64decode(clave)
x = clave.split('\n')

def ConsultasGenerales1(*args):
	if isJVMStarted() == False:
		classpath = os.getcwd()+"/ojdbcfull/ojdbc6.jar"
		startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + classpath)
	conn = java.sql.DriverManager.getConnection("jdbc:oracle:thin:@"+x[2]+":"+x[4]+":"+x[3]+"", x[0], x[1])
	stmt = conn.createStatement()
	rs = stmt.executeQuery ("SELECT CE_CLAVE FROM CICLO_ESCOLAR WHERE TO_DATE('"+str(args[1])+"', 'yyyy-mm-dd') + INTERVAL '1' DAY >=  CE_FECHAINI AND TO_DATE('"+str(args[1])+"', 'yyyy-mm-dd') + INTERVAL '1' DAY <= CE_FECHATER")
	resultado = None
	while rs.next():
		resultado = rs.getString(1)
	rs.close()
	stmt.close()
	conn.close()
	return resultado

def ConsultasGenerales2(*args):
	if isJVMStarted() == False:
		classpath = os.getcwd()+"/ojdbcfull/ojdbc6.jar"
		startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + classpath)
	conn = java.sql.DriverManager.getConnection("jdbc:oracle:thin:@"+x[2]+":"+x[4]+":"+x[3]+"", x[0], x[1])
	stmt = conn.createStatement()
	resultado = ''
	rs = stmt.executeQuery ("SELECT MA.MT_NOMBRE, to_char(GRH."+str(args[3])+",'HH24:MI:SS'), to_char(GRH."+str(args[4])+",'HH24:MI:SS'), GR.GR_CLAVE, GRH.GH_RETARDO_TIEMPO, GR.GR_GRUPO FROM MATERIA MA JOIN GRUPO GR ON MA.MT_CLAVE = GR.MT_CLAVE JOIN GRUPO_HORARIO GRH ON GRH.GR_CLAVE = GR.GR_CLAVE WHERE GR.DO_CLAVE = '"+str(args[1])+"' AND GR.CE_CLAVE = '"+str(args[2])+"' AND (('"+str(args[5])+"' >= to_char(GRH."+str(args[3])+",'HH24:MI:SS')) AND ('"+str(args[5])+"' <= to_char(GRH."+str(args[4])+",'HH24:MI:SS')))")
	while rs.next():
		resultado = [rs.getString(1),rs.getString(2),rs.getString(3),rs.getString(4),rs.getString(5),rs.getString(6)]
	rs.close()
	stmt.close()
	conn.close()
	return resultado

def ConsultasGenerales3(*args):
	if isJVMStarted() == False:
		classpath = os.getcwd()+"/ojdbcfull/ojdbc6.jar"
		startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + classpath)
	conn = java.sql.DriverManager.getConnection("jdbc:oracle:thin:@"+x[2]+":"+x[4]+":"+x[3]+"", x[0], x[1])
	stmt = conn.createStatement()
	resultado = [False]
	rs = stmt.executeQuery ("SELECT AL.AL_MATRICULA, AL.AL_NOMBRE, AL.AL_APATERNO, AL.AL_AMATERNO, GH.GH_RETARDO_TIEMPO FROM ALUMNO AL JOIN  ASIGNATURA ASI ON ASI.AL_MATRICULA = AL.AL_MATRICULA JOIN GRUPO GR ON ASI.GR_CLAVE = GR.GR_CLAVE JOIN GRUPO_HORARIO GH ON GH.GR_CLAVE = GR.GR_CLAVE JOIN MATERIA MT ON MT.MT_CLAVE = GR.MT_CLAVE WHERE GR.CE_CLAVE = '"+args[1]+"' AND GR.DO_CLAVE = '"+args[2]+"' AND AL.AL_MATRICULA = '"+args[3]+"' AND GR.GR_CLAVE = '"+args[4]+"' AND (('"+args[5]+"' >= to_char(GH."+args[6]+",'HH24:MI:SS')) AND ('"+args[5]+"' <= to_char(GH."+args[7]+",'HH24:MI:SS')))")
	while rs.next():
		resultado = [True, rs.getString(1), rs.getString(2), rs.getString(3), rs.getString(4), rs.getString(5)]
	rs.close()
	stmt.close()
	conn.close()
	return resultado

def ConsultasGenerales4(*args):
	if isJVMStarted() == False:
		classpath = os.getcwd()+"/ojdbcfull/ojdbc6.jar"
		startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + classpath)
	conn = java.sql.DriverManager.getConnection("jdbc:oracle:thin:@"+x[2]+":"+x[4]+":"+x[3]+"", x[0], x[1])
	stmt = conn.createStatement()

	rs = stmt.executeQuery ("SELECT MAX (AA_CONSECUTIVO) FROM ASISTENCIA WHERE CE_CLAVE = '"+str(args[1])+"' AND AL_MATRICULA='"+str(args[2])+"' AND GR_CLAVE='"+str(args[3])+"'")
	if rs.next():
		if rs.getInt(1)==0:
			cust_id = 1
			if(args[6]==True):
				stmt.executeQuery("INSERT INTO ASISTENCIA(CE_CLAVE, AL_MATRICULA, GR_CLAVE, AA_CONSECUTIVO, FECHA_ENTRADA, RETARDO) VALUES ('"+str(args[1])+"','"+str(args[2])+"','"+str(args[3])+"','"+str(cust_id)+"',TO_DATE('"+str(args[5])+" "+str(args[4])+"','yyyy-mm-dd HH24:MI:SS'), '1')")
				stmt.executeQuery("UPDATE ASISTENCIA t1 SET (t1.HUELLA_ENTRADA) = (SELECT t2.al_huella FROM ALUMNO t2 WHERE t1.AL_MATRICULA = t2.AL_MATRICULA) WHERE t1.AL_MATRICULA='"+str(args[2])+"' AND t1.CE_CLAVE='"+str(args[1])+"' AND t1.GR_CLAVE='"+str(args[3])+"' AND t1.AA_CONSECUTIVO='"+str(cust_id)+"'")
			else:
				stmt.executeQuery("INSERT INTO ASISTENCIA(CE_CLAVE, AL_MATRICULA, GR_CLAVE, AA_CONSECUTIVO, FECHA_ENTRADA) VALUES ('"+str(args[1])+"','"+str(args[2])+"','"+str(args[3])+"','"+str(cust_id)+"',TO_DATE('"+str(args[5])+" "+str(args[4])+"','yyyy-mm-dd HH24:MI:SS'))")
				stmt.executeQuery("UPDATE ASISTENCIA t1 SET (t1.HUELLA_ENTRADA) = (SELECT t2.al_huella FROM ALUMNO t2 WHERE t1.AL_MATRICULA = t2.AL_MATRICULA) WHERE t1.AL_MATRICULA='"+str(args[2])+"' AND t1.CE_CLAVE='"+str(args[1])+"' AND t1.GR_CLAVE='"+str(args[3])+"' AND t1.AA_CONSECUTIVO='"+str(cust_id)+"'")
		else:
			cust_id = rs.getInt(1)+1
			if(args[6]==True):
				stmt.executeQuery("INSERT INTO ASISTENCIA(CE_CLAVE,AL_MATRICULA,GR_CLAVE,AA_CONSECUTIVO,FECHA_ENTRADA, RETARDO) VALUES ('"+str(args[1])+"','"+str(args[2])+"','"+str(args[3])+"','"+str(cust_id)+"',TO_DATE('"+str(args[5])+" "+str(args[4])+"','yyyy-mm-dd HH24:MI:SS'), '1')")
				stmt.executeQuery("UPDATE ASISTENCIA t1 SET (t1.HUELLA_ENTRADA) = (SELECT t2.al_huella FROM ALUMNO t2 WHERE t1.AL_MATRICULA = t2.AL_MATRICULA) WHERE t1.AL_MATRICULA='"+str(args[2])+"' AND t1.CE_CLAVE='"+str(args[1])+"' AND t1.GR_CLAVE='"+str(args[3])+"' AND t1.AA_CONSECUTIVO='"+str(cust_id)+"'")
			else:
				stmt.executeQuery("INSERT INTO ASISTENCIA(CE_CLAVE,AL_MATRICULA,GR_CLAVE,AA_CONSECUTIVO,FECHA_ENTRADA) VALUES ('"+str(args[1])+"','"+str(args[2])+"','"+str(args[3])+"','"+str(cust_id)+"',TO_DATE('"+str(args[5])+" "+str(args[4])+"','yyyy-mm-dd HH24:MI:SS'))")
				stmt.executeQuery("UPDATE ASISTENCIA t1 SET (t1.HUELLA_ENTRADA) = (SELECT t2.al_huella FROM ALUMNO t2 WHERE t1.AL_MATRICULA = t2.AL_MATRICULA) WHERE t1.AL_MATRICULA='"+str(args[2])+"' AND t1.CE_CLAVE='"+str(args[1])+"' AND t1.GR_CLAVE='"+str(args[3])+"' AND t1.AA_CONSECUTIVO='"+str(cust_id)+"'")
	rs.close()
	stmt.close()
	conn.close()
	

def ConsultasGenerales5(*args):
	if isJVMStarted() == False:
		classpath = os.getcwd()+"/ojdbcfull/ojdbc6.jar"
		startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + classpath)
	conn = java.sql.DriverManager.getConnection("jdbc:oracle:thin:@"+x[2]+":"+x[4]+":"+x[3]+"", x[0], x[1])
	stmt = conn.createStatement()
	resultado = [False]
	rs = stmt.executeQuery("SELECT AL.AL_MATRICULA, ASIS.FECHA_ENTRADA, ASIS.FECHA_SALIDA, ASIS.AA_CONSECUTIVO  FROM ALUMNO AL JOIN  ASIGNATURA ASI ON ASI.AL_MATRICULA = AL.AL_MATRICULA JOIN GRUPO GR ON ASI.GR_CLAVE = GR.GR_CLAVE JOIN GRUPO_HORARIO GH ON GH.GR_CLAVE = GR.GR_CLAVE JOIN MATERIA MT ON MT.MT_CLAVE = GR.MT_CLAVE JOIN ASISTENCIA ASIS ON ASIS.AL_MATRICULA = AL.AL_MATRICULA WHERE GR.CE_CLAVE = '"+args[1]+"' AND GR.DO_CLAVE = '"+args[2]+"' AND AL.AL_MATRICULA = '"+args[3]+"' AND GR.GR_CLAVE = '"+args[4].replace(' ', '')+"' AND (('"+args[5]+"' >= to_char(GH."+args[6]+",'HH24:MI:SS')) AND ('"+args[5]+"' <= to_char(GH."+args[7]+",'HH24:MI:SS'))) AND (('"+args[8]+"' >= to_char(ASIS.FECHA_ENTRADA,'yyyy-mm-dd')) AND ('"+args[8]+"' <= to_char(ASIS.FECHA_ENTRADA,'yyyy-mm-dd')))")
	if rs.next():
		resultado =  [True, rs.getString(1), rs.getString(2), rs.getString(3), rs.getString(4)]
	rs.close()
	stmt.close()
	conn.close()
	return resultado

def ConsultasGenerales6(*args):
	if isJVMStarted() == False:
		classpath = os.getcwd()+"/ojdbcfull/ojdbc6.jar"
		startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + classpath)
	conn = java.sql.DriverManager.getConnection("jdbc:oracle:thin:@"+x[2]+":"+x[4]+":"+x[3]+"", x[0], x[1])
	stmt = conn.createStatement()
	stmt.executeQuery ("UPDATE ASISTENCIA SET FECHA_SALIDA = TO_DATE('"+str(args[3])+" "+str(args[2])+"','yyyy-mm-dd HH24:MI:SS') WHERE AA_CONSECUTIVO = "+args[1])
	stmt.executeQuery ("UPDATE ASISTENCIA t1 SET (t1.HUELLA_SALIDA) = (SELECT t2.al_huella FROM ALUMNO t2 WHERE t1.AL_MATRICULA = t2.AL_MATRICULA) WHERE t1.AA_CONSECUTIVO='"+args[1]+"'")
	stmt.close()
	conn.close()

def ConsultasGenerales7(*args):
	if isJVMStarted() == False:
		classpath = os.getcwd()+"/ojdbcfull/ojdbc6.jar"
		startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + classpath)
	conn = java.sql.DriverManager.getConnection("jdbc:oracle:thin:@"+x[2]+":"+x[4]+":"+x[3]+"", x[0], x[1])
	stmt = conn.createStatement()
	resultado = ''
	#SELECT DO_NOMBRE, DO_APATERNO, DO_AMATERNO FROM DOCENTE WHERE DO_CLAVE='1111';
	rs = stmt.executeQuery ("SELECT DO_NOMBRE, DO_APATERNO, DO_AMATERNO FROM DOCENTE WHERE DO_CLAVE='"+str(args[1])+"'")
	while rs.next():
		resultado = [rs.getString(1), rs.getString(2), rs.getString(3)]
	rs.close()
	stmt.close()
	conn.close()
	return resultado

def ConsultasGenerales8(*args):
	if isJVMStarted() == False:
		classpath = os.getcwd()+"/ojdbcfull/ojdbc6.jar"
		startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + classpath)
	conn = java.sql.DriverManager.getConnection("jdbc:oracle:thin:@"+x[2]+":"+x[4]+":"+x[3]+"", x[0], x[1])
	stmt = conn.createStatement()
	resultado = ''
	SQL = ''
	#HORA
	if(args[1]==0):
		SQL = "SELECT TO_CHAR(SYSDATE, 'HH24:MI:SS') FROM DUAL"
	#FECHA
	elif(args[1]==1):
		SQL = "SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD') FROM DUAL"
	#HORA FECHA
	elif(args[1]==2):
		SQL = "SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') FROM DUAL"
	elif(args[1]==3):
		SQL = "SELECT TO_CHAR(SYSDATE, 'DD-MM-YYYY') FROM DUAL"
	rs = stmt.executeQuery (SQL)
	while rs.next():
		resultado = rs.getString(1)
	rs.close()
	stmt.close()
	conn.close()
	return resultado

def ConsultasGenerales9(*args):
	if isJVMStarted() == False:
		classpath = os.getcwd()+"/ojdbcfull/ojdbc6.jar"
		startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + classpath)
	conn = java.sql.DriverManager.getConnection("jdbc:oracle:thin:@"+x[2]+":"+x[4]+":"+x[3]+"", x[0], x[1])
	stmt = conn.createStatement()
	resultado = False
	rs = stmt.executeQuery("SELECT AL.AL_MATRICULA FROM ALUMNO AL JOIN  ASIGNATURA ASI ON ASI.AL_MATRICULA = AL.AL_MATRICULA JOIN GRUPO GR ON ASI.GR_CLAVE = GR.GR_CLAVE JOIN GRUPO_HORARIO GH ON GH.GR_CLAVE = GR.GR_CLAVE WHERE GR.CE_CLAVE = '"+args[1]+"' AND GR.DO_CLAVE = '"+args[2]+"' AND AL.AL_MATRICULA = '"+args[3]+"' AND GR.GR_CLAVE = '"+args[4]+"' AND '"+args[5]+"' > to_char(GH."+args[6]+"+INTERVAL '"+args[7]+"' MINUTE,'HH24:MI:SS')")
	while rs.next():
		resultado = True
	rs.close()
	stmt.close()
	conn.close()
	return resultado

def ConsultasGenerales10(*args):
	if isJVMStarted() == False:
		classpath = os.getcwd()+"/ojdbcfull/ojdbc6.jar"
		startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + classpath)
	conn = java.sql.DriverManager.getConnection("jdbc:oracle:thin:@"+x[2]+":"+x[4]+":"+x[3]+"", x[0], x[1])
	stmt = conn.createStatement()
	resultado = False
	rs = stmt.executeQuery("SELECT TO_CHAR(SYSDATE, 'DAY') FROM DUAL")
	while rs.next():
		resultado = rs.getString(1)
	rs.close()
	stmt.close()
	conn.close()
	return resultado


def ConsultasGenerales11(*args):
	if isJVMStarted() == False:
		classpath = os.getcwd()+"/ojdbcfull/ojdbc6.jar"
		startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + classpath)
	conn = java.sql.DriverManager.getConnection("jdbc:oracle:thin:@"+x[2]+":"+x[4]+":"+x[3]+"", x[0], x[1])
	stmt = conn.createStatement()

	rs = stmt.executeQuery ("SELECT MAX (AA_CONSECUTIVO) FROM ASISTENCIA WHERE CE_CLAVE = '"+str(args[1])+"' AND AL_MATRICULA='"+str(args[2])+"' AND GR_CLAVE='"+str(args[3])+"'")
	if rs.next():
		if rs.getInt(1)==0:
			cust_id = 1
			if(args[6]==True):
				stmt.executeQuery("INSERT INTO ASISTENCIA(CE_CLAVE, AL_MATRICULA, GR_CLAVE, AA_CONSECUTIVO, FECHA_ENTRADA, RETARDO) VALUES ('"+str(args[1])+"','"+str(args[2])+"','"+str(args[3])+"','"+str(cust_id)+"',TO_DATE('"+str(args[5])+" "+str(args[4])+"','yyyy-mm-dd HH24:MI:SS'), '1')")
				stmt.executeQuery("UPDATE ASISTENCIA t1 SET (t1.VOZ_ENTRADA) = (SELECT t2.al_voz FROM ALUMNO t2 WHERE t1.AL_MATRICULA = t2.AL_MATRICULA) WHERE t1.AL_MATRICULA='"+str(args[2])+"' AND t1.CE_CLAVE='"+str(args[1])+"' AND t1.GR_CLAVE='"+str(args[3])+"' AND t1.AA_CONSECUTIVO='"+str(cust_id)+"'")
			else:
				stmt.executeQuery("INSERT INTO ASISTENCIA(CE_CLAVE, AL_MATRICULA, GR_CLAVE, AA_CONSECUTIVO, FECHA_ENTRADA) VALUES ('"+str(args[1])+"','"+str(args[2])+"','"+str(args[3])+"','"+str(cust_id)+"',TO_DATE('"+str(args[5])+" "+str(args[4])+"','yyyy-mm-dd HH24:MI:SS'))")
				stmt.executeQuery("UPDATE ASISTENCIA t1 SET (t1.VOZ_ENTRADA) = (SELECT t2.al_voz FROM ALUMNO t2 WHERE t1.AL_MATRICULA = t2.AL_MATRICULA) WHERE t1.AL_MATRICULA='"+str(args[2])+"' AND t1.CE_CLAVE='"+str(args[1])+"' AND t1.GR_CLAVE='"+str(args[3])+"' AND t1.AA_CONSECUTIVO='"+str(cust_id)+"'")
		else:
			cust_id = rs.getInt(1)+1
			if(args[6]==True):
				stmt.executeQuery("INSERT INTO ASISTENCIA(CE_CLAVE,AL_MATRICULA,GR_CLAVE,AA_CONSECUTIVO,FECHA_ENTRADA, RETARDO) VALUES ('"+str(args[1])+"','"+str(args[2])+"','"+str(args[3])+"','"+str(cust_id)+"',TO_DATE('"+str(args[5])+" "+str(args[4])+"','yyyy-mm-dd HH24:MI:SS'), '1')")
				stmt.executeQuery("UPDATE ASISTENCIA t1 SET (t1.VOZ_ENTRADA) = (SELECT t2.al_voz FROM ALUMNO t2 WHERE t1.AL_MATRICULA = t2.AL_MATRICULA) WHERE t1.AL_MATRICULA='"+str(args[2])+"' AND t1.CE_CLAVE='"+str(args[1])+"' AND t1.GR_CLAVE='"+str(args[3])+"' AND t1.AA_CONSECUTIVO='"+str(cust_id)+"'")
			else:
				stmt.executeQuery("INSERT INTO ASISTENCIA(CE_CLAVE,AL_MATRICULA,GR_CLAVE,AA_CONSECUTIVO,FECHA_ENTRADA) VALUES ('"+str(args[1])+"','"+str(args[2])+"','"+str(args[3])+"','"+str(cust_id)+"',TO_DATE('"+str(args[5])+" "+str(args[4])+"','yyyy-mm-dd HH24:MI:SS'))")
				stmt.executeQuery("UPDATE ASISTENCIA t1 SET (t1.VOZ_ENTRADA) = (SELECT t2.al_voz FROM ALUMNO t2 WHERE t1.AL_MATRICULA = t2.AL_MATRICULA) WHERE t1.AL_MATRICULA='"+str(args[2])+"' AND t1.CE_CLAVE='"+str(args[1])+"' AND t1.GR_CLAVE='"+str(args[3])+"' AND t1.AA_CONSECUTIVO='"+str(cust_id)+"'")
	rs.close()
	stmt.close()
	conn.close()

def ConsultasGenerales12(*args):
	if isJVMStarted() == False:
		classpath = os.getcwd()+"/ojdbcfull/ojdbc6.jar"
		startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + classpath)
	conn = java.sql.DriverManager.getConnection("jdbc:oracle:thin:@"+x[2]+":"+x[4]+":"+x[3]+"", x[0], x[1])
	stmt = conn.createStatement()
	stmt.executeQuery ("UPDATE ASISTENCIA SET FECHA_SALIDA = TO_DATE('"+str(args[3])+" "+str(args[2])+"','yyyy-mm-dd HH24:MI:SS') WHERE AA_CONSECUTIVO = "+args[1])
	stmt.executeQuery ("UPDATE ASISTENCIA t1 SET (t1.VOZ_SALIDA) = (SELECT t2.al_voz FROM ALUMNO t2 WHERE t1.AL_MATRICULA = t2.AL_MATRICULA) WHERE t1.AA_CONSECUTIVO='"+args[1]+"'")
	stmt.close()
	conn.close()

def ConsultasGenerales13(*args):
	if isJVMStarted() == False:
		classpath = os.getcwd()+"/ojdbcfull/ojdbc6.jar"
		startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + classpath)
	conn = java.sql.DriverManager.getConnection("jdbc:oracle:thin:@"+x[2]+":"+x[4]+":"+x[3]+"", x[0], x[1])
	stmt = conn.createStatement()
	
	RANGO_CE = stmt.executeQuery("SELECT TO_CHAR(CE_FECHAINI, 'DD/MM/YY'), TO_CHAR(CE_FECHATER, 'DD/MM/YY') FROM CICLO_ESCOLAR WHERE CE_CLAVE='"+self.cicloE+"'")
	ASISTENCIAS = stmt.executeQuery("SELECT A.AL_MATRICULA , COUNT(*) FROM ALUMNO A JOIN ASISTENCIA AC ON A.AL_MATRICULA = AC.AL_MATRICULA WHERE AC.CE_CLAVE = '"+self.cicloE+"'  AND AC.GR_CLAVE = '"+self.cGrupo+"' AND  A.AL_MATRICULA = '"+self.matricula+"' AND AC.JUSTIFICACION IS NULL AND AC.RETARDO IS NULL AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0][0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[0][1])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0][0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[0][1])+"', 'DD/MM/YY') GROUP BY A.AL_MATRICULA").fetchall()
        JUSTIFICACIONES = stmt.executeQuery("SELECT A.AL_MATRICULA , COUNT(*) FROM ALUMNO A JOIN ASISTENCIA AC ON A.AL_MATRICULA = AC.AL_MATRICULA WHERE AC.CE_CLAVE = '"+self.cicloE+"'  AND AC.GR_CLAVE = '"+self.cGrupo+"' AND  A.AL_MATRICULA = '"+self.matricula+"' AND AC.JUSTIFICACION IS NOT NULL AND AC.RETARDO IS NULL AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0][0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[0][1])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0][0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[0][1])+"', 'DD/MM/YY') GROUP BY A.AL_MATRICULA").fetchall()

        RETARDOS = stmt.executeQuery("SELECT A.AL_MATRICULA , COUNT(*) FROM ALUMNO A JOIN ASISTENCIA AC ON A.AL_MATRICULA = AC.AL_MATRICULA WHERE AC.CE_CLAVE = '"+self.cicloE+"'  AND AC.GR_CLAVE = '"+self.cGrupo+"' AND  A.AL_MATRICULA = '"+self.matricula+"' AND AC.RETARDO IS NOT NULL AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0][0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[0][1])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0][0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[0][1])+"', 'DD/MM/YY') GROUP BY A.AL_MATRICULA").fetchall()
        TOTAL_ASISTENCIAS = 0
        TOTAL_JUSTIFICACIONES = 0
        TOTAL_RETARDOS = 0
	while rs.next():
		resultado = rs.getString(1)
	rs.close()
	stmt.close()
	conn.close()
	return resultado
    
def ConsultasReportes(cicloEscolar, Matricula, ClaveGrupo):
	if isJVMStarted() == False:
		classpath = os.getcwd()+"/ojdbcfull/ojdbc6.jar"
		startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + classpath)
	conn = java.sql.DriverManager.getConnection("jdbc:oracle:thin:@"+x[2]+":"+x[4]+":"+x[3]+"", x[0], x[1])
	stmt = conn.createStatement()
	
	rs1 = stmt.executeQuery("SELECT AL_EMAIL FROM ALUMNO WHERE AL_MATRICULA = '"+Matricula+"'")
	CORREO = ''
	while rs1.next():
		CORREO = rs1.getString(1)

	if CORREO != None:
		try:
			rs1 = stmt.executeQuery ("SELECT TO_CHAR(CE_FECHAINI, 'DD/MM/YY'), TO_CHAR(CE_FECHATER, 'DD/MM/YY') FROM CICLO_ESCOLAR WHERE CE_CLAVE='"+cicloEscolar+"'")
			RANGO_CE = [None, None]
			while rs1.next():
				RANGO_CE = [rs1.getString(1),rs1.getString(2)]

			rs1 = stmt.executeQuery ("SELECT A.AL_MATRICULA , COUNT(*) FROM ALUMNO A JOIN ASISTENCIA AC ON A.AL_MATRICULA = AC.AL_MATRICULA WHERE AC.CE_CLAVE = '"+cicloEscolar+"'  AND AC.GR_CLAVE = '"+ClaveGrupo+"' AND  A.AL_MATRICULA = '"+Matricula+"' AND AC.JUSTIFICACION IS NULL AND AC.RETARDO IS NULL AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[1])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[1])+"', 'DD/MM/YY') GROUP BY A.AL_MATRICULA")
			ASISTENCIAS = [Matricula,0]
			while rs1.next():
				ASISTENCIAS = [rs1.getString(1),rs1.getString(2)]

			rs1 = stmt.executeQuery ("SELECT A.AL_MATRICULA , COUNT(*) FROM ALUMNO A JOIN ASISTENCIA AC ON A.AL_MATRICULA = AC.AL_MATRICULA WHERE AC.CE_CLAVE = '"+cicloEscolar+"'  AND AC.GR_CLAVE = '"+ClaveGrupo+"' AND  A.AL_MATRICULA = '"+Matricula+"' AND AC.JUSTIFICACION IS NOT NULL AND AC.RETARDO IS NULL AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[1])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[1])+"', 'DD/MM/YY') GROUP BY A.AL_MATRICULA")
			JUSTIFICACIONES = [Matricula,0]
			while rs1.next():
				JUSTIFICACIONES = [rs1.getString(1),rs1.getString(2)]

			rs1 = stmt.executeQuery ("SELECT A.AL_MATRICULA , COUNT(*) FROM ALUMNO A JOIN ASISTENCIA AC ON A.AL_MATRICULA = AC.AL_MATRICULA WHERE AC.CE_CLAVE = '"+cicloEscolar+"'  AND AC.GR_CLAVE = '"+ClaveGrupo+"' AND  A.AL_MATRICULA = '"+Matricula+"' AND AC.RETARDO IS NOT NULL AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_ENTRADA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[1])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') >= TO_DATE('"+str(RANGO_CE[0])+"', 'DD/MM/YY') AND TO_DATE(AC.FECHA_SALIDA, 'DD/MM/YY') <= TO_DATE('"+str(RANGO_CE[1])+"', 'DD/MM/YY') GROUP BY A.AL_MATRICULA")
			RETARDOS = [Matricula,0]
			while rs1.next():
				RETARDOS = [rs1.getString(1),rs1.getString(2)]

			TOTAL_ASISTENCIAS = 0
			TOTAL_JUSTIFICACIONES = 0
			TOTAL_RETARDOS = 0

			if len(ASISTENCIAS)>0:
				TOTAL_ASISTENCIAS = int(ASISTENCIAS[1])
			else:
				TOTAL_ASISTENCIAS = 0
			if len(JUSTIFICACIONES)>0:
				TOTAL_JUSTIFICACIONES = int(JUSTIFICACIONES[1])
			else:
				TOTAL_JUSTIFICACIONES = 0
			if len(RETARDOS)>0:
				TOTAL_RETARDOS = int(RETARDOS[1])
			else:
				TOTAL_RETARDOS = 0

			rs1 = stmt.executeQuery ("SELECT AL_NOMBRE, AL_APATERNO, AL_AMATERNO FROM ALUMNO WHERE AL_MATRICULA = '"+Matricula+"'")
			NOMBRE = ''
			while rs1.next():
				if(rs1.getString(3)!=None):
					NOMBRE = str(rs1.getString(1))+' '+str(rs1.getString(2))+' '+str(rs1.getString(3))
				else:
					NOMBRE = str(rs1.getString(1))+' '+str(rs1.getString(2))

			rs1 = stmt.executeQuery ("SELECT DO.DO_NOMBRE, DO.DO_APATERNO, DO.DO_AMATERNO FROM DOCENTE DO JOIN GRUPO GR ON DO.DO_CLAVE = GR.DO_CLAVE WHERE GR.CE_CLAVE = '"+cicloEscolar+"' AND GR.GR_CLAVE = '"+ClaveGrupo+"'")
			DOCENTE = ''
			while rs1.next():
				if(rs1.getString(3)!=None):
					DOCENTE = str(rs1.getString(1))+' '+str(rs1.getString(2))+' '+str(rs1.getString(3))
				else:
					DOCENTE = str(rs1.getString(1))+' '+str(rs1.getString(2))

			rs1 = stmt.executeQuery ("SELECT PE.PL_NOMBRE FROM PLAN_ESTUDIO PE JOIN GRUPO GR ON GR.PL_CLAVE = PE.PL_CLAVE WHERE GR.CE_CLAVE = '"+cicloEscolar+"' AND GR.GR_CLAVE = '"+ClaveGrupo+"'")
			PROGRAMA_ACADEMICO = ''
			while rs1.next():
				PROGRAMA_ACADEMICO = str(rs1.getString(1))

			rs1 = stmt.executeQuery ("SELECT MT.MT_NOMBRE FROM MATERIA MT JOIN  GRUPO GR ON MT.MT_CLAVE = GR.MT_CLAVE WHERE GR.CE_CLAVE = '"+cicloEscolar+"' AND GR.GR_CLAVE = '"+ClaveGrupo+"'")
			NOMBRE_MATERIA = ''
			while rs1.next():
				NOMBRE_MATERIA = str(rs1.getString(1))

			rs1 = stmt.executeQuery ("SELECT CE_DESCRIPCION FROM CICLO_ESCOLAR WHERE CE_CLAVE = '"+cicloEscolar+"'")
			CICLO_ESCOLAR = ''
			while rs1.next():
				CICLO_ESCOLAR = str(rs1.getString(1))

			rs1 = stmt.executeQuery ("SELECT GR_TOTAL_SESIONES FROM GRUPO WHERE CE_CLAVE = '"+cicloEscolar+"' AND GR_CLAVE = '"+ClaveGrupo+"'")
			SESIONES = 0
			while rs1.next():
				SESIONES = int(rs1.getString(1))

			rs1 = stmt.executeQuery ("SELECT GH_TOTAL_RETARDO_ASISTENCIA FROM GRUPO_HORARIO WHERE CE_CLAVE = '"+cicloEscolar+"' AND GR_CLAVE = '"+ClaveGrupo+"'")
			RETARDO_AISTENCIA = 0
			while rs1.next():
				if rs1.getString(1) != None:
					RETARDO_AISTENCIA = int(rs1.getString(1))

    			#HISTORIALES = ['SIN DATOS','SIN DATOS','SIN DATOS','SIN DATOS','SIN DATOS','SIN DATOS']
                        datos = []					
			rs1 = stmt.executeQuery("SELECT AL_MATRICULA, AA_CONSECUTIVO, TO_CHAR(FECHA_ENTRADA,'DD/MM/YYYY HH24:MI:SS') , TO_CHAR(FECHA_SALIDA,'DD/MM/YYYY HH24:MI:SS'), RETARDO, JUSTIFICACION FROM ASISTENCIA WHERE CE_CLAVE = '"+cicloEscolar+"' AND AL_MATRICULA = '"+Matricula+"' AND GR_CLAVE = '"+ClaveGrupo+"'")	
                        while rs1.next():
                            
                            if  rs1.getString(4) == None:
                                    fs = ''
                            else:
                                    fs = rs1.getString(4)
                            if rs1.getString(5) == None:
                                    r = ''
                            else:
                                    r = rs1.getString(5)
                            if rs1.getString(6) == None:
                                    j = ''
                            else:
                                    j = rs1.getString(6)
                            datos.append((rs1.getString(2),rs1.getString(3),fs,r,j))    

			rs1.close()
			stmt.close()
			conn.close()

			f = open (os.getcwd() + "/LOGIN/EVALC.bin",'r')
			clave = f.read()
			f.close()
			clave = base64.b64decode(clave)
			print datos
			reportesasistencia.generarReporteAlumno(str(Matricula), str(NOMBRE), str(DOCENTE), str(NOMBRE_MATERIA), str(CICLO_ESCOLAR), int(TOTAL_ASISTENCIAS) + int(TOTAL_JUSTIFICACIONES), str(PROGRAMA_ACADEMICO), int(TOTAL_RETARDOS), int(SESIONES), int(RETARDO_AISTENCIA), datos)
			status = envioReportes.EnviarCorreo(clave, CORREO, NOMBRE, NOMBRE_MATERIA)

			if status == True:
				return 2
			else:
				return 3
		except:
			return 4
	
	else:
		rs1.close()
		stmt.close()
		conn.close()
		return 1
	    


#print(str(ConsultasGenerales5(3,'1920SNON','1111','55555555','4       ','10:10:11','GH_MARTESINI','GH_MARTESTER','2020-01-09')))
