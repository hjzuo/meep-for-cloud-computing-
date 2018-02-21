#!/bin/bash
    
mpb strip-wvg.ctl > strip-wvg-bands.out;

grep freqs: strip-wvg-bands.out |cut -d , -f3,7- |sed 1d > strip-wvg-bands.dat;

h5topng -o wvg_power.png -x 0 -d x.r -vZc bluered -C strip-wvg-epsilon.h5 strip-wvg-flux.v.k01.b01.x.yodd.h5;
