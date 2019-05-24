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

filt=(time<100.0)
time=time[filt]
wlocal=wlocal[filt]/numpy.max(wlocal[filt])
wglobal=wglobal[filt]/numpy.max(wglobal[filt])

pylab.close()
pylab.figure(figsize=(2,1))
pylab.plot(time,wlocal, label="local inh")
pylab.plot(time,wglobal, label="global inh")
pylab.yticks([0,1])
pylab.xlabel("Time [s]")
pylab.ylabel("Maximum\nweight\nchange")
pylab.legend()
seaborn.despine()
pylab.tight_layout()
pylab.savefig("weight.svg")

