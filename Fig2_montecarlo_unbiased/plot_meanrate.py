#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

#plot meanrate
meanrate=numpy.loadtxt("meanrate.csv", delimiter=",")
param=meanrate[:,0]
meanrate=meanrate[:,1:]

order=numpy.argsort(param)
param=param[order]
meanrate=meanrate[order,:]

pylab.close()
#pylab.figure(figsize=(5,6))
pylab.figure(figsize=(2.5,2))
pylab.plot(param,meanrate,lw=2,color="black")
pylab.ylim([-1.0,1.0])
pylab.xlabel("c")
pylab.ylabel("max meanrate")
seaborn.despine()

pylab.tight_layout()
pylab.savefig("meanrate.svg")
