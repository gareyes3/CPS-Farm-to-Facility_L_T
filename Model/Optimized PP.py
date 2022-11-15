# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 08:54:21 2022

@author: gareyes3
"""

#%%
import sys
sys.path
sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility_L_T\Model')
sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility_L_T\Model')
sys.path.append('C:\\Users\\reyes\\Documents\\GitHub\\CPS-Farm-to-Facility_L_T\Model')
#%%
import numpy as np
import pandas as pd
import random 
import math
from numpy.random import Generator, PCG64
rng = Generator(PCG64())
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import reload 

import time
#Own Libraries
import Funz_T
import Inputz_T
import Scen_T
import MainModel
import DepInputz

import T_Inputz
import Dictionariez_T

#%%

def PP_Function(Iter_p_day, Tom_Sample, Samp_Plan ):
    List_Outputs = []
    List_of_cont_day = list(range(1,43))
    for i in List_of_cont_day:
        Inputz_T.Iteration_Number = Iter_p_day
        Scen_T.Tomatoes_per_sample = Tom_Sample
        Scen_T.Samp_Plan = Samp_Plan
        Scen_T.Cont_Scenario = 1
        Scen_T.Samp_Method = 1
        Scen_T.Chosen_cont_day = 1
        Scen_T.Contamination_Day = i
        reload(DepInputz)
        Outs_S1_A = MainModel.Main_Loop()
        
        Rejected_Pick1 = Outs_S1_A[0]["CFU_Bef_Pick1PHS"] - Outs_S1_A[0]["CFU_Aft_Pick1PHS"]
        Cont_Avail_Pick1 = pd.Series(np.where(Outs_S1_A[0]["CFU_Bef_Pick1PHS"]==0, "Yes", "No"))
        
        Rejected_Pick2 = Outs_S1_A[0]["CFU_Bef_Pick2PHS"] - Outs_S1_A[0]["CFU_Aft_Pick2PHS"]
        Cont_Avail_Pick2 = pd.Series(np.where(Outs_S1_A[0]["CFU_Bef_Pick2PHS"]==0, "Yes", "No"))
        
        Rejected_Pick3 = Outs_S1_A[0]["CFU_Bef_Pick3PHS"] - Outs_S1_A[0]["CFU_Aft_Pick3PHS"]
        Cont_Avail_Pick3 = pd.Series(np.where(Outs_S1_A[0]["CFU_Bef_Pick3PHS"]==0, "Yes", "No"))
        
        Total_Exposure = Outs_S1_A[0]["Total CFU"]
        
        Prot_Power=pd.concat(
                   [Outs_S1_A[0]["CFU_Bef_Pick1PHS"],Rejected_Pick1,Cont_Avail_Pick1,
                   Outs_S1_A[0]["CFU_Bef_Pick2PHS"],Rejected_Pick2,Cont_Avail_Pick2,
                   Outs_S1_A[0]["CFU_Bef_Pick3PHS"],Rejected_Pick3,Cont_Avail_Pick3,
                   Total_Exposure,pd.Series(Outs_S1_A[5])], axis = 1)
        
        List_Outputs.append(Prot_Power)
        
    Final_DF_ProtectiveP = pd.concat(List_Outputs)