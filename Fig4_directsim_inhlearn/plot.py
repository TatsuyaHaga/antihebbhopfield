#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab

time=numpy.loadtxt("time_sec.csv", delimiter=",")
overlap=numpy.loadtxt("overlap.csv", delimiter=",")
overlap[overlap<0.0]=0.0

pylab.close()
pylab.figure(figsize=(6,3))
pylab.imshow(overlap.T, interpolation="none", aspect="auto")
pylab.xlabel("Time")
pylab.ylabel("pattern")
pylab.colorbar()
pylab.tight_layout()
pylab.savefig("overlap.png")

filt=time<20.0

pylab.close()
pylab.figure(figsize=(6,3))
pylab.imshow(overlap[filt,:].T, interpolation="none", aspect="auto")
pylab.xlabel("Time")
pylab.ylabel("pattern")
pylab.colorbar()
pylab.tight_layout()
pylab.savefig("overlap_begin.png")

filt=(time>=100.0)*(time<120.0)

pylab.close()
pylab.figure(figsize=(6,3))
pylab.imshow(overlap[filt,:].T, interpolation="none", aspect="auto")
pylab.xlabel("Time")
pylab.ylabel("pattern")
pylab.colorbar()
pylab.tight_layout()
pylab.savefig("overlap_end.png")

filt=(time>=120.0)

pylab.close()
pylab.figure(figsize=(6,3))
pylab.imshow(overlap[filt,:].T, interpolation="none", aspect="auto")
pylab.xlabel("Time [s]")
pylab.ylabel("pattern")
pylab.colorbar()
pylab.tight_layout()
pylab.savefig("overlap_perturb.png")
