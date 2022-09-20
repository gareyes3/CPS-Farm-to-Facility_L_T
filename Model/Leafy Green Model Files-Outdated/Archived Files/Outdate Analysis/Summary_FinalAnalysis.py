# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 10:19:20 2021

@author: gareyes3
"""


#%%
import sys, os
sys.path
#sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model')
sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility\Model')

# %%
from importlib import reload
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



# %% BAseline Sampling:
# Contamination Challenges
ContCondz.Background_C = True
ContCondz.Point_Source_C = False
ContCondz.Systematic_C = False

# Harvester Contamination
ContCondz.Crew_C = False
ContCondz.Harvester_C = False

# Processing equipment
ContCondz.PE_C = False
ContCondz.PE_Cont_Loc = False,  # 1,2,3,4,5
# 1 = Shredder, #2 = Belt, #3 = Washing, #4 Shaker, #5Centrifuge
ContCondz.Pack_C = False


# %% Pre-Harvest- Comparing Hazard Level and Sample Size
#%%
#Tuning Parameter SampleSize and Hazard Level

Tuning_SampleSize = [60,120,300,600,1200] #list(range(100,1200,200))
Tuning_HazardLevel = list(range(10000,200000+1,10000))#[4536,45360,453600,4536000]#list(range(10000,130000,10000))
Tuning_Grab_number = [1,60,120,320]

Desired_Outputs = ["PH_CFU_PerR", "PH_Wei_PerR"""]
Output_Collection_List = [] #First Index
for i in Tuning_SampleSize:
    Hazard_Level_list = [] #SEcond INdex
    for j in Tuning_HazardLevel:  
        # Sampling Conditions, Baseline all conditions are off
        ScenCondz.Baseline_Sampling = 0  # all others must be 0if this one is 1
        ScenCondz.PH_Sampling = 1
        ScenCondz.H_Sampling = 0
        ScenCondz.R_Sampling = 0
        ScenCondz.FP_Sampling = 0
        # Pre_Harvest 4 Days
        # Pre-Harvest
        ScenCondz.PHS_4d = 1  # Scenario 1
        ScenCondz.PHS_4h = 0  # Scenario 2
        ScenCondz.PHS_Int = 0  # Scenario 3
        
        reload(SCInputz)  # Reload Inputz
        reload(Listz)  # ReUPdate Lists
        
        
        SCInputz.sample_size_PH = i
        SCInputz.BGHazard_lvl = j
        #SCInputz.No_Grabs_PH = 
        
        Main_Mod_Outs = MainModel3z.F_MainLoop()
        OutputDF = Main_Mod_Outs[1]
        ProgDF = Main_Mod_Outs[0]
        
        DF= OutFunz.F_Output_get_cols(Outdf = OutputDF , ColNames = Desired_Outputs)
        DF= pd.melt(DF)
        DF["HLev"] = j
        DF["SampSize"] = i
        Hazard_Level_list.append(DF)
    Output_Collection_List.append(Hazard_Level_list)
  
Main_list = []     
for  i in Output_Collection_List  :   
    Combined_df = pd.concat(i)
    Main_list.append(Combined_df )


Main_Combined = pd.concat(Main_list)
Main_Combined_PRej = Main_Combined.loc[Main_Combined['variable'] == "PH_CFU_PerR"]

sns.set_style("darkgrid")
sns.lmplot(x="HLev", y="value", hue="SampSize", data= Main_Combined_PRej,scatter=False)
#sns.lineplot(x="HLev", y="value", hue="SampSize", data= Main_Combined_PRej)
plt.xlabel("Initial Contamination Levels [Total CFU]")
plt.ylabel("Per CFU Rejected by Sampling Plan")
plt.title("Effect of Sample Size at different contamination levels on Probablity of rejection",fontsize=10)
plt.suptitle("Pre-Harvest Sampling 4D -Uniform Contamination",y=1.07, fontsize=18)
plt.xticks(rotation=70)
#plt.xscale('log')

sns.set_style("darkgrid")
sns.catplot(x="HLev", y="value", hue="SampSize", kind= "bar", data= Main_Combined_PRej)
#sns.lineplot(x="HLev", y="value", hue="SampSize", data= Main_Combined_PRej)
plt.xlabel("Initial Contamination Levels [Total CFU]")
plt.ylabel("Per CFU Rejected by Sampling Plan")
plt.title("Effect of Sample Size at different contamination levels on Probablity of rejection",fontsize=10)
plt.suptitle("Pre-Harvest Sampling 4D -Uniform Contamination",y=1.07, fontsize=18)
plt.xticks(rotation=70)
#plt.xscale('log')



#%% Pre-Harvest -Comparing Number of Grabs and Sample Size, Identify Major Driver. Unform Contamination
#%%
#Tuning Parameter SampleSize and Hazard Level

Tuning_SampleSize = [60,120,300,600,1200] #list(range(100,1200,200))
Tuning_HazardLevel = [4536,45360,450360,4503600]#list(range(10000,130000,10000)) #1 CFU/10kg, 1CFU kg, 1CFU/100g, 1CFU/10g. 
Tuning_Grab_number = [1,30,60,120,320]

Desired_Outputs = ["PH_CFU_PerR", "PH_Wei_PerR"""]
Output_Collection_List = [] #First Index
for i in Tuning_SampleSize:
    Hazard_Level_list = [] #SEcond INdex
    for j in Tuning_Grab_number:  
        # Sampling Conditions, Baseline all conditions are off
        ScenCondz.Baseline_Sampling = 0  # all others must be 0if this one is 1
        ScenCondz.PH_Sampling = 1
        ScenCondz.H_Sampling = 0
        ScenCondz.R_Sampling = 0
        ScenCondz.FP_Sampling = 0
        # Pre_Harvest 4 Days
        # Pre-Harvest
        ScenCondz.PHS_4d = 1  # Scenario 1
        ScenCondz.PHS_4h = 0  # Scenario 2
        ScenCondz.PHS_Int = 0  # Scenario 3
        
        reload(SCInputz)  # Reload Inputz
        reload(Listz)  # ReUPdate Lists
        
        
        SCInputz.sample_size_PH = i
        #SCInputz.BGHazard_lvl = j
        SCInputz.No_Grabs_PH = j
        
        Main_Mod_Outs = MainModel3z.F_MainLoop()
        OutputDF = Main_Mod_Outs[1]
        ProgDF = Main_Mod_Outs[0]
        
        DF= OutFunz.F_Output_get_cols(Outdf = OutputDF , ColNames = Desired_Outputs)
        DF= pd.melt(DF)
        DF["GrabNo"] = j
        DF["SampSize"] = i
        Hazard_Level_list.append(DF)
    Output_Collection_List.append(Hazard_Level_list)
  
Main_list = []     
for  i in Output_Collection_List  :   
    Combined_df = pd.concat(i)
    Main_list.append(Combined_df )


Main_Combined = pd.concat(Main_list)
Main_Combined_GS_PRej = Main_Combined.loc[Main_Combined['variable'] == "PH_CFU_PerR"]


sns.catplot(x="GrabNo", y="value", hue="SampSize",kind= "bar", data= Main_Combined_GS_PRej)
#sns.lineplot(x="GrabNo", y="value", hue="SampSize", data= Main_Combined_GS_PRej)
plt.xlabel("Number of grabs")
plt.ylabel("Per CFU Rejected by Sampling Plan")
plt.title("Effect of Sample Size and number of grabs Probablity of rejection",fontsize=10)
plt.suptitle("Pre-Harvest Sampling 4D -Uniform Contamination",y=1.07, fontsize=18)

plt.xticks(rotation=70)
plt.ticklabel_format(style='plain', axis='x')

#%% POINT SOURCE- COMPARING NUMBER OF GRABS AND SAMPLE SIZE
# %% Changing to Point Source Contamination
# Contamination Challenges
ContCondz.Background_C = False
ContCondz.Point_Source_C = True
ContCondz.Systematic_C = False

# Harvester Contamination
ContCondz.Crew_C = False
ContCondz.Harvester_C = False

# Processing equipment
ContCondz.PE_C = False
ContCondz.PE_Cont_Loc = False,  # 1,2,3,4,5
# 1 = Shredder, #2 = Belt, #3 = Washing, #4 Shaker, #5Centrifuge
ContCondz.Pack_C = False
# %% Pre-Harvest - Point Source
#Tuning Parameter SampleSize and Hazard Level

Tuning_SampleSize = [60,120,300,600,1200] #list(range(100,1200,200))
Tuning_HazardLevel = [4536,45360,450360,4503600]#list(range(10000,130000,10000)) #1 CFU/10kg, 1CFU kg, 1CFU/100g, 1CFU/10g. 
Tuning_Grab_number = [1,30,60,120,320]

Desired_Outputs = ["PH_CFU_PerR", "PH_Wei_PerR"""]
Output_Collection_List = [] #First Index
for i in Tuning_SampleSize:
    Hazard_Level_list = [] #SEcond INdex
    for j in Tuning_Grab_number:  
        # Sampling Conditions, Baseline all conditions are off
        ScenCondz.Baseline_Sampling = 0  # all others must be 0if this one is 1
        ScenCondz.PH_Sampling = 1
        ScenCondz.H_Sampling = 0
        ScenCondz.R_Sampling = 0
        ScenCondz.FP_Sampling = 0
        # Pre_Harvest 4 Days
        # Pre-Harvest
        ScenCondz.PHS_4d = 1  # Scenario 1
        ScenCondz.PHS_4h = 0  # Scenario 2
        ScenCondz.PHS_Int = 0  # Scenario 3
        
        reload(SCInputz)  # Reload Inputz
        reload(Listz)  # ReUPdate Lists
        
        
        SCInputz.sample_size_PH = i
        #SCInputz.BGHazard_lvl = j
        SCInputz.No_Grabs_PH = j
        
        Main_Mod_Outs = MainModel3z.F_MainLoop()
        OutputDF = Main_Mod_Outs[1]
        ProgDF = Main_Mod_Outs[0]
        
        DF= OutFunz.F_Output_get_cols(Outdf = OutputDF , ColNames = Desired_Outputs)
        DF= pd.melt(DF)
        DF["GrabNo"] = j
        DF["SampSize"] = i
        Hazard_Level_list.append(DF)
    Output_Collection_List.append(Hazard_Level_list)
  
Main_list = []     
for  i in Output_Collection_List  :   
    Combined_df = pd.concat(i)
    Main_list.append(Combined_df )


Main_Combined = pd.concat(Main_list)
Main_Combined_PS_PRej = Main_Combined.loc[Main_Combined['variable'] == "PH_CFU_PerR"]


sns.catplot(x="GrabNo", y="value", hue="SampSize",kind= "bar", data= Main_Combined_PS_PRej)
#sns.lineplot(x="GrabNo", y="value", hue="SampSize", data= Main_Combined_GS_PRej)
plt.xlabel("Number of grabs")
plt.ylabel("Per CFU Rejected by Sampling Plan")
plt.title("Effect of Sample Size and number of grabs Probablity of rejection",fontsize=10)
plt.suptitle("Pre-Harvest Sampling 4D -Point Source Contamination",y=1.07, fontsize=18)

plt.xticks(rotation=70)
plt.ticklabel_format(style='plain', axis='x')


















#%%

def Fun_Out_3param(DesiredOuts, TuningList1, TuningList2, Tuning1Name, Tuning2Name ):
    #DesiredOuts: List of desite outputs from output Dictionary e.g  ["PH_CFU_PerR", "PH_Wei_PerR"""]
    #TunningList1: List of tunning parameters e.g  Tuning_SampleSize = [60,120,300,600,1200] 
    #Tunning List2: List of second tunning samples e.g Tunning_HazardLevel = [1000,10000,100000,1000000]
    #Tuning1in: SCINputz, parameter that will be changed  eg  SCInputz.sample_size_PH
    #Tunin2in: SCINputz, parameter that will be changed  eg  SCInputz.BGHazard_lvl
    #Tuning1Name: str, "SampleSize"
    #Tuning2Name: srt, "HazardLevel"
    for i in TuningList1: 
        Hazard_Level_list = [] #SEcond INdex
        for j in TuningList2:  
            # Sampling Conditions, Baseline all conditions are off
            ScenCondz.Baseline_Sampling = 0  # all others must be 0if this one is 1
            ScenCondz.PH_Sampling = 1
            ScenCondz.H_Sampling = 0
            ScenCondz.R_Sampling = 0
            ScenCondz.FP_Sampling = 0
            # Pre_Harvest 4 Days
            # Pre-Harvest
            ScenCondz.PHS_4d = 1  # Scenario 1
            ScenCondz.PHS_4h = 0  # Scenario 2
            ScenCondz.PHS_Int = 0  # Scenario 3
            
            reload(SCInputz)  # Reload Inputz
            reload(Listz)  # ReUPdate Lists
            
            
            SCInputz.sample_size_PH = i
            SCInputz.BGHazard_lvl = j
            
            Main_Mod_Outs = MainModel3z.F_MainLoop()
            OutputDF = Main_Mod_Outs[1]
            ProgDF = Main_Mod_Outs[0]
            
            DF= OutFunz.F_Output_get_cols(Outdf = OutputDF , ColNames = DesiredOuts)
            DF= pd.melt(DF)
            DF[Tuning1Name] = i
            DF [Tuning2Name] = j
            Hazard_Level_list.append(DF)
        Output_Collection_List.append(Hazard_Level_list)
        return Output_Collection_List



#Conditions

def Condition_Selection(Methods,submethod):
    if "PH" in Methods:
       ScenCondz.PH_Sampling = 1
       if "4d" in submethod:
           ScenCondz.PHS_4d = 1
       elif "4h" in submethod:
           ScenCondz.PHS_4h = 1
       elif "Int" in submethod:
           ScenCondz.PHS_Int = 1
    elif "H" in Methods:
        ScenCondz.H_Sampling = 1
        if "HS Trad" in submethods:
            ScenCondz.PH_Tread = 1
        elif "HS Agg" in 
           
       
        
    
