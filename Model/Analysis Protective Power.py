# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 12:49:10 2022

@author: reyes
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

#%% Sampling Scenarios
 #Sampling Scenario
time_s = time.time()
Inputz_T.Iteration_Number = 100
Scen_T.Tomatoes_per_sample = 20
Scen_T.Samp_Plan = 1
Scen_T.Cont_Scenario = 1
Scen_T.Samp_Method = 1
reload(DepInputz)
Outs_S1_A = MainModel.Main_Loop()
print(time.time() - time_s, "CC")



#Goal here is to compare the overall or compare the cont day, with the exposure

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

Pick_1PP = Prot_Power[Prot_Power[1]=="No"]
Pick_1PP = (sum(Pick_1PP[0]))/sum(Pick_1PP["CFU_Bef_Pick1PHS"])

Pick_2PP = Prot_Power[Prot_Power[3]=="No"]
Pick_2PP = (sum(Pick_2PP[2]))/sum(Pick_2PP["CFU_Bef_Pick2PHS"])

Pick_3PP = Prot_Power[Prot_Power[5]=="No"]
Pick_3PP = (sum(Pick_3PP[4]))/sum(Pick_3PP["CFU_Bef_Pick3PHS"])

#%%
List_Outputs = []
List_of_cont_day = list(range(1,43))
for i in List_of_cont_day:
    Inputz_T.Iteration_Number = 5
    Scen_T.Tomatoes_per_sample = 20
    Scen_T.Samp_Plan = 1
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

Final_DF_ProtectiveP.to_csv(path_or_buf = "C:\\Users\\reyes\\Documents\\GitHub\\CPS-Farm-to-Facility_L_T\\Model\\Data_Tomato_Outputs\\PP10.csv")