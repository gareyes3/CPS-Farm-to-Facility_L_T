# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 15:05:52 2021

@author: gareyes3
"""

import pandas as pd 
import numpy as np
import itertools
import scipy.stats as stats
import math
import os
import random
import seaborn as sns
from matplotlib import pyplot as plt
import Funz
import ContScen
import Listz 
import OutFunz
import InFunz
import ScenCondz
import Inputz

from importlib import reload  



#%% #Graphics.

 
ProgMelted = pd.concat(Progression_DFS) 

Progplot =sns.catplot(x="variable", y="value", data=ProgMelted ,kind="bar",capsize=.2, hue = "Scenario", height=4, aspect=3 )
plt.xlabel("Process Step")
plt.ylabel("CFU in System")
plt.xticks(rotation=-75)


#Scenarios For main sampling strategies: 
    
#Boxplot Contamination Accepted CFU
data_scenarios = {'Baseline':  BL_df_outputs["Total_CFU_A"],
                'PHS':  PHS_df_outputs["Total_CFU_A"],
                'HS':  HS_df_outputs["Total_CFU_A"],
                'RS':  RS_df_outputs["Total_CFU_A"],
                'FP':  FP_df_outputs["Total_CFU_A"],
          }

df_data_scenarios = pd.DataFrame(data_scenarios)
df_data_scenarios_melted = pd.melt(df_data_scenarios)
Scenariosplot =sns.catplot(x="variable", y="value", data=df_data_scenarios_melted ,kind="bar",capsize=.2,  height=4, aspect=2 )
plt.xlabel("Process Step")
plt.ylabel("CFU Accepted in Final Product")

sum(df_data_scenarios.FP)
sum(df_data_scenarios.Baseline)


#Boxplot Contamination Accepted all Scenarios
data_scenarios_PH = {'Baseline':  BL_df_outputs["Total_CFU_A"],
                'PHS4d':  PH4d_df_outputs["Total_CFU_A"],
                'PHS 4h':  PH4h_df_outputs["Total_CFU_A"],
                'PHS Intense':  PHIN_df_outputs["Total_CFU_A"],
          }

df_data_scenarios_PH = pd.DataFrame(data_scenarios_PH)
df_data_scenarios_PH_melted = pd.melt(df_data_scenarios_PH)
Scenariosplot =sns.catplot(x="variable", y="value", data=df_data_scenarios_PH_melted ,kind="bar",capsize=.2,  height=4, aspect=2 )
plt.xlabel("Sampling Strategy")
plt.ylabel("CFU Accepted in Final Product")




#Pre-Harvest: Comparison 
#Boxplot Contamination Accepted all Scenarios
data_scenarios_PH_AR = {'PHS4d':   Out_PH4d_PercRej,
                'PHS 4h':   Out_PH4h_PercRej,
                'PHS Intense':  Out_PHIN_PercRej,
          }

df_data_scenarios_PH_AR = pd.DataFrame(data_scenarios_PH_AR)
df_data_scenarios_PH_AR_melted = pd.melt(df_data_scenarios_PH_AR)
Scenariosplot =sns.catplot(x="variable", y="value", data=df_data_scenarios_PH_AR_melted ,kind="bar",capsize=.2,  height=4, aspect=2 )
plt.xlabel("Sampling Strategy")
plt.ylabel("Percentage of CFU Rejected")

sum(df_data_scenarios.FP)
sum(df_data_scenarios.Baseline)




#HArvest Sampling Comparison Traditional vs Aggregative

    #Pre-Harvest: PErcentage Accepted Rejected
#Boxplot Contamination Accepted all Scenarios
data_scenarios_H_AR = {
                ' Traditional':   Out_HTr_PercRej,
                ' Aggregative':  Out_HAgg_PercRej,
          }

df_data_scenarios_H_AR = pd.DataFrame(data_scenarios_H_AR)
df_data_scenarios_H_AR_melted = pd.melt(df_data_scenarios_H_AR)
Scenariosplot =sns.catplot(x="variable", y="value", data=df_data_scenarios_H_AR_melted ,kind="bar",capsize=.2,  height=4, aspect=2 )
plt.xlabel("Sampling Strategy")
plt.ylabel("Percentage of CFU Rejected")



#Final Product Sampling Comparison
    #Pre-Harvest: PErcentage Accepted Rejected
#Boxplot Contamination Accepted all Scenarios
data_scenarios_PH_AR = {
                ' Traditional':   Out_FPTr_PercRej,
                ' Aggregative':  Out_FPAgg_PercRej,
          }

df_data_scenarios_PH_AR = pd.DataFrame(data_scenarios_PH_AR)
df_data_scenarios_PH_AR_melted = pd.melt(df_data_scenarios_PH_AR)
Scenariosplot =sns.catplot(x="variable", y="value", data=df_data_scenarios_PH_AR_melted ,kind="bar",capsize=.2,  height=4, aspect=2 )
plt.xlabel("Sampling Strategy")
plt.ylabel("Percentage of CFU Rejected")




# noqa

#Compare Contamination Levels and Percentage of CFU Rejected. 