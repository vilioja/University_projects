# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
import sys

#anna data-tiedosto komentoriviargumenttina, eli siis 'python piirtaja.py data'
inputfile = sys.argv[1]

f = open(inputfile,'r')

m = -6

for line in f:
	m = m + 1

f.close()

kolmiot = m / 10
yksikolmio = m / kolmiot


#Normitetaan kirkkain kohde olemaan aina saman värinen
#Luetaan myös auringon ja maan koordinaatit
f = open(inputfile,'r')

m = -6
suurinkirkkaus = 0
kirkkaus = 0

aurx = 0
aury = 0
aurz = 0
maax = 0
maay = 0
maaz = 0

for line in f:
	if (m == -6):
		aurx = float(line.strip())*0.2
	if (m == -5):
		aury = float(line.strip())*0.2
	if (m == -4):
		aurz = float(line.strip())*0.2
	if (m == -3):
		maax = float(line.strip())*0.2
	if (m == -2):
		maay = float(line.strip())*0.2
	if (m == -1):
		maaz = float(line.strip())*0.2
	
	m = m + 1
	if (m == 1):
		kirkkaus = float(line.strip())
		if (kirkkaus > suurinkirkkaus):
			suurinkirkkaus = kirkkaus

	if (m == yksikolmio):
		m = 0

f.close()

if (suurinkirkkaus > 0):
	normi = 0.7 / suurinkirkkaus
else:
	normi = 0

x = []
y = []
z = []

f = open(inputfile,'r')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim3d(-6,6)
ax.set_ylim3d(-6,6)
ax.set_zlim3d(-6,6)

m = -6
pnum = -6

for line in f:
	m = m + 1
	if (m == 1):
		kirkkaus = float(line.strip())
		continue
	
	pnum = pnum + 1

	if (pnum == 1):
		x.append(float(line.strip()))
	if (pnum == 2):
		y.append(float(line.strip()))
	if (pnum == 3):
		z.append(float(line.strip()))
		pnum = 0

	if (m == yksikolmio):
		m = 0

		pun = 0.2 + (normi * kirkkaus)
		vih = 0.2 + (normi * kirkkaus)
		sin = 0.2 + (normi * kirkkaus)

		#scatter plot pisteistä
		#ax.scatter(x, y, z)

		#kolmiointi pisteistä
		ax.plot_trisurf(x, y, z, color=[pun,vih,sin], linewidth=0.2)

		x[:] = []
		y[:] = []
		z[:] = []


ax.scatter(aurx, aury, aurz, color='y', s=5000)
ax.scatter(maax, maay, maaz, color='b', s=1000)

f.close()

plt.show()
