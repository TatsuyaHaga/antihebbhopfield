#!/usr/bin/env python3

import numpy
import sys
sys.path.append("..")
from meanfield_share import calc_meanfield_montecarlo

if __name__=="__main__":
    #parameters
    P=71
    R=10**6
    p=0.5
    param_arr=[1.5, -1.5]

    Phalf=int((P+1)//2)
    init=numpy.zeros(P)
    init[Phalf-1]=1.0
    ext_input=numpy.zeros(P)

    results_overlap=[]
    results_cor=[]
    for i in range(len(param_arr)):
        print(param_arr[i])
        tmp=calc_meanfield_montecarlo(P,R,param_arr[i],p,init,ext_input)
        results_overlap.append(tmp[0])
        results_cor.append(tmp[1])

    numpy.savetxt("overlap.csv", results_overlap, delimiter=",")
    numpy.savetxt("cor.csv", results_cor, delimiter=",")

