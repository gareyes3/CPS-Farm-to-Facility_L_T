# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 11:33:05 2021

@author: gareyes3
"""
#%%
import sys, os
sys.path
#sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model')
sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility\Model')

# %%
from importlib import reload
import numpy as np
import Listz
import pandas as pd
import MainModel3z
import SCInputz
import Inputz
import ContCondz
import ScenCondz
import InFunz
import OutFunz
import ContScen
import Funz
from matplotlib import pyplot as plt
from matplotlib.ticker import ScalarFormatter
import seaborn as sns
import sys
import Trial_MainLoop_PH
import math
import random
sys.path
#sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model')
sys.path.append(
    'C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility\Model')

#%%
def F_Sampling_2 (df, Test_Unit, NSamp_Unit, Samp_Size, Partition_Weight, NoGrab):
    Unique_TestUnit = list(df[Test_Unit].unique())
    Grab_Weight = Samp_Size/NoGrab
    for i in (Unique_TestUnit): #From sublot 1 to sublot n (same for pallet,lot,case etc)
        for l in range (1, NSamp_Unit+1): #Number of samples per sublot or lot or pallet.
            for j in range(NoGrab):
                CFU_array=np.array(df["CFU"])
                List_Random=random.choice(list(enumerate(CFU_array)))
                CFU = List_Random[1]
                Index = List_Random[0]
                CFU_grab = CFU*(Grab_Weight/(Partition_Weight*454))
                P_Detection=1-math.exp(-CFU_grab)
                RandomUnif = random.uniform(0,1)
                if RandomUnif < P_Detection:
                    df.at[Index, 'PositiveSamples']. append(l)
    return (df)


def F_Sampling_3 (df, Test_Unit, NSamp_Unit, Samp_Size, Partition_Weight, NoGrab):
    Unique_TestUnit = list(df[Test_Unit].unique())
    Grab_Weight = Samp_Size/NoGrab
    for i in (Unique_TestUnit): #From sublot 1 to sublot n (same for pallet,lot,case etc)
        for l in range (1, NSamp_Unit+1): #Number of samples per sublot or lot or pallet.
            for j in range(NoGrab):
                Sampled_Grab =df[df[Test_Unit] == i].sample(1, replace= True)
                Index = Sampled_Grab.index
                Index = Index[0]
                CFU = Sampled_Grab["CFU"]
                CFU_grab = CFU*(Grab_Weight/(Partition_Weight*454))
                P_Detection=1-math.exp(-CFU_grab)
                RandomUnif = random.uniform(0,1)
                if RandomUnif < P_Detection:
                    df.at[Index, 'PositiveSamples']. append(l)
    return (df)


CFU_hh=np.array(df["CFU"])
List_Random=random.choice(list(enumerate(CFU_hh)))
CFUs = List_Random[1]
Index_Main = List_Random[0]


#%%

df= InFunz.F_InDF(Partition_Units = 2000,
                  Field_Weight = 100000, 
                  slot_number = 10)

df=ContScen.F_systematic_C(df=df, 
                             Hazard_lvl=50000000,
                             No_Cont_Clusters =1, 
                             Cluster_Size = 10000, 
                             Partition_Weight = 50)




#%%

import time
start_time = time.time()

df = F_Sampling_2(df =df,Test_Unit ="Sublot", 
                          NSamp_Unit = 1, 
                          Samp_Size =300, 
                          Partition_Weight =50, 
                          NoGrab =60)

print("--- %s seconds ---" % (time.time() - start_time))

