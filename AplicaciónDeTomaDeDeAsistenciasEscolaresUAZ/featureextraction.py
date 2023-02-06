# -*- coding: utf-8 -*-
import numpy as np
from sklearn import preprocessing
import python_speech_features as mfcc

def calculate_delta(array):
    """Calcula y devuelve el delta de la matriz de vectores de características dada"""
    rows, cols = array.shape
    deltas = np.zeros((rows,20))
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
            index.append((second,first))
            j+=1
        deltas[i] = (array[index[0][0]]-array[index[0][1]]+(2*(array[index[1][0]]-array[index[1][1]])))/10
    return deltas

def extract_features(audio,rate):
    """extrae 20 características de mfcc tenues de un audio, realiza CMS y combina delta para convertirlo en un vector de 40 características tenues"""    
    mfcc_feature = mfcc.mfcc(audio,rate, 0.025, 0.01, 20, nfft = 1200, appendEnergy = True)    
    mfcc_feature = preprocessing.scale(mfcc_feature)
    delta = calculate_delta(mfcc_feature)
    combined = np.hstack((mfcc_feature,delta))
    """T = range(combined.shape[0])

    for i in range(combined.shape[1]):
    	plt.plot(T, combined[:,i])

    plt.show()"""
 
    return combined
