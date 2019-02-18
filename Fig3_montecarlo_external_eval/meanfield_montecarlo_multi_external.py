#!/usr/bin/env python3

import multiprocessing
import numpy
import sys
sys.path.append("..")
from meanfield_share import calc_meanfield_montecarlo

def calc_meanfield_multi_external(q,P,R,c,p,init,ext_pos,rand_seed):
    numpy.random.seed(rand_seed)
    Pinit=numpy.argmax(init)

    input_amp=0.0
    overlap=init
    num_arr=numpy.arange(P)
    gravity_center=numpy.sum(overlap*num_arr)/numpy.sum(overlap)
    while numpy.abs(gravity_center-Pinit)<numpy.abs(gravity_center-(Pinit+ext_pos)):
        input_amp+=0.01
        b=numpy.zeros(P)
        b[Pinit+ext_pos]=input_amp
        overlap,cor=calc_meanfield_montecarlo(P,R,c,p,init,b)
        gravity_center=numpy.sum(overlap*num_arr)/numpy.sum(overlap)
        if input_amp>=0.3:
            break

    q.put((c,input_amp))

if __name__=="__main__":
    #parameters
    p=float(sys.argv[1])
    ext_pos=int(sys.argv[2])
    print("p=", p, "ext_pos=", ext_pos)

    P=71
    R=10**6
    Nrepeat=5
    maxparam=1.5
    param_mesh=0.1
    tmp=int(numpy.round(maxparam/param_mesh))
    param_arr=list(map(lambda x:x*param_mesh, range(-tmp,tmp+1)))
    param_arr=numpy.around(param_arr, decimals=2)
    Nparam=len(param_arr)

    Nprocess=85

    Phalf=int((P+1)//2)
    init=numpy.zeros(P)
    init[Phalf-1]=1.0

    #start parallel calculation -> get results
    que=multiprocessing.Queue()
    process_arr=[]
    results_threshold=[]
    process_num=0
    rand_seed=0
    for param_count in range(Nparam):
        for ite in range(Nrepeat):
            param=param_arr[param_count]
            print(param,ite)
            process_arr.append(multiprocessing.Process(target=calc_meanfield_multi_external, args=(que,P,R,param,p,init,ext_pos,rand_seed)))
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
                    results_threshold.append(tmp)
                process_arr.clear()
                process_num=0

    #save to file
    numpy.savetxt("param_val.csv", param_arr, delimiter=",")
    numpy.savetxt("threshold.csv", results_threshold, delimiter=",") 
