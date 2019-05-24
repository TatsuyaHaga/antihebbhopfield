#!/usr/bin/env python3

import itertools
import numpy
import scipy.optimize

def step(x):
    return (x>0) 

def overlap_cross(m,c):
    return c*m+numpy.roll(m,1)+numpy.roll(m,-1)

def overlap_eq(m, xi, c, V, R, b):
    return V*m-numpy.sum(xi*step(xi@(V*overlap_cross(m,c)+b)).reshape((R,1)), axis=0)/R

def mean_rate(m, xi, c, V, R, b):
    return numpy.sum(step(xi@(V*overlap_cross(m,c)+b)))/R

def calc_cor(overlap,pattern,P,R,c,p,b):
    V=p*(1-p)
    Phalf=int((P+1)//2)
    cor=numpy.zeros(Phalf)
    meanr=mean_rate(overlap, pattern, c, p*(1-p), R, b)
    Vmeanr=meanr*(1.0-meanr)
    overlap_w=overlap_cross(overlap,c)
    for i in range(Phalf):
        S1=step(pattern@(V*overlap_w+b))
        S2=step(pattern@(V*numpy.roll(overlap_w, i)+b))
        cor[i]=numpy.sum((S1-meanr)*(S2-meanr))/(R*Vmeanr)

    return cor

def calc_meanfield_exact(P,c,p,init,b):
    #possible combination of patterns 
    pattern=numpy.array(list(itertools.product([1,0], repeat=P)))-p
    R=len(pattern)

    #calculate overlaps
    sol=scipy.optimize.root(overlap_eq, x0=init, method="lm", args=(pattern, c,p*(1-p),R,b))
    overlap=sol.x
    cor=calc_cor(overlap,pattern,P,R,c,p,b)

    return (overlap,cor)

def calc_meanfield_montecarlo(P,R,c,p,init,b):
    #possible combination of patterns 
    pattern=(numpy.random.rand(R, P)<p).astype(numpy.float)-p

    #calculate overlaps
    sol=scipy.optimize.root(overlap_eq, x0=init, method="lm", args=(pattern, c,p*(1-p),R,b))
    overlap=sol.x
    cor=calc_cor(overlap,pattern,P,R,c,p,b)

    return (overlap,cor)

def calc_meanfield_montecarlo_meannorm(P,R,c,p,init,b):
    #possible combination of patterns 
    pattern=(numpy.random.rand(R, P)<p).astype(numpy.float)
    pattern=pattern-numpy.sum(pattern,axis=1,keepdims=True)/P

    #calculate overlaps
    sol=scipy.optimize.root(overlap_eq, x0=init, method="lm", args=(pattern, c,p*(1-p),R,b))
    overlap=sol.x
    cor=calc_cor(overlap,pattern,P,R,c,p,b)

    return (overlap,cor)

