# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 10:35:17 2021

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

#%% Intense PH-Sampling Different Mass Size
ScenCondz.PHS_4d = 0
ScenCondz.PHS_4h = 0
ScenCondz.PHS_Int = 1 #Scenario 3

#%%
#300 Gram Composite

#50,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 1
Inputz.Hazard_lvl = 50000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_300_50k = Main_Mod_Outs[1]
DProg_300_50k=Main_Mod_Outs[0]

#10,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 1
Inputz.Hazard_lvl = 10000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_300_10k = Main_Mod_Outs[1]
DProg_300_10k=Main_Mod_Outs[0]

#5000 CFU INitial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 1
Inputz.Hazard_lvl = 5000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_300_5k = Main_Mod_Outs[1]
DProg_300_5k=Main_Mod_Outs[0]

#1000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 1
Inputz.Hazard_lvl = 1000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_300_1k = Main_Mod_Outs[1]
DProg_300_1k=Main_Mod_Outs[0]

#100 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 1
Inputz.Hazard_lvl = 100
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_300_100 = Main_Mod_Outs[1]
DProg_300_100=Main_Mod_Outs[0]
#%%
#600 Gram Composite

#50,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 2
Inputz.Hazard_lvl = 50000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_600_50k = Main_Mod_Outs[1]
DProg_600_50k=Main_Mod_Outs[0]

#10,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 2
Inputz.Hazard_lvl = 10000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_600_10k = Main_Mod_Outs[1]
DProg_600_10k=Main_Mod_Outs[0]

#5000 CFU INitial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 2
Inputz.Hazard_lvl = 5000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_600_5k = Main_Mod_Outs[1]
DProg_600_5k=Main_Mod_Outs[0]

#1000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 2
Inputz.Hazard_lvl = 1000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_600_1k = Main_Mod_Outs[1]
DProg_600_1k=Main_Mod_Outs[0]

#100 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 2
Inputz.Hazard_lvl = 100
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_600_100 = Main_Mod_Outs[1]
DProg_600_100=Main_Mod_Outs[0]

#%%
#1200 Gram Composite

#50,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 4
Inputz.Hazard_lvl = 50000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_1200_50k = Main_Mod_Outs[1]
DProg_1200_50k=Main_Mod_Outs[0]

#10,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 4
Inputz.Hazard_lvl = 10000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_1200_10k = Main_Mod_Outs[1]
DProg_1200_10k=Main_Mod_Outs[0]

#5000 CFU INitial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 4
Inputz.Hazard_lvl = 5000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_1200_5k = Main_Mod_Outs[1]
DProg_1200_5k=Main_Mod_Outs[0]

#1000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 4
Inputz.Hazard_lvl = 1000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_1200_1k = Main_Mod_Outs[1]
DProg_1200_1k=Main_Mod_Outs[0]

#100 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 4
Inputz.Hazard_lvl = 100
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_1200_100 = Main_Mod_Outs[1]
DProg_1200_100=Main_Mod_Outs[0]
#%%
#2400 Gram Composite

#50,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 8
Inputz.Hazard_lvl = 50000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_2400_50k = Main_Mod_Outs[1]
DProg_2400_50k=Main_Mod_Outs[0]

#10,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 8
Inputz.Hazard_lvl = 10000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_2400_10k = Main_Mod_Outs[1]
DProg_2400_10k=Main_Mod_Outs[0]

#5000 CFU INitial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 8
Inputz.Hazard_lvl = 5000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_2400_5k = Main_Mod_Outs[1]
DProg_2400_5k=Main_Mod_Outs[0]

#1000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 8
Inputz.Hazard_lvl = 1000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_2400_1k = Main_Mod_Outs[1]
DProg_2400_1k=Main_Mod_Outs[0]

#100 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 8
Inputz.Hazard_lvl = 100
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_2400_100 = Main_Mod_Outs[1]
DProg_2400_100=Main_Mod_Outs[0]

#%%
#3600 Gram Composite

#50,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 12
Inputz.Hazard_lvl = 50000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_3600_50k = Main_Mod_Outs[1]
DProg_3600_50k=Main_Mod_Outs[0]

#10,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 12
Inputz.Hazard_lvl = 10000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_3600_10k = Main_Mod_Outs[1]
DProg_3600_10k=Main_Mod_Outs[0]

#5000 CFU INitial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 12
Inputz.Hazard_lvl = 5000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_3600_5k = Main_Mod_Outs[1]
DProg_3600_5k=Main_Mod_Outs[0]

#1000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 12
Inputz.Hazard_lvl = 1000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_3600_1k = Main_Mod_Outs[1]
DProg_3600_1k=Main_Mod_Outs[0]

#100 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.n_samples_lot_PH = 12
Inputz.Hazard_lvl = 100
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_3600_100 = Main_Mod_Outs[1]
DProg_3600_100=Main_Mod_Outs[0]
#%% Graphics. 

L_PR_300 = {
                ' 50K':D_300_50k["PerRejected at PH"],
                ' 10K':D_300_10k["PerRejected at PH"],
                ' 5K':D_300_5k["PerRejected at PH"],
                ' 1K':D_300_1k["PerRejected at PH"],
                ' 100':D_300_100["PerRejected at PH"],
          }

df_L_PR_300 = pd.DataFrame(L_PR_300)
df_L_PR_300_melted = pd.melt(df_L_PR_300)
df_L_PR_300_melted["Type"] = "300"
Scenariosplot =sns.catplot(x="variable", y="value", data=df_L_PR_300_melted ,kind="point",  height=4, aspect=2 )
plt.xlabel("Initial Hazard Level Total CFU")
plt.ylabel("Percentage of CFU Rejected at PHS")

L_PR_600 = {
                ' 50K':D_600_50k["PerRejected at PH"],
                ' 10K':D_600_10k["PerRejected at PH"],
                ' 5K':D_600_5k["PerRejected at PH"],
                ' 1K':D_600_1k["PerRejected at PH"],
                ' 100':D_600_100["PerRejected at PH"],
          }

df_L_PR_600 = pd.DataFrame(L_PR_600)
df_L_PR_600_melted = pd.melt(df_L_PR_600)
df_L_PR_600_melted["Type"] = "600"
Scenariosplot =sns.catplot(x="variable", y="value", data=df_L_PR_600_melted ,kind="point",  height=4, aspect=2 )
plt.xlabel("Initial Hazard Level Total CFU")
plt.ylabel("Percentage of CFU Rejected at PHS")


L_PR_1200 = {
                ' 50K':D_1200_50k["PerRejected at PH"],
                ' 10K':D_1200_10k["PerRejected at PH"],
                ' 5K':D_1200_5k["PerRejected at PH"],
                ' 1K':D_1200_1k["PerRejected at PH"],
                ' 100':D_1200_100["PerRejected at PH"],
          }

df_L_PR_1200 = pd.DataFrame(L_PR_1200)
df_L_PR_1200_melted = pd.melt(df_L_PR_1200)
df_L_PR_1200_melted["Type"] = "1200"
Scenariosplot =sns.catplot(x="variable", y="value", data=df_L_PR_1200_melted ,kind="point",  height=4, aspect=2 )
plt.xlabel("Initial Hazard Level Total CFU")
plt.ylabel("Percentage of CFU Rejected at PHS")

L_PR_2400 = {
                ' 50K':D_2400_50k["PerRejected at PH"],
                ' 10K':D_2400_10k["PerRejected at PH"],
                ' 5K':D_2400_5k["PerRejected at PH"],
                ' 1K':D_2400_1k["PerRejected at PH"],
                ' 100':D_2400_100["PerRejected at PH"],
          }

df_L_PR_2400 = pd.DataFrame(L_PR_2400)
df_L_PR_2400_melted = pd.melt(df_L_PR_2400)
df_L_PR_2400_melted["Type"] = "2400"
Scenariosplot =sns.catplot(x="variable", y="value", data=df_L_PR_2400_melted ,kind="point",  height=4, aspect=2 )
plt.xlabel("Initial Hazard Level Total CFU")
plt.ylabel("Percentage of CFU Rejected at PHS")


L_PR_3600 = {
                ' 50K':D_3600_50k["PerRejected at PH"],
                ' 10K':D_3600_10k["PerRejected at PH"],
                ' 5K':D_3600_5k["PerRejected at PH"],
                ' 1K':D_3600_1k["PerRejected at PH"],
                ' 100':D_3600_100["PerRejected at PH"],
          }

df_L_PR_3600 = pd.DataFrame(L_PR_3600)
df_L_PR_3600_melted = pd.melt(df_L_PR_3600)
df_L_PR_3600_melted["Type"] = "3600"
Scenariosplot =sns.catplot(x="variable", y="value", data=df_L_PR_3600_melted ,kind="point",  height=4, aspect=2 )
plt.xlabel("Initial Hazard Level Total CFU")
plt.ylabel("Percentage of CFU Rejected at PHS")


CombinedData_Samp = pd.concat([df_L_PR_300_melted,
                          df_L_PR_600_melted,
                          df_L_PR_1200_melted,
                          df_L_PR_2400_melted,
                          df_L_PR_3600_melted])


Scenariosplot =sns.lineplot(x="Type", y="value", hue = "variable", data=CombinedData_Samp)
plt.xlabel("Composite Sample Mass g")
plt.ylabel("Proportion of CFU Rejected by PHS")
Scenariosplot.legend_.set_title('Initial CFU')

Scenariosplot =sns.lineplot(x="variable", y="value", hue = "Type", data=CombinedData_Samp)
plt.xlabel("Initial Hazard Level [Total CFU]")
plt.ylabel("Proportion of CFU Rejected by PHS")


