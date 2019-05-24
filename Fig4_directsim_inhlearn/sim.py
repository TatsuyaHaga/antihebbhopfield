#!/usr/bin/env python3

import numpy

def f(x):
    return (x>0)+0.0

time_pitch=0.5 #ms
sim_time=int(140.0*1000.0/time_pitch)
time_plasticityOFF=100.0 #sec
time_weightperturb=120.0
plot_pitch=10 #sample

N=2000
P=50

p=0.05
tau=5.0 #ms
wdecay=1e-6
h0G=5e-3

perturb_ratio=0.5

pattern=(numpy.random.rand(P,N)<p).astype(numpy.float)
pattern_mean=numpy.sum(pattern,axis=0)/P
pattern_plus=numpy.roll(pattern, 1, axis=0)
WE=(2*(pattern.T)@(pattern)+(pattern_plus.T)@(pattern)+(pattern.T)@(pattern_plus))/N
WE[numpy.eye(N, dtype=numpy.bool)]=0.0

WIEglobal=(pattern_mean)/N
WEIglobal=numpy.zeros(N)
WEIglobal_prev=numpy.zeros_like(WEIglobal)

WIElocal=pattern/N
WEIlocal=numpy.zeros([N,P])
WEIlocal_prev=numpy.zeros_like(WEIlocal)
WEIlocal_filter=pattern.T

S=(numpy.random.rand(N)<p).astype(float)
X=S+0.0
XIglobal=0.0
XIlocal=numpy.zeros(P)
ext_input=0.0
input_amp=0.0
stimpos=numpy.random.randint(P)
plotlen=int(sim_time/plot_pitch)
overlap=numpy.zeros([plotlen, P])
plot_time=numpy.zeros(plotlen)
Wlog=numpy.zeros([plotlen,2])
AChhist=numpy.zeros(plotlen)
stimhist=numpy.zeros(plotlen)
perturb=True

for t in range(sim_time):
    time_ms=(t+1)*time_pitch
    time_sec=time_ms/1000.0
    if time_ms%1000==0:
        print(time_sec, numpy.mean(S), numpy.mean(WEIglobal), numpy.mean(WEIlocal))

    if time_sec>time_plasticityOFF:
        if time_sec>time_weightperturb and perturb:
            numpy.savetxt("WEIglobal_converge.csv", WEIglobal, delimiter=",")
            numpy.savetxt("WEIlocal_converge.csv", WEIlocal, delimiter=",")
            WEIglobal=WEIglobal*(1.0+perturb_ratio*(2*numpy.random.rand(N)-1))
            WEIlocal=WEIlocal*(1.0+perturb_ratio*(2*numpy.random.rand(N,P)-1))
            numpy.savetxt("WEIglobal_perturb.csv", WEIglobal, delimiter=",")
            numpy.savetxt("WEIlocal_perturb.csv", WEIlocal, delimiter=",")
            perturb=False
        eta=0.0
        Ach_width=5000.0 #ms
        ACh=0.5+0.4*numpy.sin(2*numpy.pi*time_ms/Ach_width)
        stim_interval=500.0
        stim_width=100.0
        if input_amp>0 and (time_ms%stim_interval)>stim_width:
            input_amp=0.0
            ext_input=0.0
            stimpos=-1
        elif time_ms%stim_interval==0:
            input_amp=0.02
            stimpos=numpy.random.randint(P-20)+10 
            ext_input=input_amp*pattern[stimpos,:]
    else:
        eta=0.05
        ACh=0.9
        input_amp=0.02
        ext_src=numpy.random.rand(N)<1e-3*time_pitch
        ext_input+=input_amp*ext_src-time_pitch*ext_input/5.0

    X+=time_pitch*(-X+S)/tau
    XIglobal=(1-ACh)*WIEglobal@X
    XIlocal=ACh*WIElocal@X
    h=WE@X-P*WEIglobal*XIglobal-WEIlocal@XIlocal+ext_input-numpy.mean(ext_input)
    S=f(h)
    
    WEIglobal+=time_pitch*eta*((h+h0G)*XIglobal-wdecay*WEIglobal)
    WEIglobal[WEIglobal<0.0]=0.0

    WEIlocal+=time_pitch*eta*(numpy.outer(h,XIlocal)-wdecay*WEIlocal)
    WEIlocal[WEIlocal<0.0]=0.0
    WEIlocal*=WEIlocal_filter

    if t%plot_pitch==0:
        t_plot=int(t/plot_pitch)
        plot_time[t_plot]=time_ms/1000.0
        overlap[t_plot,:]=((pattern-p)@X)/(N*p*(1.0-p))
        AChhist[t_plot]=ACh
        stimhist[t_plot]=stimpos
        Wlog[t_plot,0]=numpy.max(numpy.abs(WEIglobal-WEIglobal_prev))
        Wlog[t_plot,1]=numpy.max(numpy.abs(WEIlocal-WEIlocal_prev))
        WEIglobal_prev=WEIglobal+0.0
        WEIlocal_prev=WEIlocal+0.0

numpy.savetxt("overlap.csv", overlap, delimiter=",")
numpy.savetxt("time_sec.csv", plot_time, delimiter=",")
numpy.savetxt("wlocal.csv", Wlog[:,1], delimiter=",")
numpy.savetxt("wglobal.csv", Wlog[:,0], delimiter=",")
numpy.savetxt("Ach.csv", AChhist, delimiter=",")
numpy.savetxt("stim.csv", stimhist, delimiter=",")

