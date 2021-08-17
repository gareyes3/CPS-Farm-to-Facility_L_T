# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 09:26:18 2021

@author: gareyes3
"""


#%%
import sys
sys.path
#sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model')
sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility\Model')

#%% Libraries
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

#Main Model Loops
import MainModel3z

#%% 
#Progression DataFrame. 
Progression_DFS = []
#%% BAseline Sampling: 
#Contamination Challenges
ScenCondz.Background_C=1
ScenCondz.Point_Source_C=0
ScenCondz.Systematic_C=0

#Harvester Contamination
ScenCondz.Crew_C = 0
ScenCondz.Harvester_C = 0

#Processing equipment
ScenCondz.PE_C = 0
ScenCondz.PE_Cont_Loc = 0,#2,3,4,5
#1 = Shredder, #2 = Belt, #3 = Washing, #4 Shaker, #5Centrifuge
ScenCondz.Pack_C= 0

#%% Baseline Sampling
reload(ScenCondz)
#Sampling Conditions, Baseline all conditions are off
ScenCondz.Baseline_Sampling= 1 #all others must be 0if this one is 1
ScenCondz.PH_Sampling = 0
ScenCondz.H_Sampling = 0
ScenCondz.R_Sampling = 0
ScenCondz.FP_Sampling = 0

reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_Baseline = Main_Mod_Outs[1]
DProg_Baseline=Main_Mod_Outs[0]

#%%

#%% Pre-Harvest
#Sampling Conditions, Baseline all conditions are off
ScenCondz.Baseline_Sampling= 0 #all others must be 0if this one is 1
ScenCondz.PH_Sampling = 1
ScenCondz.H_Sampling = 0
ScenCondz.R_Sampling = 0
ScenCondz.FP_Sampling = 0

    #Pre_Harvest 4 Days
#Pre-Harvest


ScenCondz.PHS_4d= 1#Scenario 1
ScenCondz.PHS_4h = 0#Scenario 2
ScenCondz.PHS_Int = 0 #Scenario 3

reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists

Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PH4d = Main_Mod_Outs[1]
DProg_PH4d=Main_Mod_Outs[0]

    #Pre_Harvest 4 hr
#Pre-Harvest

ScenCondz.PHS_4d= 0#Scenario 1
ScenCondz.PHS_4h = 1#Scenario 2
ScenCondz.PHS_Int = 0 #Scenario 3

reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists

Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PH4h = Main_Mod_Outs[1]
DProg_PH4h=Main_Mod_Outs[0]

    #Pre_Harvest Int
#Pre-Harvest


ScenCondz.PHS_4d= 0#Scenario 1
ScenCondz.PHS_4h = 0#Scenario 2
ScenCondz.PHS_Int = 1 #Scenario 3

reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists

Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PHInt = Main_Mod_Outs[1]
DProg_PHInt=Main_Mod_Outs[0]


#%% Harvest

#Sampling Conditions, Baseline all conditions are off
ScenCondz.Baseline_Sampling= 0 #all others must be 0if this one is 1
ScenCondz.PH_Sampling = 0
ScenCondz.H_Sampling = 1
ScenCondz.R_Sampling = 0
ScenCondz.FP_Sampling = 0

#Harvest Traditional



ScenCondz.HS_Trad = 1 #Scenario 5
ScenCondz.HS_Agg = 0#Scenario 6

reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists

Main_Mod_Outs=MainModel3z.F_MainLoop()
D_HTrad = Main_Mod_Outs[1]
DProg_HTrad=Main_Mod_Outs[0]

#Harvest Aggregative
ScenCondz.HS_Trad = 0 #Scenario 5
ScenCondz.HS_Agg = 1 #Scenario 6

reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists

Main_Mod_Outs=MainModel3z.F_MainLoop()
D_HAgg = Main_Mod_Outs[1]
DProg_HAgg=Main_Mod_Outs[0]

#%% Receiving
reload(ScenCondz)
#Sampling Conditions, Baseline all conditions are off
ScenCondz.Baseline_Sampling= 0 #all others must be 0if this one is 1
ScenCondz.PH_Sampling = 0
ScenCondz.H_Sampling = 0
ScenCondz.R_Sampling = 1
ScenCondz.FP_Sampling = 0

#Harvest Traditional
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists

Main_Mod_Outs=MainModel3z.F_MainLoop()
D_R = Main_Mod_Outs[1]
DProg_R=Main_Mod_Outs[0]

#%% Final Product
reload(ScenCondz)
#Sampling Conditions, Baseline all conditions are off
ScenCondz.Baseline_Sampling= 0 #all others must be 0if this one is 1
ScenCondz.PH_Sampling = 0
ScenCondz.H_Sampling = 0
ScenCondz.R_Sampling = 0
ScenCondz.FP_Sampling = 1

#Harvest Traditional

ScenCondz.FPS_Trad = 1 #Scenario 5
ScenCondz.FPS_Agg = 0 #Scenario 6

reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists

Main_Mod_Outs=MainModel3z.F_MainLoop()
D_FPSTrad = Main_Mod_Outs[1]
DProg_FPSTrad=Main_Mod_Outs[0]

#Harvest Aggregative

ScenCondz.FPS_Trad = 0 #Scenario 5
ScenCondz.FPS_Agg = 1 #Scenario 6

reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists

Main_Mod_Outs=MainModel3z.F_MainLoop()
D_FPSAgg = Main_Mod_Outs[1]
DProg_FPSAgg=Main_Mod_Outs[0]

#%%Final graphs

L_Final_Conts = {
                'Baseline':D_Baseline["Total_CFU_A"],
                'PH4d':D_PH4d["Total_CFU_A"],
                'PH4h':D_PH4h["Total_CFU_A"],
                'PHInt':D_PHInt["Total_CFU_A"],
                'HTrad':D_HTrad["Total_CFU_A"],
                'HAgg':D_HAgg["Total_CFU_A"],
                'R':D_R["Total_CFU_A"],
                'FPTrad':D_FPSTrad["Total_CFU_A"],
                'FPAgg':D_FPSAgg["Total_CFU_A"],
          }

df_L_Final_Conts = pd.DataFrame(L_Final_Conts)
df_L_Final_Conts_melted = pd.melt(df_L_Final_Conts)


#Scenariosplot =sns.catplot(x="variable", y="value", data=df_L_Final_Conts_melted ,kind="bar",  height=4, aspect=2 )
Scenariosplot =sns.boxplot(x="variable", y="value", data=df_L_Final_Conts_melted )
plt.xlabel("Sampling Type")
plt.ylabel("Total CFU in Final Product")



L_Final_Per = {
                'PH4d':D_PH4d["PerRejected at PH"],
                'PH4h':D_PH4h["PerRejected at PH"],
                'PHInt':D_PHInt["PerRejected at PH"],
                'HTrad':D_HTrad["PerRejected at H"],
                'HAgg':D_HAgg["PerRejected at H"],
                'R':D_R["PerRejected at R"],
                'FPTrad':D_FPSTrad["PerRejected at FP"],
                'FPAgg':D_FPSAgg["PerRejected at FP"],
          }

df_L_Final_Per = pd.DataFrame(L_Final_Per)
df_L_Final_Per_melted = pd.melt(df_L_Final_Per)


#Scenariosplot =sns.catplot(x="variable", y="value", data=df_L_Final_Per_melted ,kind="bar",  height=4, aspect=2 )
Scenariosplot =sns.boxplot(x="variable", y="value", data=df_L_Final_Per_melted )
plt.xlabel("Sampling Type")
plt.ylabel("Percentage CFU Rejected at Sampling Step")
