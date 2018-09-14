#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

a_arr=numpy.loadtxt("a_arr.csv", delimiter=",")
theta_arr=numpy.loadtxt("theta_arr.csv", delimiter=",")
overlap=numpy.load("overlap.npy")

maxoverlap=numpy.max(overlap, axis=2)

pylab.close()
pylab.figure(figsize=(2.5,2.5))
pylab.pcolormesh(theta_arr,a_arr,maxoverlap,cmap="jet")
pylab.xlabel(r"$\theta$")
pylab.ylabel("a")
pylab.colorbar()
pylab.tight_layout()
pylab.savefig("maxoverlap_2D.pdf")
