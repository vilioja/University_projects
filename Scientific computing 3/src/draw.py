#-*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import sys


#read the data file from command line
inputfile = sys.argv[1]

#look how many objects we need to draw
f = open(inputfile,'r')
ln = f.readline().rstrip('\n')
f.close()

ln = ln.split(',')				#chop up the data based on commas
pcs = len(ln)-2					#look at the amount og objects
#timestep = float(ln[pcs])		#read the time step
#record = float(ln[pcs+1])		#read how often the points were saved

#draw the data

colours = ['yellow','brown','lightslategray']

points = -1
f = open(inputfile,'r')
for line in f:
	points = points + 1

f.close()

xplaces = np.zeros((pcs,points))
yplaces = np.zeros((pcs,points))

f = open(inputfile,'r')
masses = f.readline().rstrip('\n')
inertplaces = np.zeros(2)
rotplaces = np.zeros(2)
rotmat = np.zeros((2,2))

x=0
for line in f:
	line.rstrip('\n')
	ln = line.split(';')
	for i in xrange(pcs):
		placeAndVelocity = ln[i].split(',')			#read the inertial coordinates
		
		xplaces[i,x] = float(placeAndVelocity[0])
		yplaces[i,x] = float(placeAndVelocity[1])

	rot = np.arctan2(yplaces[1,x],xplaces[1,x])		#calculate the needed rotation so that Jupiter is on the x-axis

	for i in xrange(pcs):
		rotmat[0,0] = np.cos(rot)					#transform the inertial coordinates to rotating frame by using a rotational matrix
		rotmat[0,1] = -np.sin(rot)
		rotmat[1,0] = np.sin(rot)
		rotmat[1,1] = np.cos(rot)

		inertplaces[0] = xplaces[i,x]
		inertplaces[1] = yplaces[i,x]

		rotplaces = np.matmul(inertplaces,rotmat)

		xplaces[i,x] = rotplaces[0]
		yplaces[i,x] = rotplaces[1]


	x = x + 1

f.close()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-1.1,1.1)
ax.set_ylim(-1.1,1.1)
ax.set_aspect(1)
for i in xrange(pcs):
	ax.scatter(xplaces[i,:], yplaces[i,:], s=2, c=colours[i])

ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()

