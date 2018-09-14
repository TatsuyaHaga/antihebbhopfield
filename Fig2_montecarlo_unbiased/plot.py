#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

#plot max overlap
overlap=numpy.loadtxt("overlap.csv", delimiter=",")
param=overlap[:,0]
overlap=overlap[:,1:]
max_overlap=numpy.max(overlap, axis=1)

order=numpy.argsort(param)
param=param[order]
overlap=overlap[order,:]
max_overlap=max_overlap[order]

pylab.close()
#pylab.figure(figsize=(5,6))
pylab.figure(figsize=(2.5,3))
pylab.subplot(2,1,1)
pylab.plot(param,max_overlap,lw=2,color="black")
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

order=numpy.argsort(param_cor)
param_cor=param_cor[order]
cor=cor[order,:]
cor_num=cor_num[order]

if numpy.any(param!=param_cor):
    print("Error: param_overlap!=param_cor")

pylab.subplot(2,1,2)
pylab.plot(param,cor_num,lw=2,color="black")
#pylab.plot(param,[5]*len(param))
pylab.ylim([0,Phalf])
pylab.xlabel("c")
pylab.ylabel("Nc")
seaborn.despine()
pylab.tight_layout()
pylab.savefig("plot.svg")
