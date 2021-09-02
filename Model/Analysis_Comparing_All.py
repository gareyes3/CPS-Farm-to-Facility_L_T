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
import seaborn as sns
from matplotlib import pyplot as plt

#Own Libraries
import Funz
import ContScen
import Listz 
import OutFunz
import InFunz
import ScenCondz
import ContCondz
import Inputz
from importlib import reload 

#Main Model Loops
import MainModel3z

#%% 
#Progression DataFrame. 
Progression_DFS = []
#%% BAseline Sampling: 
#Contamination Challenges
ContCondz.Background_C=0
ContCondz.Point_Source_C=0
ContCondz.Systematic_C=1

#Harvester Contamination
ContCondz.Crew_C = 0
ContCondz.Harvester_C = 0

#Processing equipment
ContCondz.PE_C = 0
ContCondz.PE_Cont_Loc = 0,#1,2,3,4,5
#1 = Shredder, #2 = Belt, #3 = Washing, #4 Shaker, #5Centrifuge
ContCondz.Pack_C= 0

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


#Weight Rejected, Weight Accepted. 
L_Final_PerRejWeight = {
                'PH4d':D_PH4d["PerRejectedWeight"],
                'PH4h':D_PH4h["PerRejectedWeight"],
                'PHInt':D_PHInt["PerRejectedWeight"],
                'HTrad':D_HTrad["PerRejectedWeight"],
                'HAgg':D_HAgg["PerRejectedWeight"],
                'R':D_R["PerRejectedWeight"],
                'FPTrad':D_FPSTrad["PerRejectedWeight"],
                'FPAgg':D_FPSAgg["PerRejectedWeight"],
          }

df_L_Final_PerRejWeight = pd.DataFrame(L_Final_PerRejWeight)
df_L_Final_PerRejWeight_melted = pd.melt(df_L_Final_PerRejWeight)


#Scenariosplot =sns.catplot(x="variable", y="value", data=df_L_Final_Per_melted ,kind="bar",  height=4, aspect=2 )
Scenariosplot =sns.boxplot(x="variable", y="value", data=df_L_Final_PerRejWeight_melted )
plt.xlabel("Sampling Type")
plt.ylabel("Percentage total lb. Rejected at Sampling Step")

#TotalWeightRejected
#Weight Rejected, Weight Accepted. 
L_Final_RejWeight = {
                'PH4d':D_PH4d["Total_Weight_R"],
                'PH4h':D_PH4h["Total_Weight_R"],
                'PHInt':D_PHInt["Total_Weight_R"],
                'HTrad':D_HTrad["Total_Weight_R"],
                'HAgg':D_HAgg["Total_Weight_R"],
                'R':D_R["Total_Weight_R"],
                'FPTrad':D_FPSTrad["Total_Weight_R"],
                'FPAgg':D_FPSAgg["Total_Weight_R"],
          }

df_L_Final_RejWeight = pd.DataFrame(L_Final_RejWeight)
df_L_Final_RejWeight_melted = pd.melt(df_L_Final_RejWeight)


#Scenariosplot =sns.catplot(x="variable", y="value", data=df_L_Final_Per_melted ,kind="bar",  height=4, aspect=2 )
Scenariosplot =sns.boxplot(x="variable", y="value", data=df_L_Final_RejWeight_melted )
plt.xlabel("Sampling Type")
plt.ylabel("Total lb. Rejected due to sampling")


#Weight Rejected, Weight Accepted Compariason 
L_Final_PerRatio = {
                'PH4d':D_PH4d["PerRejectedWeight"] /D_PH4d["PerRejected at PH"] ,
                'PH4h':D_PH4h["PerRejectedWeight"] /D_PH4h["PerRejected at PH"] ,
                'PHInt':D_PHInt["PerRejectedWeight"] /D_PHInt["PerRejected at PH"] ,
                'HTrad':D_HTrad["PerRejectedWeight"] /D_HTrad["PerRejected at H"] ,
                'HAgg':D_HAgg["PerRejectedWeight"] /D_HAgg["PerRejected at H"] ,
                'R':D_R["PerRejectedWeight"] /D_R["PerRejected at R"] ,
                'FPTrad':D_FPSTrad["PerRejectedWeight"] /D_FPSTrad["PerRejected at FP"] ,
                'FPAgg':D_FPSAgg["PerRejectedWeight"] / D_FPSAgg["PerRejected at FP"],
          }

df_L_Final_PerRatio = pd.DataFrame(L_Final_PerRatio)
df_L_Final_PerRatio_melted = pd.melt(df_L_Final_PerRatio)


#Scenariosplot =sns.catplot(x="variable", y="value", data=df_L_Final_Per_melted ,kind="bar",  height=4, aspect=2 )
Scenariosplot =sns.boxplot(x="variable", y="value", data=df_L_Final_PerRatio_melted )
plt.xlabel("Sampling Type")
plt.ylabel("Percentage lb Rejected/  Percentage CFU Rejected")


#Combined Data PEr Rejected and per Lb Rejected. 
Percentage_Rejected = df_L_Final_Per_melted
Percentage_Rejected['Type'] = "Proportion of CFU Rejected"

Percentage_lb_Rejected = df_L_Final_PerRejWeight_melted
Percentage_lb_Rejected['Type'] = "Proportion of lb Rejected"

Combined_Percentages =  pd.concat([Percentage_Rejected,
                          Percentage_lb_Rejected])
sns.set(style="darkgrid")
Scenariosplot =sns.lineplot(x="variable", y="value", hue = "Type", data=Combined_Percentages)
plt.xlabel("Sampling Scenario")
plt.ylabel("Proportion Rejection")
Scenariosplot.legend_.set_title('Type')
# Put the legend out of the figure
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)




Combined_Percentages_Dif = Percentage_Rejected["value"] - Percentage_lb_Rejected["value"]
Combined_Percentages_Dif=pd.DataFrame(Combined_Percentages_Dif)
Combined_Percentages_Dif["Type"] = Percentage_Rejected['variable']

sns.set(style="darkgrid")
Scenariosplot =sns.lineplot(x="Type", y="value",  data=Combined_Percentages_Dif)
plt.xlabel("Sampling Scenario")
plt.ylabel("Change Prop CFU Rej & Prop Lb Rejc ")



Scenariosplot =sns.boxplot(x="variable", y="value", hue = "Type", data=Combined_Percentages)
plt.xlabel("Sampling Scenario")
plt.ylabel("Proportion Rejection")
Scenariosplot.legend_.set_title('Type')


#Conbined Per Rejected CFU and lb Rejectet

Percentage_Rejected = df_L_Final_Per_melted
Percentage_Rejected['Type'] = "Percentage CFU Rejected"

Total_lb_Rejected = df_L_Final_RejWeight_melted
Total_lb_Rejected['Type'] = "Total lb Rejected"

Combined_PerCFUTotalWeight =  Percentage_Rejected
Combined_PerCFUTotalWeight['value2'] = Total_lb_Rejected['value']






