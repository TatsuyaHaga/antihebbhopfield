#!/usr/bin/python3

import numpy

P=71
Phalf=int((P+1)//2)
N=5000

p_one=0.5
a=2*p_one-1
lamb=-1.5
theta=0.0
tau=10.0

max_transit=200
sample_num=5
overlap_mean=numpy.zeros(P)
for ite in range(sample_num):
    pattern=2.0*(numpy.random.rand(P,N)<p_one).astype(numpy.float)-1.0
    pattern_plus=numpy.roll(pattern, 1, axis=0)
    W=(lamb*(pattern.T-a)@(pattern-a)+(pattern.T-a)@(pattern_plus-a)+(pattern_plus.T-a)@(pattern-a))/N
    W[numpy.eye(N, dtype=numpy.bool)]=0

    S=pattern[Phalf,:]+0.0
    X=S+0.0
    for t in range(max_transit):
        Sprev=S+0.0
        X+=(S-X)/tau
        S=numpy.sign(W@X-theta)
        if numpy.all(S==Sprev):
            print("converge. t=", t)
            break
    overlap_mean+=(pattern@S)/(N*sample_num)

numpy.savetxt("overlap.csv", overlap_mean, delimiter=",")
