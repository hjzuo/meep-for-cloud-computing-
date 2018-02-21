# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 15:59:25 2018

@author: Haijie Zuo
"""

import nlopt
import random
from compute_fieldintensity import *

# lattice parameter (um)
a_min = 0.50;
a_max = 3.00;

# waveguide width (fraction of lattice parameter)
dfrac_min = 0.2;
dfrac_max = 0.8;

opt = nlopt.opt(nlopt.LN_BOBYQA, 2)
opt.set_max_objective(compute_fieldintensity)
opt.set_lower_bounds([ a_min, dfrac_min ])
opt.set_upper_bounds([ a_max, dfrac_max ])
opt.set_ftol_abs(0.005)
opt.set_xtol_abs(0.02)
opt.set_initial_step(0.04)
opt.max_eval = 50

# random initial parameters
a_0 = a_min + (a_max-a_min)*random.random();
dfrac_0 = dfrac_min + (dfrac_max-dfrac_min)*random.random();

x = opt.optimize([a_0, dfrac_0])
maxf = opt.last_optimum_value()
print("optimum at a={} um, d={} um".format(x[0],x[0]*x[1]))
print("maximum value = {}".format(maxf))
print("result code = {}".format(opt.last_optimize_result()))