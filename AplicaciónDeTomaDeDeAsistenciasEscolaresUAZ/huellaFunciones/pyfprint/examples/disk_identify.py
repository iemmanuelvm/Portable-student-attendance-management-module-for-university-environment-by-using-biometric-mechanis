#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyfprint
import os.path
DIR = "/root/Documents/SistemaEscolarFinal/auxHuella/"

pyfprint.fp_init()
devs = pyfprint.discover_devices()
dev = devs[0]
dev.open()

names = []
fps = []

for name in os.listdir(DIR):
	fps.append(pyfprint.Fprint(open(DIR + "/" + name, 'rb').read()))
	names.append(name)
print(names)
print ("ready to match fingers!")

while True:
	
	i, fp, img, r = dev.identify_finger(fps)

	if i is None:
		print ("no match found")

	else:
		print ("identified " + names[i] + "!")

dev.close()
pyfprint.fp_exit()
