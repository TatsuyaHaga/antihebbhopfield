#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

cor=numpy.loadtxt("cor.csv", delimiter=",")
param=cor[:,0]
cor=cor[:,1:]
Phalf=cor.shape[1]

order=numpy.argsort(param)
param=param[order]
cor=cor[order]

pylab.close()
pylab.figure(figsize=(3,3))
pylab.pcolormesh(numpy.arange(Phalf),param,cor,cmap="jet")
pylab.xlabel("pattern")
pylab.ylabel("lambda")
pylab.colorbar()
pylab.tight_layout()
pylab.savefig("cor_2D.pdf")
