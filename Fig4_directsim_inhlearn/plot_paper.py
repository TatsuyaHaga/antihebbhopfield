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

filt1=(time>=100.0)*(time<120.0)
filt2=(time>=120.0)*(time<140.0)
colorbar_sw=False

for filt_sw in [1,2]:
    if filt_sw==1:
        filt=filt1
    else:
        filt=filt2
    pylab.close()
    pylab.figure(figsize=(3,2.5))
    pylab.subplot2grid((3,1),(0,0),rowspan=1)
    pylab.plot(time[filt],Ach[filt], color="black")
    pylab.xlim([numpy.min(time[filt]), numpy.max(time[filt])])
    pylab.xticks([])
    pylab.ylim([0.0,1.0])
    pylab.yticks([0,1])
    pylab.ylabel("Inhibition\nratio")
    seaborn.despine()
    pylab.subplot2grid((3,1),(1,0),rowspan=2)
    pylab.imshow(overlap[filt,:].T, interpolation="none", aspect="auto",cmap="viridis", extent=[numpy.min(time[filt]), numpy.max(time[filt]), overlap.shape[1], 1])
    #pylab.plot(mean[filt], color="white")
    pylab.clim([0,1])
    pylab.xticks([numpy.min(time[filt]), numpy.max(time[filt])])
    pylab.xlabel("Time [s]")
    pylab.ylabel("Pattern")
    if colorbar_sw:
        pylab.colorbar()

    pylab.tight_layout()
    fname="overlap"
    if filt_sw==1:
        fname+="_end"
    else:
        fname+="_perturb"
    if colorbar_sw:
        fname+="_colorbar"
    pylab.savefig(fname+".pdf")

