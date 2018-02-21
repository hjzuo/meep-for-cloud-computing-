# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:23:27 2018

@author: Haijie Zuo
"""

import numpy as np

def is_float(string):
    """ True if given string is float else False"""
    try:
        return float(string)
    except ValueError:
        return False

data = []
data2 = []
i = 0
j = 0
with open('strip-wvg-bands.dat', 'r') as f:
    d = f.readlines()
    for i in d:
        print (i)
        k = i.rstrip().split(",")
        data2.append(k)
#        print (k)
#        while is_float(k[0]) != False:
#            for i in k:
#                data.append([float(i)])
            
#                for i in k:
#    #                if is_float(i):
#                        data.append([float(i)])  

data = np.array(data, dtype='O')

import matplotlib.pyplot as plt

f = open("strip-wvg-bands.dat", 'r')
#plt.plot(f[:,0],f[:,1:],'b-',f[:,0],f[:,0]/1.45,'k-');
#plt.xlabel("wavevector k_x (units of 2\pi\mum^{-1})");
#plt.ylabel("frequency (units of 2\pix30^{14} Hz)");
#plt.axis([0,2,0,1]);
#plt.show()
