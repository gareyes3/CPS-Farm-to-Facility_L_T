# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 11:13:00 2022

@author: gareyes3
"""

#Marginal Gain analysis sampling, creation of the funtion. 

#%%
import sys, os
sys.path
sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model')
sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility\Model')

# %%
import random
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


reload(MainModel3z)
reload(Inputz)
reload(SCInputz)
reload(ScenCondz)

#%%

#Options
     #Washing
     #Holding
     #Pre-cooling
     #Pre-Wash
     #PHS4d
     #PHS4h
     #PHSInt
     #HTrad
     #RTrad
     #FPTrad
     
def scenario_function(
                      #Intervention Strategies
                      Washing = False,
                      Holding = False,
                      Pre_Cooling = False,
                      Harvest_Wash = False,
                      #Sampling Strategies.
                      PHS4d = False,
                      PHS4h= False,
                      PHSInt =False,
                      HSTrad = False,
                      RSTrad = False,
                      FPSTrad = False
                      ):
    ''' Docstring
    Select the scenarios from the arguements to run the scenario function. 
    Args: 
        
        Initial contamination (num): Number of CFU,
    
    Returns: 
        
        1. Outputs DF
        2. Progression DF
        3. Proportion Progression DF
    
    '''
    
    #Contamination Type
    ContCondz.Systematic_C = True
    
    #Management of System Control: 
    
    #Holding Time:
        #Potentially this scenario will only be applicable to the munre and irrigation scenario. 
    ScenCondz.Holding_Time= Holding #if we have 0-8 days or 2-8 days. 
    
    #Turning off Pre-Cooling
        #Precooling yes or not. 
    SCInputz.Pre_CoolingYN = Pre_Cooling 
    
    # Turning of Washing. 
        #Washing process yes or not. 
    SCInputz.Washing_YN = Washing
    
    #Harvest Pre-Wash: 
        #Harvest Pre-Wash yes or not
    SCInputz.C_Spray_HYN =Harvest_Wash
    
    
    SCInputz.SysHazard_lvl = 1_000_000  #CFU # background contaminatio
    SCInputz.SysCluster_Size = np.random.choice(np.arange(1_000,100_001,1_000)) #Range of cluster from 1,000 lb to 100,000 lb 
    SCInputz.SysNo_Cont_Clusters = 1 #One cluster per field.  
    
    #Sampling Condition
    # Sampling Conditions, Baseline all conditions are off
    
    ScenCondz.Baseline_Sampling = 0  # all others must be 0 if this one is 1
    #PHS4d
    if PHS4d == True:
        ScenCondz.PH_Sampling = 1
        ScenCondz.PHS_4d = 1
        
    if PHS4h == True:
        ScenCondz.PH_Sampling = 1
        ScenCondz.PHS_4h = 1
    
    if PHSInt == True:
        ScenCondz.PH_Sampling = 1
        ScenCondz.PHS_Int = 1
    
    if HSTrad == True:
        ScenCondz.H_Sampling = 1
        ScenCondz.HS_Trad = 1
    
    if RSTrad == True:
        ScenCondz.R_Sampling = 1
    
    if FPSTrad == True:
        ScenCondz.FP_Sampling = 1
        ScenCondz.FPS_Trad = 1

    
    #Running The Model.
    Main_Mod_Outs = MainModel3z.F_MainLoop()
    
    #Getting the outputs from the function.
    OutputDF = Main_Mod_Outs[1]
    ProgDF = Main_Mod_Outs[0]
    PropProgDF = Main_Mod_Outs[2]
    #FinalConts = Main_Mod_Outs[6]
    
    return [OutputDF,ProgDF,PropProgDF]
    

#%% Running the scenarios. 

### BASELINE ###
#Baseline Scenario No Intervention. 
Baseline_NI =  scenario_function()


#Baseline Scenario All Interventions.
Baseline_AI =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 Harvest_Wash = True)

### Pre-Harvest Sampling 4 days. 

#Baseline no intervention. 4 days preharvest sampling
Baseline_NI_PHS4d =  scenario_function(PHS4d = True)

#Baseline with intervention. 4 days pre-harvest sampling

Baseline_AI_PHS4d =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 Harvest_Wash = True,
                                 PHS4d = True)

### Pre-Harvest Sampling 4h
#Baseline no intervention. 4 hours preharvest sampling
Baseline_NI_PHS4h =  scenario_function(PHS4h = True)

#Baseline with intervention. 4 hours pre-harvest sampling

Baseline_AI_PHS4h =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 Harvest_Wash = True,
                                 PHS4h = True)

### Pre-Harvest Sampling 4h
#Baseline no intervention. 4 hours preharvest sampling
Baseline_NI_PHSInt =  scenario_function(PHSInt = True)

#Baseline with intervention. 4 hours pre-harvest sampling

Baseline_AI_PHSInt =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 Harvest_Wash = True,
                                 PHSInt = True)



#%% Data analysis

#Creating list of contamination progression
List_of_Progs = [Baseline_NI[1],
                     Baseline_AI[1],
                     Baseline_NI_PHS4d[1],
                     Baseline_AI_PHS4d[1],
                     Baseline_NI_PHS4h[1],
                     Baseline_AI_PHS4h[1],
                     Baseline_NI_PHSInt[1],
                     Baseline_AI_PHSInt[1]
                     ]


List_of_Rejs = [Baseline_NI[0],
                     Baseline_AI[0],
                     Baseline_NI_PHS4d[0],
                     Baseline_AI_PHS4d[0],
                     Baseline_NI_PHS4h[0],
                     Baseline_AI_PHS4h[0],
                     Baseline_NI_PHSInt[0],
                     Baseline_AI_PHSInt[0]
                     ]

List_of_Final_Conts = [x["Final Product Facility"] for x in List_of_Progs]
Column_Names = "BaselineNI BaselineAI NI_PHS4D AI_PHS4D NI_PHS4H AI_PHS4H NI_PHSInt AI_PHSInt".split()


List_of_Final_Rejs = [x['PH_CFU_PerR'] for x in List_of_Rejs]
Final_Contdf_Rejs = pd.concat(List_of_Final_Rejs, axis = 1)
Final_Contdf_Rejs.columns = Column_Names



Final_Contdf = pd.concat(List_of_Final_Conts, axis = 1)
Final_Contdf.columns = Column_Names
#melting that dataframe
Final_Contdf_melted = Final_Contdf.melt()

H=sns.catplot(x="variable", y="value", kind = "box" ,
            data=Final_Contdf_melted)
plt.xlabel("Sampling Scenario")
plt.ylabel("Total CFUs")
plt.yscale('log')
plt.title("Log10 CFU Final Contaminations")
plt.xticks(rotation=70)

H=sns.catplot(x="variable", y="value", kind = "bar" ,
            data=Final_Contdf_melted)
plt.xlabel("Sampling Scenario")
plt.ylabel("Total CFUs")
plt.yscale('log')
plt.title("Log10 CFU Final Contaminations")
plt.xticks(rotation=70)


#%%
#COMPARING THE mean and 95% CI Reduction between two groups. 
import numpy as np
import math
import scipy.stats as st
import statsmodels.stats.api as sms

def mean_CI_ONE(Array):
    mean = Array.mean()
    CI = sms.DescrStatsW(Array).tconfint_mean()
    #log_mean = mean.log10()
    #CI_log = CI.log10()
    return [mean,CI]

[mean_CI_ONE(x) for x in List_of_Final_Conts]



[mean_CI_ONE(x) for x in List_of_Final_Rejs]
