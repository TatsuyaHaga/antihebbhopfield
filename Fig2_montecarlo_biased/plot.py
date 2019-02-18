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

#plot max overlap
overlap=numpy.loadtxt("overlap.csv", delimiter=",")
param=numpy.around(overlap[:,0],decimals=2)
overlap=overlap[:,1:]
max_overlap=numpy.max(overlap, axis=1)

mean=numpy.zeros(Nparam)
std=numpy.zeros(Nparam)
for i in range(Nparam):
    tmp=max_overlap[param==param_val[i]]
    mean[i]=numpy.mean(tmp)
    std[i]=numpy.std(tmp)

pylab.close()
#pylab.figure(figsize=(5,6))
pylab.figure(figsize=(1.5,2.5))
pylab.subplot(2,1,1)
pylab.fill_between(param_val,numpy.maximum(mean-std,0),mean+std,facecolor="gray")
pylab.plot(param_val,mean,color="black")
pylab.xticks([-2,0,2])
pylab.ylim([0.0,1.0])
pylab.xlabel("c")
pylab.ylabel("max overlap")
seaborn.despine()

#plot cor_num
cor=numpy.loadtxt("cor.csv", delimiter=",")
param_cor=cor[:,0]
cor=cor[:,1:]
Phalf=cor.shape[1]

cor_num=numpy.zeros(len(param_cor))
for i in range(len(param_cor)):
    tmp=numpy.where(cor[i,:]<1e-2)[0]
    if len(tmp)>0:
        cor_num[i]=numpy.min(tmp)-1
    else:
        cor_num[i]=Phalf-1

mean=numpy.zeros(Nparam)
std=numpy.zeros(Nparam)
for i in range(Nparam):
    tmp=cor_num[(param==param_val[i])]
    mean[i]=numpy.mean(tmp)
    std[i]=numpy.std(tmp)

pylab.subplot(2,1,2)
pylab.plot(param,[5]*len(param), "--", color="gray")
pylab.fill_between(param_val,numpy.maximum(mean-std,0),mean+std,facecolor="gray")
pylab.plot(param_val,mean,color="black")
pylab.ylim([0,Phalf])
pylab.xticks([-2,0,2])
pylab.xlabel("c")
pylab.ylabel("Nc")
seaborn.despine()
pylab.tight_layout()
pylab.savefig("plot.svg")
