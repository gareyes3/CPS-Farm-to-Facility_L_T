# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 13:15:08 2022

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

import Funz
import T_Inputz
import InFunz
import ContScen
import Dictionariez_T



#%%

Inputz_T.Iteration_Number = 500
Scen_T.Tomatoes_per_sample = 1
reload(DepInputz)
Outs_S1_A = MainModel.Main_Loop()

Inputz_T.Iteration_Number = 500
Scen_T.Tomatoes_per_sample = 5
reload(DepInputz)
Outs_S1_B = MainModel.Main_Loop()

Inputz_T.Iteration_Number = 500
Scen_T.Tomatoes_per_sample = 100
reload(DepInputz)
Outs_S1_C = MainModel.Main_Loop()

#HS

Inputz_T.Iteration_Number = 500
Scen_T.Tomatoes_per_sample = 1
Scen_T.Samp_Plan = 2
reload(DepInputz)
Outs_S2_A = MainModel.Main_Loop()


Inputz_T.Iteration_Number = 500
Scen_T.Tomatoes_per_sample = 5
Scen_T.Samp_Plan = 2
reload(DepInputz)
Outs_S2_B = MainModel.Main_Loop()

Inputz_T.Iteration_Number = 500
Scen_T.Tomatoes_per_sample = 100
Scen_T.Samp_Plan = 2
reload(DepInputz)
Outs_S2_C = MainModel.Main_Loop()

#RS

Inputz_T.Iteration_Number = 500
Scen_T.Tomatoes_per_sample = 1
Scen_T.Samp_Plan = 3
reload(DepInputz)
Outs_S3_A = MainModel.Main_Loop()


Inputz_T.Iteration_Number = 500
Scen_T.Tomatoes_per_sample = 5
Scen_T.Samp_Plan = 3
reload(DepInputz)
Outs_S3_B = MainModel.Main_Loop()

Inputz_T.Iteration_Number = 500
Scen_T.Tomatoes_per_sample = 100
Scen_T.Samp_Plan = 3
reload(DepInputz)
Outs_S3_C = MainModel.Main_Loop()

#%%
#Saving Dfs
S1_A_MainOut = Outs_S1_A[0]
S1_B_MainOut = Outs_S1_B[0]
S1_C_MainOut = Outs_S1_C[0]

S2_A_MainOut = Outs_S2_A[0]
S2_B_MainOut = Outs_S2_B[0]
S2_C_MainOut = Outs_S2_C[0]



#Analysis
def Get_Power(df, Weight_After, Weight_Before, CFU_avail): 
    Total_Rej = sum((df[Weight_After]-df[Weight_Before])>0 )
    Total_Avail = (sum(df[ CFU_avail]>0))
    Power =  sum((df[Weight_After]-df[Weight_Before])>0 )/ (sum(df[ CFU_avail]>0))
    return [Total_Rej,Total_Avail,Power]

#Getting contmaination at sampling points ======================================
df_locations = pd.DataFrame({
    "Pick 1": S1_A_MainOut["CFU_Bef_Pick1PHS"],
    "Pick 2": S1_A_MainOut["CFU_Bef_Pick2PHS"],
    "Pick 3": S1_A_MainOut["CFU_Bef_Pick3PHS"],
    })

df_locations_melted=df_locations.melt()

p=sns.boxplot(data = df_locations_melted, 
            x = "variable",
            y = "value"
            )
p.set_xlabel("PHS per Pick")
p.set_ylabel("TAC available at sampling point")

df_powers = pd.DataFrame({
    "PHS Pick 1":[ 0.02894736842105263],
    "PHS Pick 2": [0.065439672801636],
    "PHS Pick 3": [0.07439824945295405],
    })

df_power_melted = df_powers.melt()


sns.barplot(data = df_power_melted, 
            x = "variable",
            y = "value")


#=================================

sns.boxplot(y=S1_A_MainOut["CFU_Bef_Pick3PHS"] ) 


Total_Exposure = sum(S1_A_MainOut["Total CFU"])

def get_powers_scenarios (df):
    A=Get_Power(df = df, 
              Weight_After = "PHS 1 Weight Rejected Aft", 
              Weight_Before = "PHS 1 Weight Rejected Bef", 
              CFU_avail = "CFU_Avail Pick 1"
              )

    B=Get_Power(df = df, 
              Weight_After = "PHS 2 Weight Rejected Aft", 
              Weight_Before = "PHS 2 Weight Rejected Bef", 
              CFU_avail = "CFU_Avail Pick 2"
              )

    C= Get_Power(df = df, 
              Weight_After = "PHS 3 Weight Rejected Aft", 
              Weight_Before = "PHS 3 Weight Rejected Bef", 
              CFU_avail = "CFU_Avail Pick 3"
              )
    return [A,B,C]

    

#Power For Scenario 1

get_powers_scenarios (df=S1_A_MainOut)[0][2]

#Power For Scenario 2
get_powers_scenarios (df=S1_B_MainOut)

#Power For Scenario 3
get_powers_scenarios (df=S1_C_MainOut)

#Power For Scenario 4

get_powers_scenarios (df=S2_A_MainOut)

#Power For Scenario 5
get_powers_scenarios (df=S2_B_MainOut)

#Power For Scenario 6
get_powers_scenarios (df=S2_C_MainOut)


Powers_Summary_DF = pd

#%%
##Contamination at sampling points

def Get_Contam_Sampling(df, Type):
    S1_A_MainOut
