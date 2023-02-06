from __future__ import print_function
import os, time, datetime, pyfprint, commands, sys
from os import remove
def user():
	ESTADOS = 0
	pyfprint.fp_init()
	devs = pyfprint.discover_devices()
	if str(devs) == '[]':
		pyfprint.fp_exit()
		return 'LD'
	else:
		dev = devs[0]
		dev.open()
		fpsEntrada = []
		ClavesEntrada = []
		for name in os.listdir(os.getcwd()+"/auxHuella/JUSTIFICACIONES/"):
			fpsEntrada.append(pyfprint.Fprint(open(os.getcwd() + "/auxHuella/JUSTIFICACIONES/" + name, 'rb').read()))
			ClavesEntrada.append(name)
		i, fp, img, r = dev.identify_finger(fpsEntrada)
		if i != None:
			for name in os.listdir(os.getcwd()+"/auxHuella/JUSTIFICACIONES/"):
				remove(os.getcwd() + "/auxHuella/JUSTIFICACIONES/" + name)
			dev.close()
			pyfprint.fp_exit()
			return str(ClavesEntrada[i])
		else:
			for name in os.listdir(os.getcwd()+"/auxHuella/JUSTIFICACIONES/"):
				remove(os.getcwd() + "/auxHuella/JUSTIFICACIONES/" + name)
			dev.close()
			pyfprint.fp_exit()
			return 'SIN RESULTADOS'
			

