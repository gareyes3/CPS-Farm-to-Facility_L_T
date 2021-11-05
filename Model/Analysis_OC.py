# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 14:46:17 2021

@author: gareyes3
"""

#OC Curve Analysis

#Y Probability of Acceptance/ Percent Accepted CFU
#X= Contamination level
#Color/Hue = Sample Size & Rejection Rule. 
    #Sampling Size, Sampling Type. 
#Facet Sampling Type.


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
sys.path
#sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model')
sys.path.append(
    'C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility\Model')

#%%

Total_grams= SCInputz.Field_Weight*454


CFU_10000g = Total_grams/10000 #-4 log
CFU_1000g = Total_grams/1000  #-3 log
CFU_100g = Total_grams/100 #-2 log
CFU_10g = Total_grams/10  #-1 log
CFU_g =  Total_grams #0 log


CFU_0_1g = Total_grams*10 #1 log
CFU_0_01g = Total_grams*100 #2log

#%%
Tuning_SampleSize = [60,120,300,600,1200] #list(range(100,1200,200))
#Tuning_HazardLevel = [4536,45360,450360,4503600]#list(range(10000,130000,10000)) #1 CFU/10kg, 1CFU kg, 1CFU/100g, 1CFU/10g. 
Tuning_SampType = ["4d","4h","Int"]
Tuning_Contamination_levels = [CFU_10000g,CFU_1000g,CFU_100g,CFU_10g,CFU_g, CFU_0_1g]

Desired_Outputs = ["PH_CFU_PerR", "PH_Wei_PerR"""]
Output_Collection_List = [] #First Index
for k in Tuning_Contamination_levels:
    for i in Tuning_SampleSize:
        for j in Tuning_SampType:  
            # Sampling Conditions, Baseline all conditions are off
            ScenCondz.Baseline_Sampling = 0  # all others must be 0if this one is 1
            ScenCondz.PH_Sampling = 1
            ScenCondz.H_Sampling = 0
            ScenCondz.R_Sampling = 0
            ScenCondz.FP_Sampling = 0
            # Pre_Harvest 4 Days
            # Pre-Harvest
            if j == "4d":
                ScenCondz.PHS_4d = 1  # Scenario 1
                ScenCondz.PHS_4h = 0  # Scenario 2
                ScenCondz.PHS_Int = 0  # Scenario 3
            if j == "4h":
                ScenCondz.PHS_4d = 0  # Scenario 1
                ScenCondz.PHS_4h = 1  # Scenario 2
                ScenCondz.PHS_Int = 0  # Scenario 3
            if j == "Int":
                ScenCondz.PHS_4d = 0  # Scenario 1
                ScenCondz.PHS_4h = 0 # Scenario 2
                ScenCondz.PHS_Int = 1  # Scenario 3
            
            reload(SCInputz)  # Reload Inputz
            reload(Listz)  # ReUPdate Lists
            
            #Updating Clustering
            SCInputz.PSCluster_Size = 1000 #lb 1% cluster. 
            SCInputz.PSNo_Cont_Clusters = 1 #4 1000k lb clusters. 
            
            SCInputz.PSHazard_lvl = k
            SCInputz.sample_size_PH = i
            #SCInputz.BGHazard_lvl = j
            #SCInputz.No_Grabs_PH = j
            
            Main_Mod_Outs = MainModel3z.F_MainLoop()
            OutputDF = Main_Mod_Outs[1]
            ProgDF = Main_Mod_Outs[0]
            
            DF= OutFunz.F_Output_get_cols(Outdf = OutputDF , ColNames = Desired_Outputs)
            #DF= pd.melt(DF)
            DF["ContLevel"] = k
            DF["GrabNo"] = j
            DF["SampSize"] = i
            Output_Collection_List.append(DF)
             

Combined_df_Probs = pd.concat(Output_Collection_List)



