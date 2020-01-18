#-*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import sys


#luetaan komentoriviltä datatiedoston nimi
inputfile = sys.argv[1]

#katsotaan montako kappaletta on piirrettävänä
f = open(inputfile,'r')
rivi = f.readline().rstrip('\n')
f.close()

rivi = rivi.split(';')				#pätkitään data ;-merkkien kohdilta
kpl = len(rivi)						#katsotaan itse kappalemäärä

#piirretään

varit = ['yellow','orange']

f = open(inputfile,'r')

aika = float(sys.argv[2])/365			#luetaan komentoriviltä mikä oli laskettaessa talletusaikojen väli päivissä
x = 0
for line in f:
	plt.close('all')
	fig, (ax1, ax2) = plt.subplots(1, 2)
	ax1.axis([-6,6,-6,6])
	ax2.axis([-6,6,-1,1])
	ax1.set_aspect(1)
	ax2.set_aspect(6)
	line.rstrip('\n')
	rivi = line.split(';')	
	for i in xrange(kpl):
		paikka = rivi[i].split(',')
		if (i == 0):									#keskitetään kuvaaja aina keskuskappaleeseen
			keskuskappalex = float(paikka[0])
			keskuskappaley = float(paikka[1])
			keskuskappalez = float(paikka[2])
		
		xpaikka = float(paikka[0]) - keskuskappalex
		ypaikka = float(paikka[1]) - keskuskappaley
		zpaikka = float(paikka[2]) - keskuskappalez
		
		ax1.scatter(xpaikka, ypaikka, color=varit[i])
		ax2.scatter(ypaikka, zpaikka, color=varit[i])

	ax1.set_title('xy-taso')
	ax2.set_title('yz-taso')
	fig.text(0.5, 0.2, 'Distance (AU), T = %8.4f yr' % (x*aika), ha='center', va='center')
	fig.text(0.06, 0.5, 'Distance (AU)', ha='center', va='center', rotation='vertical')
	plt.savefig('kuva%03d' % x)
	plt.clf()
	x = x + 1
	
f.close()
