# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 08:50:33 2022

@author: Gustavo Reyes
"""

#Second Tomato Analysis

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
def Get_Power(df, Weight_After, Weight_Before, CFU_avail, Tot_Iter): 
    Total_Rej = sum((df[Weight_After]-df[Weight_Before])>0 )
    Total_Avail = (sum(df[ CFU_avail]>0))
    Power =  sum((df[Weight_After]-df[Weight_Before])>0 )/ Tot_Iter
    return [Total_Rej,Total_Avail,Power]


def get_powers_scenarios (df, Tot_Iter):
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

def Power_DF_Creation(Column_Names, Niterations):
    Outputs_Df =pd.DataFrame(np.NaN, index= range(Niterations), columns =Column_Names)
    return Outputs_Df

def Get_Contam_Sampling(df, Type, Mass, Spread):
    A=pd.DataFrame({"Cont":df["CFU_Avail Pick 1"],
                  "Pick": 1,
                  "Type" : Type,
                  "Mass": Mass,
                  "Cont Type": Spread
                  })
    B=pd.DataFrame({"Cont":df["CFU_Avail Pick 2"],
                  "Pick": 2,
                  "Type" : Type,
                  "Mass": Mass,
                  "Cont Type": Spread
                  })
    C=pd.DataFrame({"Cont":df["CFU_Avail Pick 3"],
                  "Pick": 3,
                  "Type" : Type,
                  "Mass": Mass,
                  "Cont Type": Spread
                  })
    Dfout = pd.concat([A,B,C])
    return (Dfout)

#%%
#%% Contamination progression thruhgout system No Sampling
Hazard_Iterations = 10

Powers_df = Power_DF_Creation(Column_Names = ["Power_Pick_1", "Power_Pick_2", "Power_Pick_3"],
                              Niterations = Hazard_Iterations )
Progression_df = Dictionariez_T.Output_DF_Creation(Column_Names =Dictionariez_T.Col_Days, 
                                                   Niterations = 0)
Progression_df["HI"] = np.nan

Samp_Point_df = Power_DF_Creation(Column_Names = ["Cont", "Pick", "Type", "Mass", "Cont Type", "HI"],
                              Niterations = 0)
for i in range(Hazard_Iterations):
    Random_Haz = int(rng.normal(132_000,20_000))
    Inputz_T.Iteration_Number = 10
    Inputz_T.Total_Hazard= Random_Haz
    Scen_T.Tomatoes_per_sample = 1
    Scen_T.Samp_Plan = 1
    Scen_T.Cont_Scenario = 1
    reload(DepInputz)
    Outs = MainModel.Main_Loop()
    #powers
    Powers_df.at[i,"Power_Pick_1"]=get_powers_scenarios(Outs[0],Tot_Iter = Inputz_T.Iteration_Number)[0][2]
    Powers_df.at[i,"Power_Pick_2"]=get_powers_scenarios(Outs[0],Tot_Iter = Inputz_T.Iteration_Number)[1][2]
    Powers_df.at[i,"Power_Pick_3"]=get_powers_scenarios(Outs[0],Tot_Iter = Inputz_T.Iteration_Number)[2][2]
    
    #progression
    Progression_Temp = Outs[1]
    Progression_Temp["HI"] = Random_Haz 
    Progression_df=pd.concat([Progression_df,Progression_Temp]) 
    
    #
    Samp_Point = Get_Contam_Sampling(df = Outs[0], Type = "PH",Mass = "1 Tomato", Spread= "Uniform")
    Samp_Point["HI"] = Random_Haz
    Samp_Point_df = pd.concat([Samp_Point_df,Samp_Point])
    

    
    
    
    



