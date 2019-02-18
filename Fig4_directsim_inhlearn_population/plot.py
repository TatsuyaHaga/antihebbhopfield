#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

pylab.rcParams["font.size"]=6

overlap=numpy.loadtxt("overlap.csv", delimiter=",")
time=numpy.loadtxt("time_sec.csv", delimiter=",")
Ach=numpy.loadtxt("Ach.csv", delimiter=",")
stimpos=numpy.loadtxt("stimpos.csv", delimiter=",")

x=numpy.arange(overlap.shape[1]).reshape((1,overlap.shape[1]))
dist=overlap/numpy.sum(overlap,axis=1,keepdims=True)
mean=numpy.sum(dist*x,axis=1)
var=numpy.sum(dist*(x-mean.reshape((len(mean),1)))**2,axis=1)

time2=time[range(0,len(time),40)] #200ms bin
mean2=mean[range(0,len(mean),40)]
move=numpy.abs(numpy.diff(mean2))
move=numpy.append(move,0)

pylab.close()
pylab.figure(figsize=(3,3))
pylab.imshow(overlap.T, interpolation="none", aspect="auto", cmap="viridis")
pylab.xlabel("time step")
pylab.ylabel("pattern")
pylab.colorbar()
pylab.tight_layout()
pylab.savefig("overlap.pdf")

pylab.close()
pylab.figure(figsize=(3,3))
pylab.imshow(overlap[:5000,:].T, interpolation="none", aspect="auto", cmap="viridis")
pylab.xlabel("time step")
pylab.ylabel("pattern")
pylab.colorbar()
pylab.tight_layout()
pylab.savefig("overlap_begin.pdf")

plot_start=120.0#sec
filt=(time>plot_start)
filt2=(time2>plot_start)

for colorbar_sw in [False, True]:
    pylab.close()
    pylab.figure(figsize=(3,4))
    pylab.subplot2grid((5,1),(0,0),rowspan=1)
    pylab.plot(time[filt],Ach[filt], color="black")
    pylab.xlim([numpy.min(time[filt]), numpy.max(time[filt])])
    pylab.xticks([])
    pylab.ylim([0.0,1.0])
    pylab.yticks([0,0.5,1])
    pylab.ylabel("Inhibition ratio")
    seaborn.despine()
    pylab.subplot2grid((5,1),(1,0),rowspan=2)
    pylab.imshow(overlap[filt].T, interpolation="none", aspect="auto",cmap="viridis")
    #pylab.plot(mean[filt], color="white")
    pylab.clim([0,1])
    #pylab.xlabel("time step")
    pylab.xticks([])
    pylab.ylabel("Pattern")
    if colorbar_sw:
        pylab.colorbar()
    pylab.subplot2grid((5,1),(3,0),rowspan=1)
    pylab.plot(time[filt],var[filt], color="black")
    pylab.xlim([numpy.min(time[filt]), numpy.max(time[filt])])
    pylab.xticks([])
    #pylab.xlabel("Time [s]")
    pylab.ylabel("Variance")
    seaborn.despine()
    pylab.subplot2grid((5,1),(4,0),rowspan=1)
    pylab.plot(time2[filt2],move[filt2], color="black")
    pylab.xlim([numpy.min(time2[filt2]), numpy.max(time2[filt2])])
    pylab.xlabel("Time [s]")
    pylab.ylabel("Displacement")
    seaborn.despine()
    pylab.tight_layout()
    if colorbar_sw:
        pylab.savefig("overlap_end_colorbar.pdf")
    else:
        pylab.savefig("overlap_end.pdf")

