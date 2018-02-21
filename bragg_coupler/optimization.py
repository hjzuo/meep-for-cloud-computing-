# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 17:42:57 2018

@author: Haijie Zuo
"""

from numpy import *
from string import *
from subprocess import call

def compute_fieldintensity(p, grad):

    a=p[0];
    dfrac=p[1];
    d=a*dfrac;
    np=8;
    rot_theta=20;

    exec_str = "mpirun -np %d meep a=%0.2f d=%0.2f rot-theta=%d bragg_outcoupler.ctl > bragg-optimize-a%0.2f-d%0.2f.out" % (np,a,d,rot_theta,a,d);
    call(exec_str, shell="True");
    grep_str = "grep farfield: bragg-optimize-a%0.2f-d%0.2f.out |cut -d , -f3- > bragg-optimize-a%0.2f-d%0.2f.dat" % (a,d,a,d);
    call(grep_str, shell="True");
    mydata = genfromtxt("bragg-optimize-a%0.2f-d%0.2f.dat" % (a,d), delimiter=",", dtype='str');
    mydata = char.replace(mydata,'i','j').astype(complex128);
    Ex=mydata[:,1]; Ey=mydata[:,2]; Ez=mydata[:,3];
    Hx=mydata[:,4]; Hy=mydata[:,5]; Hz=mydata[:,6];
    Ex=conj(Ex); Ey=conj(Ey); Ez=conj(Ez);
    Px=real(multiply(Ey,Hz)-multiply(Ez,Hy));
    Py=real(multiply(Ez,Hx)-multiply(Ex,Hz));
    Pz=real(multiply(Ex,Hy)-multiply(Ey,Hx));
    Pr=sqrt(square(Px)+square(Py));
    Pnorm = Pr/max(Pr);
    ang_min = 70;
    ang_max = 80;
    ang_min = ang_min*pi/180;
    ang_max = ang_max*pi/180;
    idx = where((mydata[:,0] > ang_min) & (mydata[:,0] < ang_max));
    val = sum(Pnorm[idx])/sum(Pnorm);
    print ("intensity:, %0.2f, %0.2f, %0.6f" % (a,d,val))

    return val;



