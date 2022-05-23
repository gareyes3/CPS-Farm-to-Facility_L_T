# -*- coding: utf-8 -*-
"""
Created on Mon May 23 13:22:12 2022

@author: gareyes3
"""

#%%
import sys
sys.path
sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility_L_T\Model')
sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility_L_T\Model')

#%%
import numpy as np
import pandas as pd

#Own Libraries
import Funz
import T_Inputz
import InFunz

#%%

#Creating the initial dataframe for this harvest. 
Partition_Units = T_Inputz.Pick_Weight/T_Inputz.Bucket_Weight

df= InFunz.F_InDF_T(Partition_Units = 1093,
                  Field_Weight = 35_000, )

int(35000/32)

int(1093/11)
