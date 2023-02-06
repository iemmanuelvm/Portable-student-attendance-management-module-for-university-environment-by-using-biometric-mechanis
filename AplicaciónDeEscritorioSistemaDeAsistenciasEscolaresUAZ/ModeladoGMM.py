# -*- coding: utf-8 -*-
import cPickle, warnings, os
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GMM 
from MFCCExtraction import extraer_caracteristicas

def ModelarGMM(NombreGMM,Longitud):
	warnings.filterwarnings("ignore")
	#path to training data
	source   = os.getcwd()+"/MuestrasDeVoz/MuestrasAudio/"   
	#path where training speakers will be saved
	dest = "MuestrasDeVoz/ModeloGMM/"
	train_file = "MuestraDeAudio.txt" 
	file_paths = open(train_file,'r')
	count = 1
	#Funciones de extracción para cada altavoz (5 archivos por altavoces)
	caracteristica = np.asarray(())
	for path in file_paths:    
		path = path.strip()
		#Leer el audio
		sr, audio = read(source + path)
		#extraer 40 características dimensionales MFCC y delta MFCC
		vector   = extraer_caracteristicas(audio, sr)
		if caracteristica.size == 0:
			caracteristica = vector
		else:
			caracteristica = np.vstack((caracteristica, vector))
		#cuando las características de 5 archivos de altavoces se concatenan, entonces haga entrenamiento modelo
		if count == int(Longitud):    
			gmm = GMM(n_components = 16, n_iter = 200, covariance_type='diag', n_init = 3)
			gmm.fit(caracteristica)
			#modelo gaussiano entrenado
			picklefile = 'voz'+NombreGMM+".gmm"
			cPickle.dump(gmm, open(os.getcwd()+"/"+dest + picklefile, 'w'))
			caracteristica = np.asarray(())
			count = 0
		count = count + 1
	return '+ Modelado completado: ' + str(picklefile)
