#!/usr/bin/env python3

import numpy

beta=5.0

def f(x):
    return 1.0/(1.0+numpy.exp(-beta*x))

time_pitch=0.1 #ms
sim_time=int(150.0*1000.0/time_pitch)
stim_start=int(100.0*1000.0/time_pitch)
plot_ratio=int(5.0/time_pitch)

N=50

theta=-0.2
p_targ=f(theta)
tau=5.0 #ms

WE=2*numpy.eye(N)+numpy.eye(N,k=1)+numpy.eye(N,k=-1)
WE[0,-1]=1.0
WE[-1,0]=1.0
WEIglobal=numpy.zeros(N)
WEIglobal_grad=numpy.zeros_like(WEIglobal)
WEIlocal=numpy.zeros(N)
WEIlocal_grad=numpy.zeros_like(WEIlocal)

S=numpy.random.rand(N)
X=S+0.0
XIglobal=0.0
XIlocal=numpy.zeros(N)
ext_input=numpy.zeros(N)
stimpos=int(N//2)
overlap=numpy.zeros([int(sim_time//plot_ratio), N])
Achhist=numpy.zeros(int(sim_time//plot_ratio))
plot_time=numpy.zeros(int(sim_time//plot_ratio))
stim_hist=numpy.zeros(int(sim_time//plot_ratio))
WEIglobal_hist=numpy.zeros(int(sim_time//plot_ratio))
WEIlocal_hist=numpy.zeros(int(sim_time//plot_ratio))
n_plot=0

#simulation
for t in range(sim_time):
    time_ms=t*time_pitch
    if (t-1)%10000==0:
        print(t-1, Ach, numpy.mean(X), numpy.mean(WEIglobal), numpy.mean(WEIlocal))
    if t>stim_start:
        eta=0.0
        stim_width=500.0
        ext_input=numpy.zeros(N)
        ext_input[stimpos]=0.5*((time_ms%stim_width)/stim_width<0.2)
        if time_ms%stim_width==0:
            stimpos=numpy.random.randint(N-20)+10
        Ach_width=10000.0 #ms
        Ach=0.5+0.4*numpy.sin(2*numpy.pi*time_ms/Ach_width)
    else:
        eta=1e-3
        Ach_width=10000.0 #ms
        Ach=0.9

    X+=time_pitch*(-X+S)/tau
    XIglobal=(1.0-Ach)*numpy.sum(X)
    XIlocal=Ach*X
    h=WE@X-WEIglobal*XIglobal-WEIlocal*XIlocal
    S=f(h+ext_input+theta)

    WEIglobal+=(time_pitch*eta*(S-p_targ))*XIglobal
    WEIglobal[WEIglobal<0.0]=0.0

    WEIlocal+=(time_pitch*eta*(S-p_targ))*XIlocal
    WEIlocal[WEIlocal<0.0]=0.0

    if int(t%plot_ratio)==0:
        n_plot=int(t//plot_ratio)
        stim_hist[n_plot]=(ext_input[stimpos]>0)*(stimpos+1)-1
        plot_time[n_plot]=time_ms/1000.0
        overlap[n_plot,:]=X
        Achhist[n_plot]=Ach
        WEIglobal_hist[n_plot]=numpy.mean(WEIglobal)
        WEIlocal_hist[n_plot]=numpy.mean(WEIlocal)

numpy.savetxt("time_sec.csv", plot_time, delimiter=",")
numpy.savetxt("overlap.csv", overlap, delimiter=",")
numpy.savetxt("Ach.csv", Achhist, delimiter=",")
numpy.savetxt("stimpos.csv", stim_hist, delimiter=",")
numpy.savetxt("wlocal.csv", WEIlocal_hist, delimiter=",")
numpy.savetxt("wglobal.csv", WEIglobal_hist, delimiter=",")

