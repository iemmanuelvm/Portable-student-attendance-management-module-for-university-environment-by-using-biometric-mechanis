# -*- coding: utf-8 -*-
import os, time, cPickle, warnings
import numpy as np
from scipy.io.wavfile import read
from featureextraction import extract_features
warnings.filterwarnings("ignore")

def user():
    #path donde se guardarán las plantillas de los oradores
    modeloGMMPath = os.getcwd()+"/VOCES/"
    #list comprehesion con los modelos GMM
    archivos_gmm = [os.path.join(modeloGMMPath,fname) for fname in os.listdir(modeloGMMPath) if fname.endswith('.gmm')]
    #Cargar los modelos GMM
    modelos = [cPickle.load(open(fname,'r')) for fname in archivos_gmm]
    voces_usuarios = [fname.split("/")[-1].split(".gmm")[0] for fname in archivos_gmm]
    path = os.getcwd()+'/MUESTRA_VOZ/AUDIO_TEST.wav'
    sr, audio = read(path)
    vector   = extract_features(audio,sr)
    log_likelihood = np.zeros(len(modelos)) 
    for i in range(len(modelos)):
        gmm = modelos[i]
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
    winner = np.argmax(log_likelihood)

    if(len(str(voces_usuarios[winner]).replace('\n', ' ').replace('\r', '').replace(" ", ""))==4):
        return [1, voces_usuarios[winner].replace('\n', ' ').replace('\r', '').replace(" ", "")] 
    else:
        return [2, voces_usuarios[winner].replace('\n', ' ').replace('\r', '').replace(" ", "")] 