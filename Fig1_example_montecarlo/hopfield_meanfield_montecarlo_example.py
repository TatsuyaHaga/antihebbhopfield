#!/usr/bin/env python3

import numpy
import scipy.optimize

def overlap_eq(m, e_combi, e_combi_w):
    return m-numpy.sum(e_combi*(numpy.sign(e_combi_w@m).reshape((e_combi.shape[0],1))), axis=0)/len(e_combi)

def mean_rate(m, e_combi_w):
    return numpy.sum(numpy.sign(e_combi_w@m))/len(e_combi_w)

def calc_meanfield(P,R,lamb):
    Phalf=int((P+1)//2)

    init=numpy.zeros(P)
    init[Phalf-1]=1.0

    #possible combination of variables
    e_combi=2*(numpy.random.rand(R, P)<0.5)-1
    e_combi_w=lamb*e_combi+numpy.roll(e_combi, 1, axis=1)+numpy.roll(e_combi, -1, axis=1)

    #print("calculate overlaps.")
    sol=scipy.optimize.root(overlap_eq, x0=init, method="lm", args=(e_combi, e_combi_w))
    overlap=sol.x
    #print(sol, overlap_eq(overlap, e_combi, e_combi_w, c, a))

    #print("calculate correlation.")
    cor=numpy.zeros(Phalf)
    meanr=mean_rate(overlap, e_combi_w)
    overlap_w=lamb*overlap+numpy.roll(overlap, 1)+numpy.roll(overlap, -1)
    for i in range(Phalf):
        S1=numpy.sign(e_combi@overlap_w)
        S2=numpy.sign(e_combi@numpy.roll(overlap_w, i))
        cor[i]=numpy.sum((S1-meanr)*(S2-meanr))/(len(e_combi)*(1.0-meanr**2))
    print(meanr, cor)

    return (overlap, cor)

if __name__=="__main__":
    #parameters
    P=71
    R=10**6
    param_arr=[1.5, -1.5]

    results_overlap=[]
    results_cor=[]
    for i in range(len(param_arr)):
        print(param_arr[i])
        tmp=calc_meanfield(P,R,param_arr[i])
        results_overlap.append(tmp[0])
        results_cor.append(tmp[1])

    numpy.savetxt("overlap.csv", results_overlap, delimiter=",")
    numpy.savetxt("cor.csv", results_cor, delimiter=",")

