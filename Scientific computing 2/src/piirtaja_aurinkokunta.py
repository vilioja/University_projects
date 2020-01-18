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

varit = ['yellow','lightslategray','chartreuse','b','r','orange','brown','lightskyblue','midnightblue']

f = open(inputfile,'r')

aika = float(sys.argv[2])/365			#luetaan komentoriviltä mikä oli laskettaessa talletusaikojen väli päivissä
x = 0
for line in f:
	plt.close('all')
	fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
	ax1.axis([-2,2,-2,2])
	ax2.axis([-2,2,-1,1])
	ax3.axis([-31,31,-31,31])
	ax4.axis([-31,31,-1,1])
	ax1.set_aspect(1)
	ax2.set_aspect(2)
	ax3.set_aspect(1)
	ax4.set_aspect(31)
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
		ax3.scatter(xpaikka, ypaikka, color=varit[i])
		ax4.scatter(ypaikka, zpaikka, color=varit[i])

	ax1.set_title('xy-taso')
	ax2.set_title('yz-taso')
	ax3.set_title('xy-taso')
	ax4.set_title('yz-taso')
	fig.text(0.5, 0.03, 'Distance (AU), T = %8.4f yr' % (x*aika), ha='center', va='center')
	fig.text(0.06, 0.5, 'Distance (AU)', ha='center', va='center', rotation='vertical')
	plt.savefig('kuva%04d' % x)
	plt.clf()
	x = x + 1
	
f.close()
