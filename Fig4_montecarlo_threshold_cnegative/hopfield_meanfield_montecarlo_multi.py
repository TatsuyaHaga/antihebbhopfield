#!/usr/bin/env python3

import multiprocessing
import numpy
import scipy.optimize

def overlap_eq(m, e_combi, e_combi_w,theta,a):
    return (1.0-a**2)*m-numpy.sum(e_combi*(numpy.sign((1.0-a**2)*(e_combi_w@m)-theta).reshape((e_combi.shape[0],1))), axis=0)/len(e_combi)

def calc_meanfield(q,P,R,lamb,a,theta,acount,thetacount):
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

    q.put((acount,thetacount,overlap))
    #return overlap

if __name__=="__main__":
    #parameters
    P=71
    R=10**6
    param=-1.5
    a_arr=-numpy.arange(0.0,1.0,0.1)
    theta_arr=numpy.arange(-0.5,0.51,0.05)
    Na=len(a_arr)
    Ntheta=len(theta_arr)
    Phalf=int((P+1)//2)
    Nprocess=40

    que=multiprocessing.Queue()
    process_arr=[]
    process_num=0
    results_overlap=numpy.zeros([Na,Ntheta,P])

    for acount in range(Na):
        for thetacount in range(Ntheta):
            a=a_arr[acount]
            theta=theta_arr[thetacount]
            print(a,theta)
            process_arr.append(multiprocessing.Process(target=calc_meanfield, args=(que,P,R,param,a,theta,acount,thetacount)))
            process_arr[-1].start()
            process_num+=1
            if process_num>=Nprocess:
                for i in range(process_num):
                    process_arr[i].join()
                for i in range(process_num):
                    res=que.get()
                    results_overlap[res[0],res[1],:]=res[2]
                process_arr.clear()
                process_num=0

    for i in range(process_num):
        process_arr[i].join()
    for i in range(process_num):
        res=que.get()
        results_overlap[res[0],res[1],:]=res[2]

    numpy.savetxt("a_arr.csv", a_arr, delimiter=",")
    numpy.savetxt("theta_arr.csv", theta_arr, delimiter=",")
    numpy.save("overlap.npy", results_overlap) 
