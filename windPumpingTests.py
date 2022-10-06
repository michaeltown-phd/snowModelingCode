#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 16:18:50 2022

testing wind pumping code to see what happens in EastGRIP-like snow

@author: michaeltown
"""

import numpy as np
import geophysics as gp
import matplotlib.pyplot as plt
import pandas as pd

# data loc
figureLoc = '/home/michaeltown/work/projects/snowiso/figures/EastGRIP/model/windpumping/'

# make the model snow field and atmospheric conditions

duneLength = np.asarray([0.25,0.5,1.0])     # dune length
duneHeight = np.asarray([0.05,0.1,0.2])     # dune height
xCor = np.arange(0.01,0.5, 0.01)      # simulate half a wavelength
zCor = np.arange(0,0.5,0.02)         # down to one meter every 5 cm
rhoS = 350
u10 = np.asarray([2.5, 5, 10, 20])           # wind speed in m/s

# initialize and fill in dataframe for horizontal wind speeds and residence times at depth
uField = pd.DataFrame()

for ut in u10:
    for dl in duneLength:
        for dh in duneHeight:
            for xt in xCor:
            
                uField[xt], tau = gp.windpumping(h=dh, l=dl, x=xt, z=zCor, ws10m=ut, rhoSnow=rhoS, rhoAir = 1.2, mu = 1.2*10**-5, k = 22*10**-10)
            
            uField.set_index(zCor,inplace = True)
    
            fig = plt.figure();
            clrRange = np.arange(0,0.2,0.02)
            plt.contourf(xCor,-zCor,uField.values,cmap = 'Greys',levels = clrRange)
            plt.clim(0,0.2)
            cbar = plt.colorbar()
            cbar.set_ticks(clrRange)
            plt.xlabel('horizontal distance (m)')
            plt.ylabel('depth (m)')
            plt.xlim([0,0.5])
            plt.text(0.02,-0.40,'ux = ' + str(ut)+ ' m/s, dune h = ' + str(dh)+' m, dune l = '+ str(dl) + ' m')
            plt.text(0.02,-0.43,'max ux = ' + str(np.round(np.max(uField.values),2)) + ' m/s')
            fileName = 'duneSim_l'+str(dl)+'_h'+str(dh)+'_u'+str(ut)+'.jpg'
            fig.savefig(figureLoc+fileName)
            
            # mean, min, max horizontal windspeed profile
            
            uMean = uField.loc[:,uField.columns<=dl/2].mean(axis = 1)
            uMin= uField.loc[:,uField.columns<=dl/2].min(axis = 1)
            uMax= uField.loc[:,uField.columns<=dl/2].max(axis = 1)
            uStd = uField.loc[:,uField.columns<=dl/2].std(axis = 1)
            
            fig,ax = plt.subplots()
            plt.plot(uMean,-zCor,color = 'black',linewidth = 3)
            ax.fill_betweenx(-zCor,uMin,uMax,alpha = 0.5, color = 'Gray')
            ax.fill_betweenx(-zCor,uMean-uStd,uMax+uStd,alpha = 0.5, color = 'Gray')
            plt.xlabel('horizontal wind speed (m/s)')
            plt.ylabel('depth (m)')
            plt.text(0.1,-0.40,'ux = ' + str(ut)+ ' m/s, dune h = ' + str(dh)+' m, dune l = '+ str(dl) + ' m')
            plt.text(0.1,-0.43,'max ux = ' + str(np.round(np.max(uField.values),2)) + ' m/s')
            plt.xlim([0,1])
            fileName = 'duneSimProf_l'+str(dl)+'_h'+str(dh)+'_u'+str(ut)+'.jpg'
            fig.savefig(figureLoc+fileName)

            