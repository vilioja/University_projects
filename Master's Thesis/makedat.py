import sys
import os
import math
import numpy as np

a = 11500.0
aorig = a
ecc = 0.6
eccorig = ecc
spinmag = 0.28
spinmagorig = spinmag

ajoname = "ajo_mass-ratio2.sh"
fajo = open(ajoname, "w")
fajo.write("#!/bin/bash\n")
fajo.write("\n")

#printing variables
#common things
points = 2
proptime = 1000000
printtime = 1
usePN = 1
useSpin = 1
useCross = 0
BHBHonly = 0
ignoreStarStar = 0
maxPN = 7
G = 1
c = 10000

nums = 100
qlist = np.logspace(-2.2,0,nums)

type1 = 5
m1 = 1.4e10
type2 = 5
m2 = 1.8e8
mtot = m1+m2


for i in range(0,nums):
    mfrac = qlist[i]
    m1 = mtot/(mfrac + 1)
    m2 = mtot - m1
    #particle 1
    pos11 = -1 * (a*(1+ecc)/math.sqrt(2.)) * (m2/mtot)
    pos12 = 0
    pos13 = -1 * (-1 * a*(1+ecc)/math.sqrt(2.)) * (m2/mtot)
    vel11 = 0
    vel12 = -1 * math.sqrt(mtot*(1-ecc)/(1+ecc)*(1./a)) * (m2/mtot)
    vel13 = 0
    spin11 = 0
    spin12 = 0
    spin13 = G * (m1**2)/c * spinmag

    #particle 2
    pos21 = (a*(1+ecc)/math.sqrt(2.)) * (m1/mtot)
    pos22 = 0
    pos23 = (-1 * a*(1+ecc)/math.sqrt(2.)) * (m1/mtot)
    vel21 = 0
    vel22 = math.sqrt(mtot*(1-ecc)/(1+ecc)*(1./a)) * (m1/mtot)
    vel23 = 0
    spin21 = 0
    spin22 = 0
    spin23 = 0

    if mfrac >= 0.1:
        printtime = 0.1

    name = "oj287-mass-ratio%.4f.dat" % mfrac
    fajo.write("./archain_test %s\n" % name)
    f = open(name, "w")
    f.write("%d\n" % points)
    f.write("%d\n" % proptime)
    f.write("%f\n" % printtime)
    f.write("%d\n" % usePN)
    f.write("%d\n" % useSpin)
    f.write("%d\n" % useCross)
    f.write("%d\n" % BHBHonly)
    f.write("%d\n" % ignoreStarStar)
    f.write("%d\n" % maxPN)
    f.write("%f\n" % G)
    f.write("%f\n" % c)

    f.write("%d\n" % type1)
    f.write("%f\n" % m1)
    f.write("%.18f\n" % pos11)
    f.write("%.18f\n" % pos12)
    f.write("%.18f\n" % pos13)
    f.write("%.18f\n" % vel11)
    f.write("%.18f\n" % vel12)
    f.write("%.18f\n" % vel13)
    f.write("%.18f\n" % spin11)
    f.write("%.18f\n" % spin12)
    f.write("%.18f\n" % spin13)

    f.write("%d\n" % type2)
    f.write("%f\n" % m2)
    f.write("%.18f\n" % pos21)
    f.write("%.18f\n" % pos22)
    f.write("%.18f\n" % pos23)
    f.write("%.18f\n" % vel21)
    f.write("%.18f\n" % vel22)
    f.write("%.18f\n" % vel23)
    f.write("%.18f\n" % spin21)
    f.write("%.18f\n" % spin22)
    f.write("%.18f\n" % spin23)

    f.close()



fajo.close()
komento = "chmod u=rwx %s" % ajoname
os.system(komento)
