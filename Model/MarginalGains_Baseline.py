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
    reload(MainModel3z)
    reload(Inputz)
    reload(SCInputz)
    reload(ScenCondz)
    reload(ContCondz)
    
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
    
    reload(SCInputz)
    
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
    
    
    SCInputz.SysHazard_lvl = 100_000  #CFU # background contaminatio
    SCInputz.SysCluster_Size = np.random.choice(np.arange(1_000,100_001,1_000)) #Range of cluster from 1,000 lb to 100,000 lb 
    SCInputz.SysNo_Cont_Clusters = 1 #One cluster per field.  
    

    
    #Running The Model.
    Main_Mod_Outs = MainModel3z.F_MainLoop()
    
    #Getting the outputs from the function.
    OutputDF = Main_Mod_Outs[1]
    ProgDF = Main_Mod_Outs[0]
    PropProgDF = Main_Mod_Outs[2]
    #FinalConts = Main_Mod_Outs[6]
    
    return [OutputDF,ProgDF,PropProgDF]

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

def Calc_red(meanCI, treatments):
    list_1=[]
    for i in list(range(0,treatments)):
        mean = meanCI[i][0]
        list_1.append(((meanCI[0][0]-mean)/meanCI[0][0]))
    return list_1
    
#%% Effect of Individual Interventions
Baseline_NI =  scenario_function()

#Effect of Holding
Baseline_NI_Holding =  scenario_function(Holding=True)

#Effect of PreCooling
Baseline_NI_Precooling =  scenario_function(Pre_Cooling=True)

#Effect of Wash
Baseline_NI_Wash =  scenario_function(Washing=True)

#Harvest Wash
Baseline_NI_H_Wash =  scenario_function(Harvest_Wash=True)


Baseline_NI[1].columns

#Initial Contamination From BAseline
(Baseline_NI[1]['Contam Event Before PHS'].mean() - 6882030.7) / Baseline_NI[1]['Contam Event Before PHS'].mean()

(6882030.7- Baseline_NI_Holding[1]['Final Product Facility'].mean()) / 6882030.7


Intervention_Final_Conts = [Baseline_NI[1],
                     Baseline_NI_Holding[1],
                     Baseline_NI_Precooling[1],
                     Baseline_NI_Wash[1],
                     Baseline_NI_H_Wash[1]
                     ]



List_of_Final_Conts_Ints = [x["Final Product Facility"] for x in Intervention_Final_Conts]
Column_Names = "BaselineNI Holding Precooling Washing Harvest_Wash".split()


Final_Conts_INT = pd.concat(List_of_Final_Conts_Ints, axis = 1)
Final_Conts_INT.columns = Column_Names
Final_Conts_INT_melted = Final_Conts_INT.melt()

H=sns.catplot(x="variable", y="value", kind = "bar" ,
            data=Final_Conts_INT_melted)
plt.xlabel("Intervention")
plt.ylabel("Total CFUs at Finished Product")
plt.yscale('log')
plt.title("CFU Final Contamination")
plt.xticks(rotation=70)



Mean_andCI= [mean_CI_ONE(x) for x in List_of_Final_Conts_Ints]




Reduction = Calc_red(meanCI =Mean_andCI,treatments= 5)

reduction_DF = pd.DataFrame({"Treatment": Column_Names,
                             "Reduction": Reduction} )

reduction_DF=reduction_DF.sort_values('Reduction',ascending=False).reset_index()

chart = sns.barplot(data = reduction_DF, x = "Treatment", y = "Reduction", order=reduction_DF['Treatment'])
chart.bar_label(chart.containers[0])
plt.title("mean % Reduction obtained by Intervention")
plt.xlabel("Intervention")
plt.ylabel("Percent Reduction from Baseline NI")

Intervention_Comp = pd.DataFrame([mean_CI_ONE(x) for x in List_of_Final_Conts_Ints], columns = ["mean", "95% CI"])


#%% Running the scenarios. 

### BASELINE  NO INTERVENTION###
#Baseline Scenario No Intervention. 
Baseline_NI =  scenario_function()

### Pre-Harvest Sampling 4 days.
#Baseline no intervention. 4 days preharvest sampling
Baseline_NI_PHS4d =  scenario_function(PHS4d = True)

#Baseline no intervention. 4 hours preharvest sampling
Baseline_NI_PHS4h =  scenario_function(PHS4h = True)

#Baseline no intervention. 4 hours preharvest sampling
Baseline_NI_PHSInt =  scenario_function(PHSInt = True)

#Baseline no intervention Harvest Sampling Traditional
Baseline_NI_H=  scenario_function(HSTrad = True)

#Baseline no intervention Receiving Samplgin Traditional
Baseline_NI_R=  scenario_function(RSTrad =True)

#Baseline no intervention Receiving Samplgin Traditional
Baseline_NI_FP=  scenario_function(FPSTrad =True)



### BASELINE  ALL INTERVENTIONS###

### Pre-Harvest Sampling 4 days.
#Baseline Scenario All Interventions.
Baseline_AI =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 Harvest_Wash = True)
 



#Baseline with intervention. 4 days pre-harvest sampling

Baseline_AI_PHS4d =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 Harvest_Wash = True,
                                 PHS4d = True)

### Pre-Harvest Sampling 4h
#Baseline no intervention. 4 hours preharvest sampling
Baseline_NI_PHS4h =  scenario_function(PHS4h = True)

### Pre-Harvest Sampling 4h
#Baseline with intervention. 4 hours pre-harvest sampling
Baseline_AI_PHS4h =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 Harvest_Wash = True,
                                 PHS4h = True)

### Pre-Harvest Sampling Intense
#Baseline with intervention. Intense pre-harvest sampling
Baseline_AI_PHSInt =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 Harvest_Wash = True,
                                 PHSInt = True)

### Harvest Sampling Intense
#Baseline with intervention. Intense Harvest sampling
Baseline_AI_H =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 Harvest_Wash = True,
                                 HSTrad = True)

### Receiving Sampling Intense
#Baseline with intervention. Intense Receiving sampling
Baseline_AI_R =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 Harvest_Wash = True,
                                 RSTrad = True)

### FPS Sampling Intense
#Baseline with intervention. Intense Receiving sampling
Baseline_AI_FP =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 Harvest_Wash = True,
                                 FPSTrad = True)



#%% Data analysis

#BASELINE NO INTERVETIONS -------------------------------------------------------

#Creating list of contamination progression
List_of_Progs_NI = [Baseline_NI[1],
                     Baseline_NI_PHS4d[1],
                     Baseline_NI_PHS4h[1],
                     Baseline_NI_PHSInt[1],
                     Baseline_NI_H[1],
                     Baseline_NI_R[1],
                     Baseline_NI_FP[1]
                     ]

L_FC_NI = [x["Final Product Facility"] for x in List_of_Progs_NI]
Column_Names_L_FC_NI = "BaselineNI PHS4D PHS4H PHSInt HTrad RSTrad FPSTrad".split()


FC_NI = pd.concat(L_FC_NI, axis = 1)
FC_NI.columns = Column_Names_L_FC_NI
FC_NI_melted = FC_NI.melt()

#Catplot
H=sns.catplot(x="variable", y="value", kind = "bar" ,
            data=FC_NI_melted)
plt.xlabel("Intervention")
plt.ylabel("Total CFUs at Finished Product")
plt.yscale('log')
plt.title("CFU Final Contamination: Baseline No INterventions")
plt.xticks(rotation=70)


L_FC_NI_Mean_CI= [mean_CI_ONE(x) for x in L_FC_NI]


Reduction_L_FC_NI = Calc_red(meanCI =L_FC_NI_Mean_CI,treatments= 7)

reduction_DF_L_FC_NI = pd.DataFrame({"Treatment": Column_Names_L_FC_NI,
                             "Reduction": Reduction_L_FC_NI} )

reduction_DF_L_FC_NI=reduction_DF_L_FC_NI.sort_values('Reduction',ascending=False).reset_index()
#reduction_DF_L_FC_NI=reduction_DF_L_FC_NI[:6]

chart = sns.barplot(data = reduction_DF_L_FC_NI, x = "Treatment", y = "Reduction", order=reduction_DF_L_FC_NI['Treatment'])
chart.bar_label(chart.containers[0])
plt.xlabel("Intervention")
plt.ylabel("Percent Reduction from Baseline NI")
#plt.ylim(0.995,1)



NI_PH4d_RE=Baseline_NI_PHS4d[0]
NI_PH4h_RE=Baseline_NI_PHS4h[0]
NI_PHSInt_RE=Baseline_NI_PHSInt[0]
NI_HSTrad_RE=Baseline_NI_H[0]
NI_RSTrad_RE=Baseline_NI_R[0]
NI_FPSTrad_RE=Baseline_NI_FP[0]


len(NI_PH4d_RE[(NI_PH4d_RE["PH_CFU_Acc"]>0) | (NI_PH4d_RE["PH_CFU_Rej"]>0) ])
len(NI_PH4d_RE[ (NI_PH4d_RE["PH_CFU_Rej"]>0) ])

Before_PHS4d=Baseline_NI_PHS4d[1]["Bef Pre-Harvest Samp"]
Before_PHS4d[Before_PHS4d>0].describe()


NI_PH4h_RE[(NI_PH4h_RE["PH_CFU_Acc"]>0) | (NI_PH4h_RE["PH_CFU_Rej"]>0) ]
NI_PH4h_RE[ (NI_PH4h_RE["PH_CFU_Rej"]>0) ]

Before_PHS4h=Baseline_NI_PHS4h[1]["Bef Pre-Harvest Samp"]
Before_PHS4h[Before_PHS4h>0].describe()


NI_PHSInt_RE[(NI_PHSInt_RE["PH_CFU_Acc"]>0) | (NI_PHSInt_RE["PH_CFU_Rej"]>0) ]
NI_PHSInt_RE[ (NI_PHSInt_RE["PH_CFU_Rej"]>0) ]

Before_PHSInt=Baseline_NI_PHSInt[1]["Bef Pre-Harvest Samp"]
Before_PHSInt[Before_PHSInt>0].describe()


NI_HSTrad_RE[(NI_HSTrad_RE["H_CFU_Acc"]>0) | (NI_HSTrad_RE["H_CFU_Rej"]>0) ]
NI_HSTrad_RE[ (NI_HSTrad_RE["H_CFU_Rej"]>0) ]

Before_HS=Baseline_NI_H[1]["Bef Harvest Samp"]
Before_HS[Before_HS>0].describe()


NI_RSTrad_RE[(NI_RSTrad_RE["R_CFU_Acc"]>0) | (NI_RSTrad_RE["R_CFU_Rej"]>0) ]
NI_RSTrad_RE[ (NI_RSTrad_RE["R_CFU_Rej"]>0) ]

Before_R=Baseline_NI_R[1]["Bef Receiving Samp"]
Before_R[Before_R>0].describe()



NI_FPSTrad_RE[(NI_FPSTrad_RE["FP_CFU_Acc"]>0) | (NI_FPSTrad_RE["FP_CFU_Rej"]>0) ]
NI_FPSTrad_RE[ (NI_FPSTrad_RE["FP_CFU_Rej"]>0) ]

Before_FPS=Baseline_NI_FP[1]["Bef Final Prod S"]
Before_FPS[Before_FPS>0].describe()




#### BASELINE INTERVETION-------------------------------------------------------------------------------

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
List_of_Initial_Cont = [x["Final Product Facility"] for x in List_of_Progs]
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




[mean_CI_ONE(x) for x in List_of_Final_Conts]

pd.DataFrame([mean_CI_ONE(x) for x in List_of_Final_Conts], columns = ["mean", "95% CI"])

[mean_CI_ONE(x) for x in List_of_Final_Rejs]
