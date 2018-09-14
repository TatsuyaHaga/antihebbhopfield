#!/usr/bin/env python3

import multiprocessing
import numpy
import scipy.optimize

def overlap_eq(m, e_combi, e_combi_w,theta,a):
    return (1.0-a**2)*m-numpy.sum(e_combi*(numpy.sign((1.0-a**2)*(e_combi_w@m)-theta).reshape((e_combi.shape[0],1))), axis=0)/len(e_combi)

def mean_rate(m, e_combi_w):
    return numpy.sum(numpy.sign(e_combi_w@m))/len(e_combi_w)

def calc_meanfield(q,P,R,lamb,a,theta):
    Phalf=int((P+1)//2)
    f=0.5*(a+1.0)

    init=numpy.zeros(P)
    init[Phalf-1]=1.0

    #possible combination of variables
    e_combi=(2*(numpy.random.rand(R, P)<f)-1)-a
    e_combi_w=lamb*e_combi+numpy.roll(e_combi, 1, axis=1)+numpy.roll(e_combi, -1, axis=1)

    #print("calculate overlaps.")
    sol=scipy.optimize.root(overlap_eq, x0=init, method="lm", args=(e_combi, e_combi_w,theta,a))
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
    #print(meanr, cor)

    q.put((lamb,overlap,cor,meanr))
    #return overlap

if __name__=="__main__":
    #parameters
    P=71
    R=10**6
    a=-0.8
    theta=0.0
    maxparam=3
    param_mesh=0.05
    tmp=int(numpy.round(maxparam/param_mesh))
    param_arr=list(map(lambda x:x*param_mesh, range(-tmp,tmp+1)))
    Phalf=int((P+1)//2)
    Nprocess=40

    que=multiprocessing.Queue()
    process_arr=[]
    results_overlap=[]
    results_cor=[]
    results_meanr=[]
    process_num=0
    for param in param_arr:
        print(param)
        process_arr.append(multiprocessing.Process(target=calc_meanfield, args=(que,P,R,param,a,theta)))
        process_arr[-1].start()
        process_num+=1
        if process_num>=Nprocess:
            for i in range(process_num):
                process_arr[i].join()
            for i in range(process_num):
                tmp=que.get()
                results_overlap.append(numpy.concatenate([tmp[0:1],tmp[1]], axis=0))
                results_cor.append(numpy.concatenate([tmp[0:1],tmp[2]], axis=0))
                results_meanr.append(numpy.array([tmp[0],tmp[3]]))
            process_arr.clear()
            process_num=0

    for i in range(process_num):
        process_arr[i].join()
    for i in range(process_num):
        tmp=que.get()
        results_overlap.append(numpy.concatenate([tmp[0:1],tmp[1]], axis=0))
        results_cor.append(numpy.concatenate([tmp[0:1],tmp[2]], axis=0))
        results_meanr.append(numpy.array([tmp[0],tmp[3]]))
    numpy.savetxt("overlap.csv", results_overlap, delimiter=",") 
    numpy.savetxt("cor.csv", results_cor, delimiter=",") 
    numpy.savetxt("meanrate.csv", results_meanr, delimiter=",") 
