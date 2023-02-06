import re

def Correo(cadena):	
	patron="[A-Za-z]+((.+|_+)([a-z]+|(\d+)))?@[A-Za-z]+.com$"
    	if(re.match(patron,cadena)):
		return True	
    	else:
        	return False
                             
def Nombres(cadena):
		
    	patron="[A-Za-z(\s)]+$"
    	if(re.match(patron,cadena)):
        	return True
    	else:
        	return False

def Apellidos(cadena):
    	patron="[A-Za-z]+$"
    	if(re.match(patron,cadena)):
        	return True
    	else:
        	return False

def Entero(cadena):
    	patron="([0-9]{1,4})+$"
    	if(re.match(patron,cadena)):
        	return True
    	else:
        	return False

def comprobar_fecha(a, m, d):
	#Array que almacenara los dias que tiene cada mes (si el ano es bisiesto, sumaremos +1 al febrero)
	dias_mes = [31, 28, 31, 30,31, 30, 31, 31, 30, 31, 30, 31]
	#Comprobar si el ano es bisiesto y anadir dia en febrero en caso afirmativo
	if((a%4 == 0 and a%100 != 0) or a%400 == 0):
		dias_mes[1] += 1
	#Comprobar que el mes sea valido
	if(m < 1 or m > 12):
		return False
	#Comprobar que el dia sea valido
	m -= 1
	if(d <= 0 or d > dias_mes[m]):
		return False
	#Si ha pasado todas estas condiciones, la fecha es valida
	return True
