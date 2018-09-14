#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

a_arr=numpy.loadtxt("a_arr.csv", delimiter=",")
theta_arr=numpy.loadtxt("theta_arr.csv", delimiter=",")
overlap_data=numpy.load("overlap.npy")
P=overlap_data.shape[2]
Phalf=int((P+1)//2)

cor_num=numpy.zeros([len(a_arr),len(theta_arr)])
for i in range(len(a_arr)):
    for j in range(len(theta_arr)):
        overlap=overlap_data[i,j]
        corON=numpy.where(overlap<1e-4)[0]
        corON=corON[corON>Phalf]
        if len(corON)>0:
            cor_num[i,j]=corON[0]-Phalf-1
        else:
            cor_num[i,j]=Phalf-1

pylab.close()
pylab.figure(figsize=(2.5,2.5))
pylab.pcolormesh(theta_arr,a_arr,cor_num,cmap="jet")
pylab.xlabel(r"$\theta$")
pylab.ylabel("a")
pylab.colorbar()
pylab.tight_layout()
pylab.savefig("cornum_2D.pdf")
