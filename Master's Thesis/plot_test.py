#!/usr/bin/python
import sys
import numpy as np
import math
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# plot chain test output


# columns,
# from archain_c.c

#        // time and energy conservation
#        maintask_fprintf(output, "%16.10g ", ch->physical_time);
#        maintask_fprintf(output, "%16.10g ", T);
#        maintask_fprintf(output, "%16.10g ", U);
#        maintask_fprintf(output, "%16.10g ", ch->gr_energy);
#        maintask_fprintf(output, "%16.10g ", ch->binding_energy);
#        maintask_fprintf(output, "%16.10g ", H + ch->binding_energy);
#        // ttl w
#        maintask_fprintf(output, "%16.10g ", ch->ttl_w);
#
#        for (i = 0; i < ch->Nmemb; i++) {
#            double rv[3], vv[3], m1, m2, mu, oe[6];
#            int k;
#
#            // print mass and chain index
#            maintask_fprintf(output, "%16.10g ", copies[i].Mass);
#            maintask_fprintf(output, "%d ", copies[i].chain_index);
#            // print positions and velocities
#            maintask_fprintf(output, "%16.10g %16.10g %16.10g ",
#                    copies[i].Pos[0],
#                    copies[i].Pos[1],
#                    copies[i].Pos[2]);
#            maintask_fprintf(output, "%16.10g %16.10g %16.10g ",
#                    copies[i].Vel[0],
#                    copies[i].Vel[1],
#                    copies[i].Vel[2]);
#
#            // print orbital elements
#            if (bh_index < 0 || i == bh_index) {
#                oe[0] = oe[1] = oe[2] = oe[3] = oe[4] = oe[5] = 0;
#            }
#            else {
#                for (k = 0; k < 3; k++) {
#                    rv[k] = copies[i].Pos[k] - copies[bh_index].Pos[k];
#                    vv[k] = copies[i].Vel[k] - copies[bh_index].Vel[k];
#                }
#                m1 = copies[bh_index].Mass;
#                m2 = copies[i].Mass;
#                /*mu = m1*m2/(m1+m2) * ch->G;*/
#                mu = (m1+m2) * ch->G;
#                chain_orbital_elements(mu, rv, vv, oe);
#            }
#
#            maintask_fprintf(output, "%16.10g %16.10g %16.10g %16.10g %16.10g %16.10g ",
#                    oe[0], oe[1], oe[2], oe[3], oe[4], oe[5]);
#
#        }
#        maintask_fprintf(output, "\n");


if len(sys.argv) != 2:
    print "args: chain_output_file"
    exit(0)

pointoffset = 7
pointcomps  = 14
roffset = 2
oeoffset = 8

f = sys.argv[1]
#data = np.loadtxt(f)
#data = np.genfromtxt(f)
data = np.genfromtxt(f,skip_footer=1)
#data = np.genfromtxt(f, usecols = np.arange(693))

rows = data.shape[0]
cols = data.shape[1]
print "rows", rows
print "cols", cols
npts = (cols - pointoffset)/pointcomps

print "read datafile", f, "containing", npts, "points at", rows, "times"

# store masses
masses = data[0, pointoffset::pointcomps]
print "masses", masses

# conversion factors to SI units
timeyr = 0.156191016424
lenau = 0.9870927200526253

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# plot energy error and energy division
if 0:
    fig = plt.figure()
    fig.add_subplot(121)
    plt.title(r'Energy error (abs / rel)')
    plt.plot(data[:,0], np.abs(data[:,5]), label=r'Abs')
    plt.plot(data[:,0], np.abs(data[:,5]/data[0,4]), label=r'Rel')
    plt.yscale('log')
    plt.legend()

    fig.add_subplot(122)
    plt.title(r'Energy partition')
    plt.plot(data[:,0], np.abs(data[:,1]), label=r'T')
    plt.plot(data[:,0], np.abs(data[:,2]), label=r'U')
    plt.plot(data[:,0], np.abs(data[:,3]), label=r'gr')
    plt.plot(data[:,0], np.abs(data[:,4]), label=r'B')
    plt.legend(loc='lower right')
    plt.yscale('log')

    plt.show()
    fig.clf()

# plot particles' radii and speeds
if 0:
    fig = plt.figure()
    speeds = np.zeros((rows, npts))
    radii = np.zeros((rows, npts))
    for k in range(npts):
        vs = data[:, (pointoffset + k*pointcomps + roffset+3):(pointoffset + k*pointcomps + roffset+6)]
        rs = data[:, (pointoffset + k*pointcomps + roffset):(pointoffset + k*pointcomps + roffset+3)]
        speeds[:, k] = np.linalg.norm(vs, axis=1)
        radii[:, k] = np.linalg.norm(rs, axis=1)
        #print "vs of part", k
        #print vs
        #print "speeds of part", k
        #print speeds

    plt.subplot(121)
    for k in range(npts):
        plt.plot(data[:,0]*timeyr, speeds[:,k]*(lenau/timeyr))
    plt.xlabel(r'Time, yr')
    plt.ylabel(r'Velocity, AU/yr')

    plt.subplot(122)
    for k in range(npts):
        plt.plot(data[:,0]*timeyr, radii[:,k]*lenau)
    plt.xlabel(r'Time, yr')
    plt.ylabel(r'Radii, AU')

    plt.tight_layout()
    plt.show()
    fig.clf()

# plot semimajor axis and eccentricity for binary black holes
if 1:
    #fig = plt.figure(figsize=(10,5),dpi=150)
    fig = plt.figure()
    time = data[:,0]*timeyr
    semi = data[:, pointoffset + (1)*pointcomps + oeoffset]*lenau
    ecc = data[:, pointoffset + (1)*pointcomps + oeoffset+1]

    timeavg = np.zeros(rows)
    semiavg = np.zeros(rows)
    eccavg = np.zeros(rows)

    i = 0

    interval = 1200
    for k in range(0,rows,interval):
        timeavg[i] = np.mean(time[k:k+interval])
        semiavg[i] = np.mean(semi[k:k+interval])
        eccavg[i] = np.mean(ecc[k:k+interval])
        i = i + 1

    semiavg = semiavg[:i]
    eccavg = eccavg[:i]
    timeavg = timeavg[:i]

    plt.subplot(121)
    #semimajor axes
    if 1:
        plt.plot(time, semi)
        plt.xlabel(r'\textbf{Time, yr}')
        plt.ylabel(r'\textbf{Semimajor Axis, AU}')
    if 1:
        plt.plot(timeavg,semiavg)
#        plt.xlabel(r'Time, yr')
#        plt.ylabel(r'Semimajor Axis, AU')

    plt.subplot(122)
    #eccentricities
    if 1:
        plt.plot(time, ecc)
        plt.xlabel(r'\textbf{Time, yr}')
        plt.ylabel(r'\textbf{Eccentricity}')
    if 1:
        plt.plot(timeavg,eccavg)
#        plt.xlabel(r'Time, yr')
#        plt.ylabel(r'Eccentricity')

    plt.tight_layout()
#    plt.savefig("%s.png" %f)
    plt.show()
    fig.clf()

# plot inclination, longitude of the ascending node, the argument of periapsis, and mean anomaly for binary black holes
if 1:
    #fig = plt.figure(figsize=(10,10),dpi=150)
    fig = plt.figure()
    time = data[:,0]*timeyr
    inc = data[:, pointoffset + (1)*pointcomps + oeoffset+2]
    asc = data[:, pointoffset + (1)*pointcomps + oeoffset+3]
    asc = asc + math.pi
    aps = data[:, pointoffset + (1)*pointcomps + oeoffset+4]
    aps = aps + math.pi
    ano = data[:, pointoffset + (1)*pointcomps + oeoffset+5]
    ano = ano + math.pi

    inc = inc * 360/(2*math.pi)
    asc = asc * 360/(2*math.pi)
    aps = aps * 360/(2*math.pi)
    ano = ano * 360/(2*math.pi)

    # timeavg = np.zeros(rows)
    # semiavg = np.zeros(rows)
    # eccavg = np.zeros(rows)
    #
    # i = 0
    #
    # interval = 1200
    # for k in range(0,rows,interval):
    #     timeavg[i] = np.mean(time[k:k+interval])
    #     semiavg[i] = np.mean(semi[k:k+interval])
    #     eccavg[i] = np.mean(ecc[k:k+interval])
    #     i = i + 1
    #
    # semiavg = semiavg[:i]
    # eccavg = eccavg[:i]
    # timeavg = timeavg[:i]

    plt.subplot(221)
    #inclination
    if 1:
        plt.plot(time, inc)
        plt.xlabel(r'\textbf{Time, yr}')
        plt.ylabel(r'\textbf{Inclination}')

    plt.subplot(222)
    #ascending node
    if 1:
        plt.plot(time, asc)
        plt.xlabel(r'\textbf{Time, yr}')
        plt.ylabel(r'\textbf{Longitude of the ascending node}')

    plt.subplot(223)
    #argument of periapsis
    if 1:
        plt.plot(time, aps)
        plt.xlabel(r'\textbf{Time, yr}')
        plt.ylabel(r'\textbf{Argument of periapsis}')

    plt.subplot(224)
    #mean anomaly
    if 1:
        plt.plot(time, ano)
        plt.xlabel(r'\textbf{Time, yr}')
        plt.ylabel(r'\textbf{Mean anomaly at epoch}')

    plt.tight_layout()
#    plt.savefig("%s.png" %f)
    plt.show()
    fig.clf()

# plot orbits
if 1:
    raw_input("Press enter to start")
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    title = ax.set_title('Point orbits, t = {0:8.2f} yr'.format(data[0,0]*0.1561859405615804))
    ax.set_xlabel("x (AU)")
    ax.set_ylabel("y (AU)")
    ax.set_zlabel("z (AU)")
#    ax.set_xlim3d(-19000,19000)
#    ax.set_ylim3d(-19000,19000)
#    ax.set_zlim3d(-19000,19000)
    ax.set_xlim3d(-1400,1400)
    ax.set_ylim3d(-1400,1400)
    ax.set_zlim3d(-1400,1400)
    rs0 = data[:, (pointoffset + 0*pointcomps + roffset):(pointoffset + 0*pointcomps + roffset + 3)] * lenau
    rs1 = data[:, (pointoffset + 1*pointcomps + roffset):(pointoffset + 1*pointcomps + roffset + 3)] * lenau
    line1, = ax.plot([rs0[0,0]], [rs0[0,1]], [rs0[0,2]], 'o')
    line2, = ax.plot([rs1[0,0]], [rs1[0,1]], [rs1[0,2]], 'o')
    color = line2.get_color()
    line3, = ax.plot([rs1[0,0]], [rs1[0,1]], [rs1[0,2]], color=color)
    az = 0.
    el = 16.
    ax.view_init(elev=el, azim=az)
    #line4 = ax.quiver(rs1[0,0], rs1[0,1], rs1[0,2], rs1[0,0], rs1[0,1], rs1[0,2]+5000, color='black')

    #for k in range(1,rows,200):
    for k in range(1,rows):
        az = az + 1
        m = k - 500
        if (m < 0):
            m = 0
        title.set_text("Point orbits, t = {0:8.2f} yr".format(data[k,0]*0.1561859405615804))
        #ax.view_init(elev=el, azim=az)
        line1.set_data(rs0[k,0], rs0[k,1])
        line1.set_3d_properties(rs0[k,2])
        line2.set_data(rs1[k,0], rs1[k,1])
        line2.set_3d_properties(rs1[k,2])
        line3.set_data(rs1[m:k,0], rs1[m:k,1])
        line3.set_3d_properties(rs1[m:k,2])
        #line4.set_segments([[rs1[k,0], rs1[k,1], rs1[k,2]], [rs1[k,0], rs1[k,1], rs1[k,2]+5000]])
        fig.canvas.draw()
        #plt.draw()
        #plt.savefig('results/anim/%05d.png' %(k))
        fig.canvas.flush_events()

        #rs = data[:, (pointoffset + k*pointcomps + roffset):(pointoffset + (k+1)*pointcomps + roffset)]*lenau
        #line, = ax.plot(rs[:100,0], rs[:100,1], rs[:100,2])
        #line, = ax.plot(rs[-1000:,0], rs[-1000:,1], rs[-1000:,2])
        #color = line.get_color()
        #xmax = max(xmax, np.amax(np.abs(rs[:,0])))
        #ymax = max(ymax, np.amax(np.abs(rs[:,1])))
        #zmax = max(zmax, np.amax(np.abs(rs[:,2])))
        #ax.plot([rs[-1,0]], [rs[-1,1]], [rs[-1,2]], 'o', color=color)
        #ax.plot([rs[100,0]], [rs[100,1]], [rs[100,2]], 'o', color=color)
        #ax.quiver(rs1[100,0], rs1[100,1], rs1[100,2], rs1[100,0], rs1[100,1], rs1[100,2]+5000, color='black')

    #ani = animation.FuncAnimation(fig, anim, frames=rows, interval=50, blit=False)
    #plt.show()
    #fig.clf()

if 0:
    def plot_components(c1, c2):
        for k in range(npts):
            rs = data[:, (pointoffset + k*pointcomps + roffset):(pointoffset + k*pointcomps + roffset + 3)] * lenau
            vs = data[:, (pointoffset + k*pointcomps + roffset+3):(pointoffset + k*pointcomps + roffset+6)] * (lenau/timeyr)
            line, = plt.plot(rs[:,c1], rs[:,c2])
            color = line.get_color()
            # kludge. find bh by mass
            if masses[k] >= 1e-2:
                print "bh was particle", k
                plt.plot([rs[-1,c1]], [rs[-1,c2]], 'o', markersize=bh_markersize, color=color)
            else:
                plt.plot([rs[-1,c1]], [rs[-1,c2]], 'o', color=color)
            # plot (initial) velocities
            #plt.quiver([rs[-1,0]], [rs[-1,1]], [vs[-1,0]], [vs[-1,1]], **quiver_params)
            # plot all velocities
            #plt.quiver(rs[:,c1], rs[:,c2], vs[:,c1], vs[:,c2], **quiver_params)

    bh_markersize = 10
    quiver_params = {
            'headwidth' : 2.0,
            'headlength' : 2.0,
            'width': 0.002,
            }

    fig = plt.figure()
    plt.subplot(221)
    plt.title('xy-projection, AU')
    plot_components(0, 1)


    plt.subplot(222)
    plt.title('xz-projection, AU')
    plot_components(0, 2)

    plt.subplot(223)
    plt.title('yz-projection, AU')
    plot_components(1, 2)

    plt.tight_layout()
    plt.show()

if 0:
    plt.ioff()
    fig = plt.figure(figsize=(7,6))
    xy = fig.add_subplot(221, aspect='equal')
    xy.set_title("xy-projection, t = {0:8.2f} yr".format(data[0,0]*0.1561859405615804))
    xy.set_xlim(-19000,19000)
    xy.set_ylim(-19000,19000)
    xy.set_xlabel("x (AU)")
    xy.set_ylabel("y (AU)")
    xy.arrow( -18000, -18000, 4000, 0, head_width=1000, head_length=1000, color='red')
    xy.arrow( -18000, -18000, 0, 4000, head_width=1000, head_length=1000, color='green')
    xz = fig.add_subplot(222, aspect='equal')
    xz.set_title('xz-projection')
    xz.set_xlim(-19000,19000)
    xz.set_ylim(-19000,19000)
    xz.set_xlabel("x (AU)")
    xz.set_ylabel("z (AU)")
    xz.arrow( -18000, -18000, 4000, 0, head_width=1000, head_length=1000, color='red')
    xz.arrow( -18000, -18000, 0, 4000, head_width=1000, head_length=1000, color='blue')
    yz = fig.add_subplot(223, aspect='equal')
    yz.set_title('yz-projection')
    yz.set_xlim(-19000,19000)
    yz.set_ylim(-19000,19000)
    yz.set_xlabel("y (AU)")
    yz.set_ylabel("z (AU)")
    yz.arrow( -18000, -18000, 4000, 0, head_width=1000, head_length=1000, color='green')
    yz.arrow( -18000, -18000, 0, 4000, head_width=1000, head_length=1000, color='blue')
    plt.tight_layout()
    rs0 = data[:, (pointoffset + 0*pointcomps + roffset):(pointoffset + 0*pointcomps + roffset + 3)] * lenau
    vs0 = data[:, (pointoffset + 0*pointcomps + roffset+3):(pointoffset + 0*pointcomps + roffset+6)] * (lenau/timeyr)
    rs1 = data[:, (pointoffset + 1*pointcomps + roffset):(pointoffset + 1*pointcomps + roffset + 3)] * lenau
    vs1 = data[:, (pointoffset + 1*pointcomps + roffset+3):(pointoffset + 1*pointcomps + roffset+6)] * (lenau/timeyr)
    line11, = xy.plot([rs0[0,0]], [rs0[0,1]], 'o')
    line12, = xy.plot([rs1[0,0]], [rs1[0,1]], 'o')
    color1 = line12.get_color()
    line13, = xy.plot([rs1[0,0]], [rs1[0,1]], color=color1)
    line21, = xz.plot([rs0[0,0]], [rs0[0,2]], 'o')
    line22, = xz.plot([rs1[0,0]], [rs1[0,2]], 'o')
    color2 = line22.get_color()
    line23, = xz.plot([rs1[0,0]], [rs1[0,2]], color=color2)
    line31, = yz.plot([rs0[0,1]], [rs0[0,2]], 'o')
    line32, = yz.plot([rs1[0,1]], [rs1[0,2]], 'o')
    color3 = line32.get_color()
    line33, = yz.plot([rs1[0,1]], [rs1[0,2]], color=color3)
    plt.savefig('results/anim/%05d.png' %(0))
    for k in range(1,rows):
        m = k - 500
        if (m < 0):
            m = 0

        xy.set_title("xy-projection, t = {0:8.2f} yr".format(data[k,0]*0.1561859405615804))
        line11.set_xdata([rs0[k,0]])
        line11.set_ydata([rs0[k,1]])
        line12.set_xdata([rs1[k,0]])
        line12.set_ydata([rs1[k,1]])
        line13.set_xdata([rs1[m:k,0]])
        line13.set_ydata([rs1[m:k,1]])

        line21.set_xdata([rs0[k,0]])
        line21.set_ydata([rs0[k,2]])
        line22.set_xdata([rs1[k,0]])
        line22.set_ydata([rs1[k,2]])
        line23.set_xdata([rs1[m:k,0]])
        line23.set_ydata([rs1[m:k,2]])

        line31.set_xdata([rs0[k,1]])
        line31.set_ydata([rs0[k,2]])
        line32.set_xdata([rs1[k,1]])
        line32.set_ydata([rs1[k,2]])
        line33.set_xdata([rs1[m:k,1]])
        line33.set_ydata([rs1[m:k,2]])
        fig.canvas.draw()
        plt.savefig('results/anim/%05d.png' %(k))
        fig.canvas.flush_events()
