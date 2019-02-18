#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

param_val=numpy.loadtxt("param_val.csv", delimiter=",")
param_val=numpy.around(param_val,decimals=2)
Nparam=len(param_val)

#plot threshold 
threshold=numpy.loadtxt("threshold.csv", delimiter=",")
param=numpy.around(threshold[:,0],decimals=2)
threshold=threshold[:,1:]

mean=numpy.zeros(Nparam)
std=numpy.zeros(Nparam)
for i in range(Nparam):
    tmp=threshold[param==param_val[i]]
    mean[i]=numpy.mean(tmp)
    std[i]=numpy.std(tmp)

pylab.close()
pylab.figure(figsize=(1.5,1.5))
pylab.fill_between(param_val,numpy.maximum(mean-std,0),mean+std,facecolor="gray")
pylab.plot(param_val,mean,color="black")
pylab.ylim([0.0,0.3])
pylab.yticks([0,0.1,0.2,0.3])
pylab.xlabel("c")
pylab.ylabel("Threshold")
seaborn.despine()

pylab.tight_layout()
pylab.savefig("plot.svg")
