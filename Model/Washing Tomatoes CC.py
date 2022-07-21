# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 12:37:55 2022

@author: gareyes3
"""
import numpy as np
#Washing FC 
FC_lvl = np.random.triangular(0,80,250)
if FC_lvl<10:
    log_red_Wash_mean = FC_lvl*0.04+0.3
elif FC_lvl>10:
    log_red_Wash_mean = FC_lvl*0.0056+0.5952
    
logred_sd = 0.175

#Transfer to uncontaminated pieces. 
Log_Trans_Upper = -0.6798*FC_lvl-0.6
Log_Trans_Lower = -1.3596*FC_lvl-0.6

np.random.uniform(Log_Trans_Lower,Log_Trans_Upper)



    
