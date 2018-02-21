# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 14:17:07 2018

@author: Haijie Zuo
"""

import meep as mp
cell = mp.Vector3(16, 8, 0)

geometry = [mp.Block(mp.Vector3(1e20, 1, 1e20),
                     center=mp.Vector3(0, 0),
                     material=mp.Medium(epsilon=12))]

sources = [mp.Source(mp.ContinuousSource(frequency=0.15),
                     component=mp.Ez,
                     center=mp.Vector3(-7,0))]
pml_layers = [mp.PML(1.0)]

resolution = 10

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

sim.run(mp.at_beginning(mp.output_epsilon),
        mp.at_end(mp.output_efield_z),
        until=200)

import h5py
import numpy as np
import matplotlib.pyplot as plt


eps_h5file = h5py.File('eps-000000.00.h5','r')
eps_data = np.array(eps_h5file['eps'])
plt.figure(dpi=100)
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.axis('off')
plt.show()

ez_h5file = h5py.File('ez-000200.00.h5','r')
ez_data = np.array(ez_h5file['ez'])
plt.figure(dpi=100)
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
plt.axis('off')
plt.show()