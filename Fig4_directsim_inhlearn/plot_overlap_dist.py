#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

time=numpy.loadtxt("time_sec.csv", delimiter=",")
Ach=numpy.loadtxt("Ach.csv", delimiter=",")
overlap=numpy.loadtxt("overlap.csv", delimiter=",")
stim=numpy.loadtxt("stim.csv", delimiter=",")

center=int(overlap.shape[1]//2)

before=(time>100)*(time<120)
after=(time>120)
for setting in ["before", "after"]:
    if setting=="before":
        lim=before
    elif setting=="after":
        lim=after
    t1=numpy.where(lim*(Ach>0.8)*(stim<0))[0]
    t2=numpy.where(lim*(Ach<0.2)*(stim<0))[0]

    tmp=numpy.zeros([len(t1), overlap.shape[1]])
    for i in range(len(t1)):
        tmp[i,:]=numpy.roll(overlap[t1[i],:], center-numpy.argmax(overlap[t1[i],:]))
    mean1=numpy.mean(tmp,axis=0)
    std1=numpy.std(tmp,axis=0)

    tmp=numpy.zeros([len(t2), overlap.shape[1]])
    for i in range(len(t2)):
        tmp[i,:]=numpy.roll(overlap[t2[i],:], center-numpy.argmax(overlap[t2[i],:]))
    mean2=numpy.mean(tmp,axis=0)
    std2=numpy.std(tmp,axis=0)

    x=numpy.arange(len(mean1))-center 
    pylab.close()
    pylab.figure(figsize=(1.5,1.5))
    pylab.plot(x, mean1, color="r")
    pylab.fill_between(x, mean1-std1, mean1+std1, facecolor="r",alpha=0.5)
    pylab.plot(x, mean2, color="g")
    pylab.fill_between(x, mean2-std2, mean2+std2, facecolor="g",alpha=0.5)
    pylab.plot([numpy.min(x),numpy.max(x)], [0,0], color="black")
    pylab.ylim([-0.2,1.1])
    pylab.yticks([0,0.5,1])
    pylab.xlim([numpy.min(x),numpy.max(x)])
    pylab.xticks([numpy.min(x),0,numpy.max(x)])
    pylab.xlabel("pattern")
    pylab.ylabel("overlap")
    pylab.tight_layout()
    pylab.savefig("overlapdist"+setting+".pdf")

