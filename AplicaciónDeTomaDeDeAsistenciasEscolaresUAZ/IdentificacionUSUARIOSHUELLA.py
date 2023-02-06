from __future__ import print_function
import os, pyfprint, time

def user():
	pyfprint.fp_init()
	devs = pyfprint.discover_devices()
	if len(devs)==0:
		pyfprint.fp_exit()
		return [0]
	else:
		dev = devs[0]
		dev.open()
		fpsEntrada = []
		ClavesEntrada = []
		for name in os.listdir(os.getcwd()+"/HUELLAS/"):
			fpsEntrada.append(pyfprint.Fprint(open(os.getcwd() + "/HUELLAS/" + name, 'rb').read()))
			ClavesEntrada.append(name)
		time.sleep(1)
		i, fp, img, r = dev.identify_finger(fpsEntrada)
		if i != None:
			if(len(ClavesEntrada[i].replace('\n', ' ').replace('\r', '').replace(" ", ""))==4):
				print("Es un docente: "+str(ClavesEntrada[i].replace('\n', ' ').replace('\r', '').replace(" ", "")))
				dev.close()
				pyfprint.fp_exit()
				f = open (os.getcwd() + "/LOGIN/LOGIN.txt",'w')
				f.write(ClavesEntrada[i].replace('\n', ' ').replace('\r', '').replace(" ", ""))
				f.close()
				return [1, ClavesEntrada[i].replace('\n', ' ').replace('\r', '').replace(" ", "")]
			else:
				print("Es un alumno: "+str(ClavesEntrada[i].replace('\n', ' ').replace('\r', '').replace(" ", "")))
				dev.close()
				pyfprint.fp_exit()
				return [2, ClavesEntrada[i].replace('\n', ' ').replace('\r', '').replace(" ", "")]
		else:
			dev.close()
			pyfprint.fp_exit()
			return [3]