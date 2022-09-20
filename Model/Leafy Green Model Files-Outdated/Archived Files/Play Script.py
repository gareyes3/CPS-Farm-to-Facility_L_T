# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 09:05:11 2021

@author: Gustavo Reyes
"""

def F_Growth_K(Temperature, TimeD ):
    b=0.0616
    T0= 2.628
    if (Temperature-T0) <0:
        TDif = 0
    else:
        TDif = Temperature-T0
    Growth1D = (b*TDif)**2
    TotalGrowth = Growth1D*TimeD #Change Log CFU
    return TotalGrowth


F_Growth_K(Temperature =5, TimeD = 63/24)
