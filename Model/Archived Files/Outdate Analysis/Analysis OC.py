# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 16:07:07 2021

@author: Gustavo Reyes
"""

#Contamination Leves

#Wrapped Testing Strategy
# Y = %Rejected
# X = Contamination Levels
#Inside Sampling Strategy

#%%
import sys
sys.path
sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model')
#sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility\Model')

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

#Own Libraries
import Funz
import ContScen
import Listz 
import OutFunz
import InFunz
import ScenCondz
import Inputz
import ContCondz
from importlib import reload 

#Main Model Loops
import MainModel3z

#%% 
#Progression DataFrame. 
Progression_DFS = []



#%%                                                    BACKGROUND CONTAMINATION
#Contamination Challenges
ContCondz.Background_C=1
ContCondz.Point_Source_C=0
ContCondz.Systematic_C=0

#Harvester Contamination
ContCondz.Crew_C = 0
ContCondz.Harvester_C = 0

#Processing equipment
ContCondz.PE_C = 0
ContCondz.PE_Cont_Loc = 0,#1,2,3,4,5
#1 = Shredder, #2 = Belt, #3 = Washing, #4 Shaker, #5Centrifuge
ContCondz.Pack_C= 0

#%% Contamination Level Analysis PH 4d
reload(ScenCondz)
#50,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 50000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PH4d_50k = Main_Mod_Outs[1]
D_BGProg_PH4d_50k=Main_Mod_Outs[0]

#10,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 10000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PH4d_10k = Main_Mod_Outs[1]
D_BGProg_PH4d_10k=Main_Mod_Outs[0]

#5000 CFU INitial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 5000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PH4d_5k = Main_Mod_Outs[1]
D_BGProg_PH4d_5k=Main_Mod_Outs[0]

#1000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 1000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PH4d_1k = Main_Mod_Outs[1]
D_BGProg_PH4d_1k=Main_Mod_Outs[0]

#100 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 100
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PH4d_100 = Main_Mod_Outs[1]
D_BGProg_PH4d_100=Main_Mod_Outs[0]
#%% Contamination Level Analysis PH 4h

ScenCondz.PHS_4d = 0
ScenCondz.PHS_4h = 1

#50,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 50000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PH4h_50k = Main_Mod_Outs[1]
D_BGProg_PH4h_50k=Main_Mod_Outs[0]

#10,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 10000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PH4h_10k = Main_Mod_Outs[1]
D_BGProg_PH4h_10k=Main_Mod_Outs[0]

#5000 CFU INitial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 5000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PH4h_5k = Main_Mod_Outs[1]
D_BGProg_PH4h_5k=Main_Mod_Outs[0]

#1000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 1000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PH4h_1k = Main_Mod_Outs[1]
D_BGProg_PH4h_1k=Main_Mod_Outs[0]

#100 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 100
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PH4h_100 = Main_Mod_Outs[1]
D_BGProg_PH4h_100=Main_Mod_Outs[0]

#%% Contamination Level Analysis PH Intense

ScenCondz.PHS_4d = 0
ScenCondz.PHS_4h = 0
ScenCondz.PHS_Int = 1 #Scenario 3

#50,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 50000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PHInt_50k = Main_Mod_Outs[1]
D_BGProg_PHInt_50k=Main_Mod_Outs[0]

#10,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 10000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PHInt_10k = Main_Mod_Outs[1]
D_BGProg_PHInt_10k=Main_Mod_Outs[0]

#5000 CFU INitial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 5000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PHInt_5k = Main_Mod_Outs[1]
D_BGProg_PHInt_5k=Main_Mod_Outs[0]

#1000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 1000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PHInt_1k = Main_Mod_Outs[1]
D_BGProg_PHInt_1k=Main_Mod_Outs[0]

#100 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 100
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_BG_PHInt_100 = Main_Mod_Outs[1]
D_BGProg_PHInt_100=Main_Mod_Outs[0]





#%%                                                 POINT SOURCE CONTAMINATION
#Contamination Challenges
ContCondz.Background_C=0
ContCondz.Point_Source_C=1
ContCondz.Systematic_C=0

#Harvester Contamination
ContCondz.Crew_C = 0
ContCondz.Harvester_C = 0

#Processing equipment
ContCondz.PE_C = 0
ContCondz.PE_Cont_Loc = 0,#1,2,3,4,5
#1 = Shredder, #2 = Belt, #3 = Washing, #4 Shaker, #5Centrifuge
ContCondz.Pack_C= 0

#%% Contamination Level Analysis PH 4d
reload(ScenCondz)
#50,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 50000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PH4d_50k = Main_Mod_Outs[1]
D_PSProg_PH4d_50k=Main_Mod_Outs[0]

#10,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 10000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PH4d_10k = Main_Mod_Outs[1]
D_PSProg_PH4d_10k=Main_Mod_Outs[0]

#5000 CFU INitial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 5000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PH4d_5k = Main_Mod_Outs[1]
D_PSProg_PH4d_5k=Main_Mod_Outs[0]

#1000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 1000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PH4d_1k = Main_Mod_Outs[1]
D_PSProg_PH4d_1k=Main_Mod_Outs[0]

#100 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 100
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PH4d_100 = Main_Mod_Outs[1]
D_PSProg_PH4d_100=Main_Mod_Outs[0]
#%% Contamination Level Analysis PH 4h

ScenCondz.PHS_4d = 0
ScenCondz.PHS_4h = 1

#50,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 50000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PH4h_50k = Main_Mod_Outs[1]
D_PSProg_PH4h_50k=Main_Mod_Outs[0]

#10,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 10000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PH4h_10k = Main_Mod_Outs[1]
D_PSProg_PH4h_10k=Main_Mod_Outs[0]

#5000 CFU INitial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 5000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PH4h_5k = Main_Mod_Outs[1]
D_PSProg_PH4h_5k=Main_Mod_Outs[0]

#1000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 1000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PH4h_1k = Main_Mod_Outs[1]
D_PSProg_PH4h_1k=Main_Mod_Outs[0]

#100 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 100
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PH4h_100 = Main_Mod_Outs[1]
D_PSProg_PH4h_100=Main_Mod_Outs[0]

#%% Contamination Level Analysis PH Intense

ScenCondz.PHS_4d = 0
ScenCondz.PHS_4h = 0
ScenCondz.PHS_Int = 1 #Scenario 3

#50,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 50000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PHInt_50k = Main_Mod_Outs[1]
D_PSProg_PHInt_50k=Main_Mod_Outs[0]

#10,000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 10000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PHInt_10k = Main_Mod_Outs[1]
D_PSProg_PHInt_10k=Main_Mod_Outs[0]

#5000 CFU INitial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 5000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PHInt_5k = Main_Mod_Outs[1]
D_PSProg_PHInt_5k=Main_Mod_Outs[0]

#1000 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 1000
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PHInt_1k = Main_Mod_Outs[1]
D_PSProg_PHInt_1k=Main_Mod_Outs[0]

#100 CFU Initial
reload(Inputz) #Reload Inputz
reload(Listz) #ReUPdate Lists
Inputz.Hazard_lvl = 100
Main_Mod_Outs=MainModel3z.F_MainLoop()
D_PS_PHInt_100 = Main_Mod_Outs[1]
D_PSProg_PHInt_100=Main_Mod_Outs[0]







#%% Graphics for Proportion CFU Rejected. 

#BACKGROUND

L_PR_PH4d = {
                ' 50K':D_BG_PH4d_50k["PerRejected at PH"],
                ' 10K':D_BG_PH4d_10k["PerRejected at PH"],
                ' 5K':D_BG_PH4d_5k["PerRejected at PH"],
                ' 1K':D_BG_PH4d_1k["PerRejected at PH"],
                ' 100':D_BG_PH4d_100["PerRejected at PH"],
          }

df_L_PR_PH4d = pd.DataFrame(L_PR_PH4d)
df_L_PR_PH4d_melted = pd.melt(df_L_PR_PH4d)
df_L_PR_PH4d_melted["Type"] = "4d"


L_PR_PH4h = {
                ' 50K':D_BG_PH4h_50k["PerRejected at PH"],
                ' 10K':D_BG_PH4h_10k["PerRejected at PH"],
                ' 5K':D_BG_PH4h_5k["PerRejected at PH"],
                ' 1K':D_BG_PH4h_1k["PerRejected at PH"],
                ' 100':D_BG_PH4h_100["PerRejected at PH"],
          }

df_L_PR_PH4h = pd.DataFrame(L_PR_PH4h)
df_L_PR_PH4h_melted = pd.melt(df_L_PR_PH4h)
df_L_PR_PH4h_melted["Type"] = "4h"


L_PR_PHInt = {
                ' 50K':D_BG_PHInt_50k["PerRejected at PH"],
                ' 10K':D_BG_PHInt_10k["PerRejected at PH"],
                ' 5K':D_BG_PHInt_5k["PerRejected at PH"],
                ' 1K':D_BG_PHInt_1k["PerRejected at PH"],
                ' 100':D_BG_PHInt_100["PerRejected at PH"],
          }

df_L_PR_PHInt = pd.DataFrame(L_PR_PHInt)
df_L_PR_PHInt_melted = pd.melt(df_L_PR_PHInt)
df_L_PR_PHInt_melted["Type"] = "Int"


CombinedData = pd.concat([df_L_PR_PH4d_melted,
                          df_L_PR_PH4h_melted,
                          df_L_PR_PHInt_melted])


Scenariosplot =sns.lineplot(x="variable", y="value", hue = "Type", data=CombinedData)
plt.xlabel("Initial Hazard Level [Total CFU]")
plt.ylabel("Proportion of CFU Rejected by Sampling Strategy")


#%%
#POINT SOURCE
#Graphics for Proportion CFU Rejected. 

L_PR_PH4d_PS = {
                ' 50K':D_PS_PH4d_50k["PerRejected at PH"],
                ' 10K':D_PS_PH4d_10k["PerRejected at PH"],
                ' 5K':D_PS_PH4d_5k["PerRejected at PH"],
                ' 1K':D_PS_PH4d_1k["PerRejected at PH"],
                ' 100':D_PS_PH4d_100["PerRejected at PH"],
          }

df_L_PR_PH4d_PS = pd.DataFrame(L_PR_PH4d_PS)
df_L_PR_PH4d_PS_melted = pd.melt(df_L_PR_PH4d_PS)
df_L_PR_PH4d_PS_melted["Type"] = "4d"


L_PR_PH4h_PS = {
                ' 50K':D_PS_PH4h_50k["PerRejected at PH"],
                ' 10K':D_PS_PH4h_10k["PerRejected at PH"],
                ' 5K':D_PS_PH4h_5k["PerRejected at PH"],
                ' 1K':D_PS_PH4h_1k["PerRejected at PH"],
                ' 100':D_PS_PH4h_100["PerRejected at PH"],
          }

df_L_PR_PH4h_PS = pd.DataFrame(L_PR_PH4h_PS)
df_L_PR_PH4h_PS_melted = pd.melt(df_L_PR_PH4h_PS)
df_L_PR_PH4h_PS_melted["Type"] = "4h"


L_PR_PHInt_PS = {
                ' 50K':D_PS_PHInt_50k["PerRejected at PH"],
                ' 10K':D_PS_PHInt_10k["PerRejected at PH"],
                ' 5K':D_PS_PHInt_5k["PerRejected at PH"],
                ' 1K':D_PS_PHInt_1k["PerRejected at PH"],
                ' 100':D_PS_PHInt_100["PerRejected at PH"],
          }

df_L_PR_PHInt_PS = pd.DataFrame(L_PR_PHInt_PS)
df_L_PR_PHInt_PS_melted = pd.melt(df_L_PR_PHInt_PS)
df_L_PR_PHInt_PS_melted["Type"] = "Int"


CombinedData_PS = pd.concat([df_L_PR_PH4d_PS_melted,
                          df_L_PR_PH4h_PS_melted,
                          df_L_PR_PHInt_PS_melted])


Scenariosplot =sns.lineplot(x="variable", y="value", hue = "Type", data=CombinedData_PS)
plt.xlabel("Initial Hazard Level [Total CFU]")
plt.ylabel("Proportion of CFU Rejected by Sampling Strategy")



#%% 
#Wrapped:
CombinedData["Contamination"] = 'Background'
CombinedData_PS["Contamination"] = 'PointSource'
WrappedData = pd.concat([CombinedData,
                          CombinedData_PS])
    
g = sns.FacetGrid(WrappedData, col="Contamination")
g.map(sns.lineplot,"variable", "value",  "Type")

#%% Graphics for Proportion Weight Rejected. 

L_PRW_PH4d_PS = {
                ' 50K':D_PS_PH4d_50k["PerRejectedWeight"],
                ' 10K':D_PS_PH4d_10k["PerRejectedWeight"],
                ' 5K':D_PS_PH4d_5k["PerRejectedWeight"],
                ' 1K':D_PS_PH4d_1k["PerRejectedWeight"],
                ' 100':D_PS_PH4d_100["PerRejectedWeight"],
          }

df_L_PRW_PH4d_PS = pd.DataFrame(L_PRW_PH4d_PS)
df_L_PRW_PH4d_PS_melted = pd.melt(df_L_PRW_PH4d_PS)
df_L_PRW_PH4d_PS_melted["Type"] = "4d"


L_PRW_PH4h_PS = {
                ' 50K':D_PS_PH4h_50k["PerRejectedWeight"],
                ' 10K':D_PS_PH4h_10k["PerRejectedWeight"],
                ' 5K':D_PS_PH4h_5k["PerRejectedWeight"],
                ' 1K':D_PS_PH4h_1k["PerRejectedWeight"],
                ' 100':D_PS_PH4h_100["PerRejectedWeight"],
          }

df_L_PRW_PH4h_PS = pd.DataFrame(L_PRW_PH4h_PS)
df_L_PRW_PH4h_PS_melted = pd.melt(df_L_PRW_PH4h_PS)
df_L_PRW_PH4h_PS_melted["Type"] = "4h"


L_PRW_PHInt_PS = {
                ' 50K':D_PS_PHInt_50k["PerRejectedWeight"],
                ' 10K':D_PS_PHInt_10k["PerRejectedWeight"],
                ' 5K':D_PS_PHInt_5k["PerRejectedWeight"],
                ' 1K':D_PS_PHInt_1k["PerRejectedWeight"],
                ' 100':D_PS_PHInt_100["PerRejectedWeight"],
          }

df_L_PRW_PHInt_PS = pd.DataFrame(L_PRW_PHInt_PS)
df_L_PRW_PHInt_PS_melted = pd.melt(df_L_PRW_PHInt_PS)
df_L_PRW_PHInt_PS_melted["Type"] = "Int"


CombinedDataPRW_PS = pd.concat([df_L_PRW_PH4d_PS_melted,
                          df_L_PRW_PH4h_PS_melted,
                          df_L_PRW_PHInt_PS_melted])


Scenariosplot =sns.lineplot(x="variable", y="value", hue = "Type", data=CombinedDataPRW_PS)
plt.xlabel("Initial Hazard Level [Total CFU]")
plt.ylabel("Proportion of Weight Rejected by Sampling Strategy")

