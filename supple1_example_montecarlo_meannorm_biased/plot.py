#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

overlap=numpy.loadtxt("overlap.csv", delimiter=",")
cor=numpy.loadtxt("cor.csv", delimiter=",")
P=overlap.shape[1]
Phalf=cor.shape[1]

param_arr=[1.5, -1.5] #lambda
ls_arr=["-", "--"]

pylab.figure(figsize=(2,3))

pylab.subplot(2,1,1)
#pylab.plot(numpy.arange(P), [0]*P, "--", color="black", lw=1)
for i in range(len(param_arr)):
    pylab.plot(numpy.arange(1,P+1), overlap[i,:], ls_arr[i], color="black", label="c="+str(param_arr[i]))
pylab.plot([1,P+1], [0,0], color="gray")
pylab.xlim([1,P+1])
pylab.xticks(numpy.arange(1,P+1,10))
pylab.ylim([-0.3,1])
pylab.xlabel("pattern")
pylab.ylabel("overlap")
pylab.legend(loc="upper right")
seaborn.despine()

pylab.subplot(2,1,2)
#pylab.plot(numpy.arange(Phalf), [0]*Phalf, "--", color="black", lw=1)
for i in range(len(param_arr)):
    pylab.plot(numpy.arange(0,Phalf), cor[i,:], ls_arr[i], color="black", label="c="+str(param_arr[i]))
pylab.plot([0,Phalf], [0,0], color="gray")
pylab.xlim(0,Phalf)
pylab.xticks(numpy.arange(0,Phalf,10))
pylab.ylim([-0.3,1])
pylab.xlabel("distance")
pylab.ylabel("correlation")
pylab.legend(loc="upper right")
seaborn.despine()

pylab.tight_layout()
pylab.savefig("plot.svg")
