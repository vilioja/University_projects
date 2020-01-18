import numpy as np
import math
import matplotlib.pyplot as plt
import sys
from scipy.optimize import curve_fit
from scipy.stats import chi2
import random

#---------functions------------

def funct(x,a,b,c):
	return a+b*np.cos(x)+c*np.sin(x)

#---------

def reffunct(t,a,b,c,f):
	return a+b*np.cos(2*np.pi*f*t)+c*np.sin(2*np.pi*f*t)

#---------

def khitoiseen(x,y,beta,sig):
	return np.sum(((y-funct(x,*beta))/sig)**2)

#---------

def pilotsearch(t,y,sig,pmin,pmax,ofac,k):
	dmin=0.9*pmin
	dmax=4*pmax
	fmin=1.0/pmax								#calculate fmin, fmax, and the step
	fmax=1.0/pmin
	fstep=1.0/(ofac*dmax)
	tau = 1.0/(4*k)
	w=sig**(-2)

	n = len(t)
	tij = np.zeros((n,n))
	yij = np.zeros((n,n))
	Wij = np.zeros((n,n))
	weights = np.zeros((n,n))
	Wij = Wij.astype(int)

	for x1 in range(n-1):								#compute the pairs tij, yij, Wij, and weights
		for x2 in range(x1+1,n):						#here x1 and x2 are names used for the indices 'i' and 'j'
			tij[x1][x2] = abs(t[x1] - t[x2])			#we'll use this notation since later on we'll use j as a different index
			yij[x1][x2] = (y[x1] - y[x2])**2
			weights[x1][x2] = (w[x1]*w[x2])/(w[x1]+w[x2])
			if (tij[x1][x2] > dmin and tij[x1][x2] < dmax):
				Wij[x1][x2] = 1

	j = int(math.floor((fmax-fmin)/fstep))				#we want to test all multiples f_j > fmin + j*fstep. This way we can calculate j beforehand
	f = np.zeros(j)
	theta = np.zeros(j)

	for i in range(j):									#begin the loop to calculate theta
		f[i] = fmin + i*fstep							#calculate the frequencies we want to test
		fii = np.zeros((n,n))
		Zij = np.zeros((n,n))
		Zij = Zij.astype(int)
		summa1 = 0.
		summa2 = 0
		for x1 in range(n-1):							#first calculate phi for this frequency, and corresponding Z
			for x2 in range(x1+1,n):
				fii[x1][x2] = (f[i]*tij[x1][x2])%1
				if (fii[x1][x2] < tau or fii[x1][x2] > 1.-tau):
					Zij[x1][x2] = 1

				summa1 = summa1 + Zij[x1][x2]*Wij[x1][x2]*weights[x1][x2]*yij[x1][x2]	#calculate the sums that form theta
				summa2 = summa2 + Zij[x1][x2]*Wij[x1][x2]*weights[x1][x2]

		theta[i] = summa1/summa2


	bestFs = np.empty(0)
	prevtheta = 0.
	prevf = 0.
	erotus = (1./dmax)/2									#we want the minimum separation between frequencies to be (1/Dmax)/2 in both directions
	for i in range(1,j-1):												#find all local minima
		if (theta[i] < theta[i-1] and theta[i] < theta[i+1]):			#these checks make sure that we don't get multiple best values
			if (len(bestFs) == 0):										#that are actually just extremely close to each other in frequency
				prevtheta = theta[i]
				prevf = f[i]
				bestFs = np.append(bestFs, theta[i])					#the first value will always be stored
			else:
				if (f[i]-prevf > erotus):								#if the two values are far enough apart, nothing special happens
					bestFs = np.append(bestFs, theta[i])
					prevtheta = theta[i]
					prevf = f[i]
				else:													#if they're very close, save only the smaller theta
					if (theta[i] < prevtheta):
						bestFs = np.delete(bestFs,len(bestFs)-1)		#delete the previous one and save the new one
						bestFs = np.append(bestFs, theta[i])
						prevtheta = theta[i]
						prevf = f[i]

	bestFs.sort()									#sort the minima, from smallest to largest
	bestFs = bestFs[:4]								#take only the four best periods, i.e. the first four
	indeksit = np.zeros(4).astype(int)				#get the indices of the best values
	i = 0
	while (i < 4):												#since there might be multiple best values with nearly identical theta,
		n1 = len(np.where(theta==bestFs[i])[0])					#this loop chekcs that if there are, then they all get included
		itemp = i
		for i1 in range(n1):
			indeksit[i] = np.where(theta==bestFs[itemp])[0][i1]
			i = i+1

	indeksit.sort()									#sort the indices
	f4 = np.zeros(4)
	theta4 = np.zeros(4)
	for i in range(4):								#get the four best values of theta and f, in order from left to right
		freq = indeksit[i]
		f4[i] = f[freq]
		theta4[i] = theta[freq]

	return f,theta,f4,theta4,dmax

#---------

def gridsearch(t,y,sig,k,f4,dmax,ofac):
	n = len(t)
	t = t - t[0]
	fpilot = 1.0/dmax
	fgrid = 1.0/(ofac*(t[-1]-t[0]))
	tau = 1.0/(4*k)

	fmin = np.zeros(4).astype(int)
	for i in range(4):
		a = (f4[i]-(5*fpilot))/fgrid
		fmin[i] = int(math.ceil(a))

	b = (f4[0]+(5*fpilot))/fgrid		#while the f' differs and thus the starting f too, the amount of tested frequencies stays the same
	fmax = int(math.ceil(b))			#all tested frequencies are x*fgrid, where x is an integer and fmin <= x < fmax
	famount = fmax - fmin[0]			#we get the number of frequencies from this
	freqs = np.zeros((4,famount))		#store all values of tested frequencies f
	thetagrid = np.zeros((4,famount))	#store all actual theta_grid values

	p4 = np.zeros((4,famount))
	phases = np.zeros((4,famount,n))
	xi = np.zeros((4,famount,n))
	freepms = 2*k+1										#number of free parameters
	beta0 = np.ones((famount,freepms))					#initial guesses for the free parameters
	beta = np.zeros((4,famount,freepms))
	pcov = np.zeros((4,famount,freepms,freepms))
	ebeta = np.zeros((4,famount,freepms))
	df = n-freepms								#degrees of freedom
	khi2 = np.zeros((4,famount))				#the chi^2 values
	fbest = np.zeros(4)
	thetagridbest = np.zeros(4)
	indeksit = np.zeros(4).astype(int)
	betabest = np.zeros((4,freepms))

	for i in range(4):					#calculate all the wanted frequencies
		for j in range(famount):
			freqs[i,j] = (fmin[i]+j)*fgrid

			p4[i,j] = 1./freqs[i,j]						#calculations for determining the best p value
			phases[i,j,:] = ((t-t[0])*freqs[i,j])%1		#calculate the phases

			xi[i,j,:] = 2*np.pi*phases[i,j,:]

			beta[i,j,:],pcov[i,j,:,:]=curve_fit(funct,xi[i,j,:],y,p0=beta0[j,:],sigma=sig)	#calculate the best free paramters with curve_fit
			ebeta[i,j,:] = np.sqrt(np.diag(pcov[i,j,:,:]))									#errors for the free parameters

			khi2[i,j] = khitoiseen(xi[i,j,:],y,beta[i,j,:],sig)

			thetagrid[i,j] = 2*(1./np.sum(w))*khi2[i,j]

		thetagridbest[i] = np.amin(thetagrid[i,:])
		indeksit[i] = np.where(thetagrid[i,:]==thetagridbest[i])[0][0]
		fbest[i] = freqs[i,indeksit[i]]
		betabest[i,:] = beta[i,indeksit[i],:]

	betacur = np.zeros((4,1+freepms))
	for i in range(4):
		betacur[i,:] = np.append(betabest[i,:],fbest[i])

	return freqs,thetagrid,fbest,thetagridbest,betacur

#---------

def refinedsearch(t,y,sig,k,betacur):
	n=len(t)
	t = t - t[0]
	freepms = 2*k+2
	df = n-freepms

	beta = np.zeros((4,freepms))

	for i in range(4):
		beta[i,:],pcov=curve_fit(reffunct,t,y,p0=betacur[i,:],sigma=sig)
	
	return beta

#---------

def bootstrap(t,y,sig,k,beta):
	n=len(t)
	t = t - t[0]
	freepms = 2*k+2
	df = n-freepms

	resid = np.zeros((4,n))
	gi = np.zeros((4,n))

	for i in range(4):
		gi[i,:] = reffunct(t,*beta[i,:])
		resid[i,:] = y - gi[i,:]

	smaara = 200										#how many times the bootstrap is run
	betamin = np.zeros((4,smaara,freepms))				#beta'
	gmin = np.zeros((4,smaara,n))
	amps = np.zeros((4,smaara))
	means = np.zeros((4,smaara))
	pvalues = np.zeros((4,smaara))
	freqs = np.zeros((4,smaara))

	for i in range(4):									#start the bootstrap iteration itself
		for s in range(smaara):
			residsample = np.zeros(n)					#epsilon*
			sigsample = np.zeros(n)						#error*
			ysample = np.zeros(n)						#y*
			random.seed()
			for j in range(n):
				indeksi = random.randint(0,n-1)
				residsample[j] = resid[i,indeksi]
				sigsample[j] = sig[indeksi]
			
			ysample = gi[i,:] + residsample
			
			betamin[i,s,:],pcov=curve_fit(reffunct,t,ysample,p0=beta[i,:],sigma=sigsample)
			gmin[i,s,:] = reffunct(t,*betamin[i,s,:])
			means[i,s] = np.mean(gmin[i,s,:])
			amps[i,s] = np.amax(gmin[i,s,:]) - np.amin(gmin[i,s,:])
			pvalues[i,s] = 1./betamin[i,s,freepms-1]

	meanmean = np.zeros(4)				#means
	meanstd = np.zeros(4)				#errors of means
	ampmean = np.zeros(4)				#amplitudes
	ampstd = np.zeros(4)				#errors of amplitudes
	pvaluemean = np.zeros(4)			#p values
	pvaluestd = np.zeros(4)				#errors of p values
	betameans = np.zeros((4,freepms))	#averages of the free parameters
	for i in range(4):
		meanmean[i] = np.mean(means[i,:])
		meanstd[i] = np.std(means[i,:])
		ampmean[i] = np.mean(amps[i,:])
		ampstd[i] = np.std(amps[i,:])
		pvaluemean[i] = np.mean(pvalues[i,:])
		pvaluestd[i] = np.std(pvalues[i,:])
		betameans[i,:] = np.mean(betamin[i,:,:],axis=0)

	return meanmean, meanstd, ampmean, ampstd, pvaluemean, pvaluestd, betameans

#---------main---------------------

f=open('STUDENT9_AIJA.DAT','r')				#open the data file to read
t=f.read()									#read the data
f.close()
ttemp=map(float, t.split())					#split the strings
t=ttemp[0::3]								#read every second number starting from the first, they're the times
t=np.array(t)								#convert the array into a numpy array
n = len(t)
y=ttemp[1::3]								#read every second number starting from the second, they're the data values
y=np.array(y)
sig=ttemp[2::3]								#read the errors
sig=np.array(sig)
my=(sum(y))/len(y)							#calculate my, average of y
y=y-my										#substract average from data
w=sig**(-2)									#calculate the weights from the errors

pmin=0.5									#define the min and max for p, the over filling factor, and k/tau
pmax=10
ofac=10
k=1											#tau=0.25


f,theta,f4,theta4,dmax = pilotsearch(t,y,sig,pmin,pmax,ofac,k)				#run the pilotsearch function

fg,thetag,fgbest,thetagbest,betacur = gridsearch(t,y,sig,k,f4,dmax,ofac)	#run gridsearch

betafinal = refinedsearch(t,y,sig,k,betacur)								#run refinedsearch

meanmean,meanerror,ampmean,amperror,pvaluemean,pvalueerror,betameans = bootstrap(t,y,sig,k,betafinal)	#run bootstrap

ti = t-t[0]
p4p = np.zeros(4)
p4g = np.zeros(4)
phasesp = np.zeros((4,n))
phasesboot = np.zeros((4,n))
for i in range(4):
	p4p[i] = 1./f4[i]						#calculations for determining the best p value
	p4g[i] = 1./fgbest[i]						
	phasesp[i,:] = (ti*f4[i])%1					#phases from pilotsearch
	phasesboot[i,:] = (ti*betameans[i,3])%1		#phases from bootstrap


#------------plotting---------------------

fig = plt.figure(figsize=(14,12))

vaakakoko = 4
pystykoko = 5
koko=(pystykoko,vaakakoko)
ax1 = plt.subplot2grid(koko, (0, 0), rowspan=1, colspan=4)
ax2 = plt.subplot2grid(koko, (1, 0), rowspan=1, colspan=4)
ax3 = plt.subplot2grid(koko, (2, 0), rowspan=1, colspan=1)
ax4 = plt.subplot2grid(koko, (2, 1), rowspan=1, colspan=1)
ax5 = plt.subplot2grid(koko, (2, 2), rowspan=1, colspan=1)
ax6 = plt.subplot2grid(koko, (2, 3), rowspan=1, colspan=1)
ax7 = plt.subplot2grid(koko, (3, 0), rowspan=1, colspan=1)
ax8 = plt.subplot2grid(koko, (3, 1), rowspan=1, colspan=1)
ax9 = plt.subplot2grid(koko, (3, 2), rowspan=1, colspan=1)
ax10 = plt.subplot2grid(koko, (3, 3), rowspan=1, colspan=1)
ax11 = plt.subplot2grid(koko, (4, 0), rowspan=1, colspan=1)
ax12 = plt.subplot2grid(koko, (4, 1), rowspan=1, colspan=1)
ax13 = plt.subplot2grid(koko, (4, 2), rowspan=1, colspan=1)
ax14 = plt.subplot2grid(koko, (4, 3), rowspan=1, colspan=1)

fig.add_subplot(ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9,ax10,ax11,ax12,ax13,ax14)
fig.set_tight_layout('true')

plt.subplots_adjust(wspace=0.5,hspace=0.5)

#----------plot the data----------
ax1.plot(t,y,'r+')
ax1.axis([min(t)-2,max(t)+3,min(y)-0.05,max(y)+0.05])
ax1.tick_params(axis='both',size=8)
txt='Data'
ax1.set_title(txt,fontsize=10)

#----------plot the pilot search and the best P values----------
ero = (max(theta) - min(theta))/6.
ax2.plot(f,theta,'r')
for i in range(4):
	ax2.plot(f4[i],theta4[i],'bd',markerfacecolor='none',markersize=6)
	ax2.text(f4[i]+0.025,theta4[i]-(ero/3),'P = %5.3f' %(p4p[i]))

ax2.axis([min(f)-0.05,max(f)+0.05,min(theta)-ero,max(theta)+ero])
ax2.tick_params(axis='both',size=8)
txt='%s %4s %3.0f' %('Pilot search, ','n = ',n)
ax2.set_title(txt,fontsize=10)

#----------plot the psch phases, gridsearch results and the final bootstrap values----------
xpoints = np.linspace(0,1,1000)
for i in range(4):
	fig.axes[i+2].plot(phasesp[i,:],y,'b+')
	fig.axes[i+2].axis([0,1,min(y),max(y)])
	fig.axes[i+2].tick_params(axis='both',size=8)
	txt='Phase plot, P = %5.3f' %(p4p[i])
	fig.axes[i+2].set_title(txt,fontsize=10)

	fig.axes[i+6].plot(fg[i,:],thetag[i,:],'r-')
	fig.axes[i+6].plot((fgbest[i],fgbest[i]),(max(thetag[i,:]),min(thetag[i,:])),'b-',linewidth=1)
	fig.axes[i+6].axis([min(fg[i,:]),max(fg[i,:]),min(thetag[i,:]),max(thetag[i,:])])
	fig.axes[i+6].tick_params(axis='both',size=8)
	txt='Gridsearch, P = %5.3f' %(p4g[i])
	fig.axes[i+6].set_title(txt,fontsize=10)

	fig.axes[i+10].plot(phasesboot[i,:],y,'b+')
	fig.axes[i+10].plot(xpoints,funct(xpoints*2*np.pi,*betameans[i,:3]),'r-')
	fig.axes[i+10].axis([0,1,min(y),max(y)])
	fig.axes[i+10].tick_params(axis='both',size=8)
	txt='Bootstrap, P = %6.4f' %(pvaluemean[i])
	fig.axes[i+10].set_title(txt,fontsize=10)
	txt='M=%6.4f %s %6.4f \n A=%6.4f %s %6.4f \n P=%7.5f %s %7.5f' %(meanmean[i],'$\pm$', meanerror[i], ampmean[i], '$\pm$', amperror[i], pvaluemean[i], '$\pm$', pvalueerror[i])
	fig.axes[i+10].set_xlabel(txt,fontsize=10)

#plt.show()
plt.savefig('ex12_STUDENT9_AIJA.pdf')
