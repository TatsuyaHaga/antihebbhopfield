#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

overlap=numpy.loadtxt("overlap.csv", delimiter=",")
P=overlap.shape[1]
Phalf=int((P-1)//2)

param_arr=[1.5, -1.5] #lambda
ls_arr=["-", "--"]

pylab.figure(figsize=(2,1.5))

#pylab.plot(numpy.arange(P), [0]*P, "--", color="black", lw=1)
for i in range(len(param_arr)):
    pylab.plot(numpy.arange(1,P+1), overlap[i,:], ls_arr[i], color="black", label="c="+str(param_arr[i]))
pylab.xlim([1,P+1])
pylab.xticks(numpy.arange(1,P+1,10))
pylab.ylim([0,1])
pylab.xlabel("pattern")
pylab.ylabel("overlap")
pylab.legend(loc="upper right")
seaborn.despine()

pylab.tight_layout()
pylab.savefig("plot.svg")
