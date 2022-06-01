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
import ContScen

#%%

#Creating the initial dataframe for this harvest. 
i=1

#Intiializing dataframe that tracks the contmaination that may remain in the plant
field_cont = InFunz.F_InFieldCont_T(Partition_Units =T_Inputz.Partition_Units ,Field_Weight =T_Inputz.Pick_Weight) 

#Initializing dataframe of actual contamination. 
df= InFunz.F_InDF_T(Partition_Units = T_Inputz.Partition_Units,
                  Field_Weight = T_Inputz.Pick_Weight,
                  Pick_No = i)

#Contaminating Field/ Field Dataframe. 

ContScen.F_systematic_C(df = df, 
               Hazard_lvl = 100000,
               No_Cont_Clusters = 1,
               Cluster_Size = 32.022, 
               Partition_Weight = 32.022)

df["Harvester"] = Funz.F_Assign_Harvesters(df = df, n_harvesters = T_Inputz.N_Harvesters)
