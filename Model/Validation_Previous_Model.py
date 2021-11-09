# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 14:09:39 2021

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
sys.path
#sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model')
sys.path.append(
    'C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility\Model')
#%%
#%%

Total_grams= SCInputz.Field_Weight*454


CFU_10000g = Total_grams/10000 #-4 log
CFU_1000g = Total_grams/1000  #-3 log
CFU_100g = Total_grams/100 #-2 log
CFU_10g = Total_grams/10  #-1 log
CFU_g =  Total_grams #0 log
CFU_0_1g = Total_grams*10 #1 log


CFU_0_01g = Total_grams*100 #2log
CFU_0_001g = Total_grams*1000 #3log

#%% BAseline Sampling: 
#Contamination Challenges
ContCondz.Background_C=True
ContCondz.Point_Source_C=False
ContCondz.Systematic_C=False

#Harvester Contamination
ContCondz.Crew_C = False
ContCondz.Harvester_C = False

#Processing equipment
ContCondz.PE_C = False
ContCondz.PE_Cont_Loc = False,#1,2,3,4,5
#1 = Shredder, #2 = Belt, #3 = Washing, #4 Shaker, #5Centrifuge
ContCondz.Pack_C= False

#%%
Tuning_Contamination_levels = [CFU_10000g,CFU_1000g,CFU_100g,CFU_10g]
Tuning_SampleSize =[180,360,900,1800,3600]#[60,120,300,600,1200]

#%%


import time
start_time = time.time()

reload(ScenCondz)

Desired_Outputs = ["PH_CFU_PerR", "PH_Wei_PerR"""]
Output_Collection_List = [] #First Index

for k in Tuning_Contamination_levels:
    for i in Tuning_SampleSize:


        # Sampling Conditions, Baseline all conditions are off
        ScenCondz.Baseline_Sampling = 0  # all others must be 0if this one is 1
        ScenCondz.PH_Sampling = 1
        ScenCondz.H_Sampling = 0
        ScenCondz.R_Sampling = 0
        ScenCondz.FP_Sampling = 0
        # Pre_Harvest 4 Days
        ScenCondz.PHS_4d = 1  # Scenario 1
        ScenCondz.PHS_4h = 0  # Scenario 2
        ScenCondz.PHS_Int = 0  # Scenario 3


        reload(SCInputz)  # Reload Inputz
        reload(Listz)  # Reload Lists
        
        #Updating Hazard Level
        SCInputz.BGHazard_lvl = k
        #Updating Sample Size
        SCInputz.sample_size_PH = i
        
        #Running the main Loop
        Main_Mod_Outs = Trial_MainLoop_PH.F_MainLoop_Validation()
        
        OutputDF = Main_Mod_Outs[1]
        ProgDF = Main_Mod_Outs[0]
        
        DF= OutFunz.F_Output_get_cols(Outdf = OutputDF , ColNames = Desired_Outputs)
        #DF= pd.melt(DF)
        DF["ContLevel"] = k
        DF["SampleMass"] = i
        Output_Collection_List.append(DF)
             
print("--- %s seconds ---" % (time.time() - start_time))

Combined_df_Probs = pd.concat(Output_Collection_List)

Combined_df_Probs["PH_CFU_PerA"] = 1-Combined_df_Probs["PH_CFU_PerR"]
#%%
sns.lineplot(x="SampleMass", y="PH_CFU_PerA", hue = "ContLevel" ,data=Combined_df_Probs)
plt.xlabel("Composite Sample Mass")
plt.ylabel("% of contamination Accepted")
plt.title("Area Contamination, Uniform")
# Put the legend out of the figure
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)









