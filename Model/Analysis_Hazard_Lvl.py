# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 09:41:52 2021

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
#%% Contamination Level Analysis PH 4d
reload(ScenCondz)
#50,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 50000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PH4d_50k = Main_Mod_Outs[1]
DProg_PH4d_50k=Main_Mod_Outs[0]

#10,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 10000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PH4d_10k = Main_Mod_Outs[1]
DProg_PH4d_10k=Main_Mod_Outs[0]

#5000 CFU INitial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 5000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PH4d_5k = Main_Mod_Outs[1]
DProg_PH4d_5k=Main_Mod_Outs[0]

#1000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 1000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PH4d_1k = Main_Mod_Outs[1]
DProg_PH4d_1k=Main_Mod_Outs[0]

#100 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 100
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PH4d_100 = Main_Mod_Outs[1]
DProg_PH4d_100=Main_Mod_Outs[0]
#%% Contamination Level Analysis PH 4h

ScenCondz.PHS_4d = 0
ScenCondz.PHS_4h = 1

#50,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 50000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PH4h_50k = Main_Mod_Outs[1]
DProg_PH4h_50k=Main_Mod_Outs[0]

#10,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 10000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PH4h_10k = Main_Mod_Outs[1]
DProg_PH4h_10k=Main_Mod_Outs[0]

#5000 CFU INitial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 5000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PH4h_5k = Main_Mod_Outs[1]
DProg_PH4h_5k=Main_Mod_Outs[0]

#1000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 1000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PH4h_1k = Main_Mod_Outs[1]
DProg_PH4h_1k=Main_Mod_Outs[0]

#100 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 100
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PH4h_100 = Main_Mod_Outs[1]
DProg_PH4h_100=Main_Mod_Outs[0]

#%% Contamination Level Analysis PH Intense

ScenCondz.PHS_4d = 0
ScenCondz.PHS_4h = 0
ScenCondz.PHS_Int = 1 #Scenario 3

#50,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 50000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PHInt_50k = Main_Mod_Outs[1]
DProg_PHInt_50k=Main_Mod_Outs[0]

#10,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 10000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PHInt_10k = Main_Mod_Outs[1]
DProg_PHInt_10k=Main_Mod_Outs[0]

#5000 CFU INitial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 5000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PHInt_5k = Main_Mod_Outs[1]
DProg_PHInt_5k=Main_Mod_Outs[0]

#1000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 1000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PHInt_1k = Main_Mod_Outs[1]
DProg_PHInt_1k=Main_Mod_Outs[0]

#100 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 100
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PHInt_100 = Main_Mod_Outs[1]
DProg_PHInt_100=Main_Mod_Outs[0]


#%% Graphics. 

L_PR_PH4d = {
                ' 50K':D_PH4d_50k["PerRejected at PH"],
                ' 10K':D_PH4d_10k["PerRejected at PH"],
                ' 5K':D_PH4d_5k["PerRejected at PH"],
                ' 1K':D_PH4d_1k["PerRejected at PH"],
                ' 100':D_PH4d_100["PerRejected at PH"],
          }

df_L_PR_PH4d = pd.DataFrame(L_PR_PH4d)
df_L_PR_PH4d_melted = pd.melt(df_L_PR_PH4d)
df_L_PR_PH4d_melted["Type"] = "4d"
Scenariosplot =sns.catplot(x="variable", y="value", data=df_L_PR_PH4d_melted ,kind="point",  height=4, aspect=2 )
plt.xlabel("Initial Hazard Level Total CFU")
plt.ylabel("Percentage of CFU Rejected at PHS")

L_PR_PH4h = {
                ' 50K':D_PH4h_50k["PerRejected at PH"],
                ' 10K':D_PH4h_10k["PerRejected at PH"],
                ' 5K':D_PH4h_5k["PerRejected at PH"],
                ' 1K':D_PH4h_1k["PerRejected at PH"],
                ' 100':D_PH4h_100["PerRejected at PH"],
          }

df_L_PR_PH4h = pd.DataFrame(L_PR_PH4h)
df_L_PR_PH4h_melted = pd.melt(df_L_PR_PH4h)
df_L_PR_PH4h_melted["Type"] = "4h"
Scenariosplot =sns.catplot(x="variable", y="value", data=df_L_PR_PH4h_melted ,kind="point",  height=4, aspect=2 )
plt.xlabel("Initial Hazard Level Total CFU")
plt.ylabel("Percentage of CFU Rejected at PHS")

L_PR_PHInt = {
                ' 50K':D_PHInt_50k["PerRejected at PH"],
                ' 10K':D_PHInt_10k["PerRejected at PH"],
                ' 5K':D_PHInt_5k["PerRejected at PH"],
                ' 1K':D_PHInt_1k["PerRejected at PH"],
                ' 100':D_PHInt_100["PerRejected at PH"],
          }

df_L_PR_PHInt = pd.DataFrame(L_PR_PHInt)
df_L_PR_PHInt_melted = pd.melt(df_L_PR_PHInt)
df_L_PR_PHInt_melted["Type"] = "Int"
Scenariosplot =sns.catplot(x="variable", y="value", data=df_L_PR_PHInt_melted ,kind="point",  height=4, aspect=2 )
plt.xlabel("Initial Hazard Level Total CFU")
plt.ylabel("Percentage of CFU Rejected at PHS")

CombinedData = pd.concat([df_L_PR_PH4d_melted,
                          df_L_PR_PH4h_melted,
                          df_L_PR_PHInt_melted])


Scenariosplot =sns.lineplot(x="variable", y="value", hue = "Type", data=CombinedData)
plt.xlabel("Initial Hazard Level [Total CFU]")
plt.ylabel("Proportion of CFU Rejected by PHS")

