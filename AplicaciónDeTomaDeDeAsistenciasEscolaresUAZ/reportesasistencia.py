# -*- coding: utf-8 -*-
#pip install reportlab
#python -m pip install --upgrade pip
#pip install --upgrade --force-reinstall reportlab
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os
from datetime import datetime
def multiple(valor, multiple):
    """
    Funcion para calcular si el numero es multiplo
    utilizando el modulo de la division
    """
    resto = valor % multiple
    if resto == 0:
        return True
    else:
        return False

 
def generarReporteAlumno(Matricula,NombreAlumno,Docente,Curso,CicloEscolar,TotalAsistencias,ProgramaAcademico,Retardos,ClasesTotales,RETARDO_ASISTENCIA,hist):
    doc = SimpleDocTemplate(os.getcwd()+"/REPORTES/reporte.pdf", pagesize=letter,rightMargin=72, leftMargin=72,topMargin=72, bottomMargin=18)
    Story = []
    logotipo = os.getcwd()+"/icons/uaz2.jpg"
    Universisdad = "BENÉMERITA UNIVERSIDAD AUTÓNOMA DE ZACATECAS"
    nombre = '"Fracisco García Salinas"'
    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name='Titulo', alignment=TA_CENTER, fontSize = 15, borderColor = 'black', fontName = "Times-Bold", spaceAfter = 50))
    texto = '%s' % Universisdad
    Story.append(Paragraph(texto, estilos["Titulo"]))
    resto = 0
    if(Retardos != 0):
        resto = Retardos % RETARDO_ASISTENCIA
    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name='Titulo1', alignment=TA_CENTER, fontSize = 12, borderColor = 'black', fontName = "Times-Bold", spaceAfter = 50))
    texto = '%s' % nombre
    Story.append(Paragraph(texto, estilos["Titulo1"]))


    imagen = Image(logotipo, 2 * inch, 2 * inch)
    Story.append(imagen)

    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name='Cuerpo', alignment = TA_JUSTIFY, fontSize = 12, borderColor = 'black', fontName = "Times-Roman", spaceBefore = 50, leading = 15))
    texto = 'El alumno %s inscrito dentro del programa %s con la matrícula %s que se encuentra cursando la materia de %s con el docente %s obtuvo el siguiente reporte de asistencias dentro del ciclo escolar %s:' % (NombreAlumno,ProgramaAcademico,Matricula,Curso,Docente,CicloEscolar)
    Story.append(Paragraph(texto, estilos["Cuerpo"]))
    
    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name='Asistencia', alignment = TA_JUSTIFY, fontSize = 12, borderColor = 'black', fontName = "Times-Roman", spaceBefore = 30))
    texto = 'HISTORIAL DE ASISTENCIAS\n\n' 
    Story.append(Paragraph(texto, estilos["Asistencia"]))

    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name='Asistencia', alignment = TA_JUSTIFY, fontSize = 12, borderColor = 'black', fontName = "Times-Roman", spaceBefore = 30))
    texto = '' 
    Story.append(Paragraph(texto, estilos["Asistencia"]))

    datos = [
        ('NO.', 'FECHA ENTRADA', 'FECHA SALIDA', 'RETARDO', 'JUSTIFICA'),
        ]
    datos.extend(hist)
    #AL_MATRICULA, AA_CONSECUTIVO, TO_CHAR(FECHA_ENTRADA,'DD/MM/YYYY HH24:MI:SS') , TO_CHAR(FECHA_SALIDA,'DD/MM/YYYY HH24:MI:SS'), RETARDO, JUSTIFICACION
    """for asis in HISTORIAL:
        if asis[3] == None:
            fs = ''
        else:
            fs = asis[3]
        if asis[4] == None:
            r = ''
        else:
            r = asis[4]
        if asis[5] == None:
            j = ''
        else:
            j = asis[5]
        datos.append((asis[1],asis[2],fs,r,j))"""

    tabla = Table(data = datos,
              style = [
                       ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                       ('BOX',(0,0),(-1,-1),2,colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                       ]
              )
    Story.append(tabla)
    Story.append(Spacer(5,5))

    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name='Asistencia', alignment = TA_JUSTIFY, fontSize = 12, borderColor = 'black', fontName = "Times-Roman", spaceBefore = 30))
    texto = 'Se impartieron un total de %s clases' % (ClasesTotales)
    Story.append(Paragraph(texto, estilos["Asistencia"]))
    
    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name='Asistencia', alignment = TA_JUSTIFY, fontSize = 12, borderColor = 'black', fontName = "Times-Roman", spaceBefore = 12))
    texto = 'El alumno asistio a un total de clases %s' % str(int(TotalAsistencias)+int(Retardos))
    asistencia = TotalAsistencias+resto
    Story.append(Paragraph(texto, estilos["Asistencia"]))
    totalAsistencia = 0
    
    if RETARDO_ASISTENCIA != 0:
        count = Retardos/RETARDO_ASISTENCIA
        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='Asistencia', alignment = TA_JUSTIFY, fontSize = 12, borderColor = 'black', fontName = "Times-Roman", spaceBefore = 12))
        texto = 'Cada '+str(RETARDO_ASISTENCIA)+' retardos equivalen a 1 Falta, por lo tanto, el alumno obtuvo un total de retardos ' +str(Retardos)+' que equivalen a ' + str(count) +' faltas'
        Story.append(Paragraph(texto, estilos["Asistencia"]))
        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='Asistencia', alignment = TA_JUSTIFY, fontSize = 12, borderColor = 'black', fontName = "Times-Roman", spaceBefore = 12))
        texto = 'El alumno falto un total de clases %s' % (ClasesTotales-(TotalAsistencias+Retardos-count))
        Story.append(Paragraph(texto, estilos["Asistencia"]))
        totalAsistencia = ((ClasesTotales-(ClasesTotales-(TotalAsistencias+Retardos-count)))*100)/ClasesTotales
    else:
        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='Asistencia', alignment = TA_JUSTIFY, fontSize = 12, borderColor = 'black', fontName = "Times-Roman", spaceBefore = 12))
        texto = 'El alumno falto un total de clases %s' % (ClasesTotales-(TotalAsistencias+Retardos))
        Story.append(Paragraph(texto, estilos["Asistencia"]))
        totalAsistencia = ((ClasesTotales-(ClasesTotales-(TotalAsistencias+Retardos)))*100)/ClasesTotales

    
    

    

    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name='Asistencia', alignment = TA_JUSTIFY, fontSize = 12, borderColor = 'black', fontName = "Times-Roman", spaceBefore = 30, leading = 15))
    texto = 'El porcentaje final de asistencia del alumno %s con matricula %s durante el curso de %s fue del %s porciento.' % (NombreAlumno,Matricula,Curso,totalAsistencia)
    Story.append(Paragraph(texto, estilos["Asistencia"]))
    

    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name='Final', alignment = TA_RIGHT, fontSize = 12, borderColor = 'black', fontName = "Times-Roman", spaceBefore = 30, leading = 15))
    texto = '%s, Zacatecas, Zacatecas, México' % (datetime.now())
    Story.append(Paragraph(texto, estilos["Final"]))
    doc.build(Story)



#generarReporteAlumno("35161479","EMMANUEL DE JESUS VELASQUEZ MARTINEZ","PEDRO LUIS MTZ","REDES","2019-NON",32,"INGENIERIA EN COMPUTACION",8,2,52)

