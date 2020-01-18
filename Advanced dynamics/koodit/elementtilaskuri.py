#-*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from numpy import arccos as acos
from numpy import dot, sqrt
from numpy.linalg import norm
import sys

#------------------funktioita

def eccentric_anomaly_from_true(e, f):
	E = np.arctan2(sqrt(1- e**2) * np.sin(f), e + np.cos(f))
	n = np.floor(E/(2*np.pi))
	E = E - n*(2*np.pi)
	return E

def mean_anomaly_from_true(e, f):
	E = eccentric_anomaly_from_true(e, f)
	return E - e*np.sin(E)

def angular_momentum(paikka, nopeus):
	r0 = paikka
	v0 = nopeus
	return np.cross(r0, v0)

def node_vector(angmomentum):
	return np.cross([0, 0, 1], angmomentum)

def eccentricity_vector(paikka, nopeus, massa):
	r0 = paikka
	v0 = nopeus
	ev = (1/massa)*((norm(v0)**2 - massa/norm(r0))*r0 - dot(r0, v0)*v0)
	return ev

def specific_orbital_energy(paikka, nopeus, massa):
	r0 = paikka
	v0 = nopeus
	ener = (norm(v0)**2)/2 - massa/norm(r0)
	return ener


#------------------ohjelma alkaa


inputfile = sys.argv[1]						#luetaan komentoriviltä datatiedoston nimi
aika = float(sys.argv[2])					#luetaan komentoriviltä mikä oli laskettaessa talletusaikojen väli vuosissa

pisteet = 0
filu = open(inputfile,'r')						#luetaan datapisteiden määrä
for line in filu:
	pisteet = pisteet + 1

pisteet = pisteet - 1
filu.close()

filu = open(inputfile,'r')
massat = filu.readline().rstrip('\n')			#luetaan kappaleiden massat ensimmäiseltä riviltä

massat = np.array(massat.split(','))		#pätkitään data ,-merkkien kohdilta
massat = massat.astype(float)
kpl = len(massat)							#katsotaan kappalemäärä

grav = 4*(np.pi**2)/(365.25**2)			#gravitaatiovakio yksiköissä Au, d, M_sol
mu = massat*grav						#mu:ta käytetään elementtilaskuissa
mu[1:6] = mu[1:6]+mu[0]					#oikea mu on siis kappaleen mu plus auringon mu

x = 0
a = np.zeros((pisteet,kpl))		#isoakselin puolikas
ecc = np.zeros((pisteet,kpl))	#eksentrisyys
inc = np.zeros((pisteet,kpl))	#inklinaatio
w = np.zeros((pisteet,kpl))		#perihelin argumentti
o = np.zeros((pisteet,kpl))		#nouseva solmu
m = np.zeros((pisteet,kpl))		#keskianomalia
lam = np.zeros((pisteet,kpl))	#keskilongitudi
fii = np.zeros(pisteet)			#fii32
t = np.zeros(pisteet)			#aika
eps = 1e-15

for line in filu:
	line.rstrip('\n')
	rivi = np.array(line.split(';'))
	r = np.zeros((kpl,3))
	v = np.zeros((kpl,3))
	for i in xrange(kpl):								#luetaan paikkoja ja nopeuksia muistiin
		paikkaJaNopeus = np.array(rivi[i].split(','))
		paikkaJaNopeus = paikkaJaNopeus.astype(float)
		if (i == 0):
			keskuskappaler = paikkaJaNopeus[0:3]

		r[i,:] = np.subtract(paikkaJaNopeus[0:3],keskuskappaler)	#vähennettään kappaleen paikasta auringon paikka jotta systeemi on keskitetty
		v[i,:] = paikkaJaNopeus[3:6]

	for i in xrange(kpl):											#lasketaan rataelementit
		if (norm(r[i,:]) > eps):
			h = angular_momentum(r[i,:], v[i,:])
			n = node_vector(h)

			ev = eccentricity_vector(r[i,:], v[i,:], mu[i])

			E = specific_orbital_energy(r[i,:], v[i,:], mu[i])

			a[x,i] = -mu[i]/(2*E)

			ecc[x,i] = norm(ev)
			inc[x,i] = acos(h[2] / norm(h))

			if (abs(inc[x,i]) < eps):
				o[x,i] = 0
				if (abs(ecc[x,i]-0) < eps):
					w[x,i] = 0
				else:
					w[x,i] = acos(ev[0] / norm(ev))
			else:
				o[x,i] = acos(n[0]/norm(n))
				if (n[1] < 0):
					o[x,i] = 2*np.pi - o[x,i]

				w[x,i] = acos(dot(n, ev)/(norm(n)*norm(ev)))

			if (abs(ecc[x,i]) < eps):
				if (abs(inc[x,i] < eps)):
					f = acos(r[i,0]/norm(r[i,:]))
					if (v[i,0] > 0):
						f = 2*np.pi - f

				else:
					f = acos(dot(n,r[i,:])/(norm(n)*norm(r[i,:])))
					if (dot(n,v[i,:]) > 0):
						f = 2*np.pi - f

			else:
				if (ev[2] < 0):
					w[x,i] = 2*np.pi - w[x,i]

				f = acos(dot(ev, r[i,:]) / (norm(ev) * norm(r[i,:])))
				if (dot(r[i,:],v[i,:]) < 0):
					f = 2*np.pi - f

			m[x,i] = mean_anomaly_from_true(ecc[x,i], f)

			lam[x,i] = o[x,i] + w[x,i] + m[x,i]					#lambda = Omega + omega + M
			while (lam[x,i] > 2*np.pi):
				lam[x,i] = lam[x,i] - 2*np.pi

	fii[x] = 3*lam[x,5] - 2*lam[x,4] - (w[x,5] + o[x,5])		#fii32 = 3*lambda_P - 2*lambda_N - pomega_P
	while (fii[x] > 2*np.pi):
		fii[x] = fii[x] - 2*np.pi

	while (fii[x] < 0):
		fii[x] = fii[x] + 2*np.pi

	t[x] = x*aika
	x = x + 1

filu.close()

#------------------valitaan mitä piirretään

varit = ['yellow','orange','brown','lightskyblue','midnightblue','lightslategray']
fig = plt.figure()
ax = fig.add_subplot(111)

#ax.set_ylim(0,50)
#for i in xrange(kpl):
#	ax.plot(t, a[:,i], c=varit[i])							#piirtää isoakselin puolikkaita

#ax.set_ylim(0,0.3)
#for i in xrange(kpl):
#ax.plot(t, ecc[:,i], c='lightslategray')					#piirtää eksentrisyyksiä

#ax.set_ylim(0,20)
#for i in xrange(kpl):
#ax.plot(t, inc[:,5]*(180/np.pi), c='lightslategray')		#piirtää inklinaatioita

#for i in xrange(kpl):
#ax.plot(t, w[:,5]*(180/np.pi), c='lightslategray')			#piirtää perihelin argumentteja

#for i in xrange(kpl):
#ax.plot(t, o[:,5]*(180/np.pi), c='lightslategray')			#piirtää nousevia solmuja

#for i in xrange(kpl):
	#ax.plot(t, m[:,2]*(180/np.pi), c=varit[i])				#piirtää keskianomalioita

#fii = fii*(180/np.pi)										#piirtää fii32:sta
#print np.mean(fii)
#ax.plot(t,fii)

ax.set_xlabel('Aika, yr')
ax.set_ylabel('Fii32, deg')
plt.show()
