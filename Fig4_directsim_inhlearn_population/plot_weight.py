#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

pylab.rcParams["font.size"]=6

time=numpy.loadtxt("time_sec.csv", delimiter=",")
wlocal=numpy.loadtxt("wlocal.csv", delimiter=",")
wglobal=numpy.loadtxt("wglobal.csv", delimiter=",")

plot_end=100.0#sec
filt=(time<plot_end)

pylab.close()
pylab.figure(figsize=(2,1))
pylab.plot(time[filt],wlocal[filt], label="local inh")
pylab.plot(time[filt],wglobal[filt], label="global inh")
pylab.yticks([0,2,4])
pylab.xlabel("Time [s]")
pylab.ylabel("Weight")
pylab.legend()
seaborn.despine()
pylab.tight_layout()
pylab.savefig("weight.svg")

