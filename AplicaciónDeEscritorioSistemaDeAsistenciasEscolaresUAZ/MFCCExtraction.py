# -*- coding: utf-8 -*-
import numpy as np
from sklearn import preprocessing
import python_speech_features as mfcc
import matplotlib.pyplot as plt

"""Calcula y devuelve el delta de la matriz de vectores de características dada"""
def calculo_de_delta(array):
	rows, cols = array.shape
	deltas = np.zeros((rows, 20))
	N = 2
	for i in range(rows):
		index = []
		j = 1
		while j <= N:
			if i-j < 0:
				first =0
			else:
				first = i-j
			if i+j > rows-1:
				second = rows-1
			else:
				second = i+j 
			index.append((second, first))
			j+=1
		deltas[i] = (array[index[0][0]]-array[index[0][1]]+(2*(array[index[1][0]]-array[index[1][1]])))/10
	return deltas

def extraer_caracteristicas(audio,rate):
	"""extrae 20 características de mfcc tenues de un audio, y combina delta para convertirlo en un vector de 40 características tenues"""    
	mfcc_caracteristica = mfcc.mfcc(audio,rate, 0.025, 0.01, 20, nfft = 1200, appendEnergy = True)    
	mfcc_caracteristica = preprocessing.scale(mfcc_caracteristica)
	delta = calculo_de_delta(mfcc_caracteristica)
	combinacion = np.hstack((mfcc_caracteristica, delta))
	return combinacion
