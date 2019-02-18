#!/usr/bin/env python3

import multiprocessing
import numpy
import sys
sys.path.append("..")
from meanfield_share import calc_meanfield_montecarlo

def calc_meanfield_multi(q,P,R,c,p,init,b,rand_seed):
    numpy.random.seed(rand_seed)
    overlap,cor=calc_meanfield_montecarlo(P,R,c,p,init,b)

    q.put((c,overlap,cor))

if __name__=="__main__":
    #parameters
    P=71
    R=10**6
    Nrepeat=5
    p=float(sys.argv[1])
    maxparam=3
    param_mesh=0.05
    tmp=int(numpy.round(maxparam/param_mesh))
    param_arr=list(map(lambda x:x*param_mesh, range(-tmp,tmp+1)))
    param_arr=numpy.around(param_arr, decimals=2)
    Nparam=len(param_arr)

    Nprocess=40

    Phalf=int((P+1)//2)
    init=numpy.zeros(P)
    init[Phalf-1]=1.0
    ext_input=numpy.zeros(P)

    #start parallel calculation -> get results
    que=multiprocessing.Queue()
    process_arr=[]
    results_overlap=[]
    results_cor=[]
    process_num=0
    rand_seed=0
    for param_count in range(Nparam):
        for ite in range(Nrepeat):
            param=param_arr[param_count]
            print(param,ite)
            process_arr.append(multiprocessing.Process(target=calc_meanfield_multi, args=(que,P,R,param,p,init,ext_input,rand_seed)))
            rand_seed+=1
            process_arr[-1].start()
            process_num+=1
            if process_num>=Nprocess or (param_count+1==Nparam and ite+1==Nrepeat):
                for i in range(process_num):
                    process_arr[i].join()
                if que.empty():
                    print("Nothing was returned from child processes.")
                    exit()
                while not que.empty():
                    tmp=que.get()
                    results_overlap.append(numpy.concatenate([tmp[0:1],tmp[1]], axis=0))
                    results_cor.append(numpy.concatenate([tmp[0:1],tmp[2]], axis=0))
                process_arr.clear()
                process_num=0

    #save to file
    numpy.savetxt("param_val.csv", param_arr, delimiter=",")
    numpy.savetxt("overlap.csv", results_overlap, delimiter=",") 
    numpy.savetxt("cor.csv", results_cor, delimiter=",") 
