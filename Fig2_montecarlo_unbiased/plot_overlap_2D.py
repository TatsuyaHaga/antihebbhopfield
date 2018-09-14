#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

overlap=numpy.loadtxt("overlap.csv", delimiter=",")
param=overlap[:,0]
overlap=overlap[:,1:]
P=overlap.shape[1]

order=numpy.argsort(param)
param=param[order]
overlap=overlap[order]

pylab.close()
pylab.figure(figsize=(3,3))
pylab.pcolormesh(numpy.arange(P),param,overlap,cmap="jet")
pylab.xlabel("pattern")
pylab.ylabel("lambda")
pylab.colorbar()
pylab.tight_layout()
pylab.savefig("overlap_2D.pdf")
