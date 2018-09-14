#!/usr/bin/env python3

import numpy
import pylab

overlap_mean=numpy.loadtxt("overlap.csv", delimiter=",")
P=len(overlap_mean)

pylab.close()
pylab.plot(numpy.arange(0,P),[0]*P, "--", color="black")
pylab.plot(overlap_mean)
pylab.xlim([0,P])
pylab.xlabel("pattern")
pylab.ylabel("overlap")
pylab.savefig("overlap.svg")

