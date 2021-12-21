# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 09:12:08 2021

@author: gareyes3
"""
#%%
import sys, os
sys.path
sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model')
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


reload(MainModel3z)
reload(Inputz)
#%%

#Scenarios Creation
#Systematic Failure from irrigation. 100% of field affected at 1CFU/g 

# 1 CFU/lb Contmination Level
One_CFU_lb = 100000 #CFUs

#Uniform Contmaination in the Field. 
# Contamination Challenges
ContCondz.Background_C = True
ContCondz.Point_Source_C =False
ContCondz.Systematic_C = False

# Harvester Contamination
ContCondz.Crew_C = False
ContCondz.Harvester_C = False

# Processing equipment
ContCondz.PE_C = False
ContCondz.PE_Cont_Loc = False,  # 1,2,3,4,5
# 1 = Shredder, #2 = Belt, #3 = Washing, #4 Shaker, #5Centrifuge
ContCondz.Pack_C = False


#%% Scenario 1. No intervention Strategies, Natural Field and No Washing. 

reload(SCInputz)  # Reload Inputz
reload(Listz)  # Reload Lists

#Management of Control: 

#Holding Time: 
ScenCondz.Holding_Time= False #0,4,8 Holding Time

#Turning off Pre-Cooling
SCInputz.Pre_CoolingYN = False 

# Turning of Washing. 
SCInputz.Washing_YN = False 

#Harvest Pre-Wash: 
SCInputz.C_Spray_HYN =False

SCInputz.BGHazard_lvl = One_CFU_lb
'''
SCInputz.PSHazard_lvl = One_CFU_g  #CFU # background contamination
SCInputz.PSCluster_Size = 1000 #lb 1%
SCInputz.PSNo_Cont_Clusters = 1 #4 1 1% Cluster
'''
#Sampling Condition
# Sampling Conditions, Baseline all conditions are off
ScenCondz.Baseline_Sampling = 0  # all others must be 0if this one is 1
ScenCondz.PH_Sampling = 0
ScenCondz.H_Sampling = 0
ScenCondz.R_Sampling = 0
ScenCondz.FP_Sampling = 0
# Pre_Harvest 4 Days
ScenCondz.PHS_4d = 0  # Scenario 1
ScenCondz.PHS_4h = 0  # Scenario 2
ScenCondz.PHS_Int = 0  # Scenario 3


#Running The Model.
Main_Mod_Outs = MainModel3z.F_MainLoop()

#Getting the outputs from the function.
OutputDF = Main_Mod_Outs[1]
ProgDF = Main_Mod_Outs[0]
PropProgDF = Main_Mod_Outs[2]
FinalConts = Main_Mod_Outs[6]

#Final Contmination Baseline Scenario
Final_CFU_Baseline =ProgDF["Final Product Facility"]

#Final Prop Contaminated
Final_Prop_Baseline = PropProgDF["PropCont_A_FP"]

#Creating boxplot for exploration
plt.boxplot(Final_CFU_Baseline)
plt.ticklabel_format(style='plain', axis='y')

#Percent Reduction by System Initial vs Final
(One_CFU_lb-Final_CFU_Baseline.mean())/One_CFU_lb #Average Reduction. 

#%% Scenario 2. No Sampling, Only Intervention Strategy is Washing

reload(SCInputz)  # Reload Inputz
reload(Listz)  # Reload Lists

#Holding Time: 
ScenCondz.Holding_Time= False #Defaults to 1 Day holding Time

#Turning off Pre-Cooling
SCInputz.Pre_CoolingYN = False 

# Turning of Washing. 
SCInputz.Washing_YN = True

#Harvest Pre-Wash: 
SCInputz.C_Spray_HYN =False


SCInputz.BGHazard_lvl = One_CFU_lb
'''
SCInputz.PSHazard_lvl = One_CFU_lb  #CFU # background contamination
SCInputz.PSCluster_Size = 1000 #lb 1%
SCInputz.PSNo_Cont_Clusters = 1 #4 1 1% Cluster
'''
#Sampling Condition
# Sampling Conditions, Baseline all conditions are off
ScenCondz.Baseline_Sampling = 0  # all others must be 0if this one is 1
ScenCondz.PH_Sampling = 0
ScenCondz.H_Sampling = 0
ScenCondz.R_Sampling = 0
ScenCondz.FP_Sampling = 0
# Pre_Harvest 4 Days
ScenCondz.PHS_4d = 0  # Scenario 1
ScenCondz.PHS_4h = 0  # Scenario 2
ScenCondz.PHS_Int = 0  # Scenario 3


#Running The Model.
Main_Mod_Outs = MainModel3z.F_MainLoop()

#Getting the outputs from the function.
OutputDF_Base_Wash = Main_Mod_Outs[1]
ProgDF_Base_Wash = Main_Mod_Outs[0]
PropProgDF_Base_Wash = Main_Mod_Outs[2]
FinalConts_Base_Wash = Main_Mod_Outs[6]

#Final Contmination Baseline Scenario
Final_CFU_Base_Wash =ProgDF_Base_Wash["Final Product Facility"]
#Final Prop Contaminated
Final_Prop_Base_Wash = PropProgDF_Base_Wash["PropCont_A_FP"]

#Creating boxplot for exploration
plt.boxplot(Final_CFU_Base_Wash)
plt.ticklabel_format(style='plain', axis='y')

#Percent Reduction by System Initial vs Final
(One_CFU_lb-Final_CFU_Base_Wash.mean())/One_CFU_lb #Average Reduction.

#%% Scenario 3 PH Sampling 4D, Washing off , and normal baseline contamination reduction
    #PH Sample: 1 Sample/Sublot, 
    #Rejection Rule: "Lot
    #Sample Mass: 365g per sublot
    # GRabs per Sublot = N60

reload(SCInputz)  # Reload Inputz
reload(Listz)  # Reload Lists

#Holding Time: 
ScenCondz.Holding_Time= False #Defaults to 1 Day holding Time

#Turning off Pre-Cooling
SCInputz.Pre_CoolingYN = False 

# Turning of Washing. 
SCInputz.Washing_YN = False #Defaults

#Harvest Pre-Wash: 
SCInputz.C_Spray_HYN =False


SCInputz.BGHazard_lvl = One_CFU_lb
'''
SCInputz.PSHazard_lvl = One_CFU_lb  #CFU # background contamination
SCInputz.PSCluster_Size = 1000 #lb 1%
SCInputz.PSNo_Cont_Clusters = 1 #4 1 1% Cluster
'''

#Sampling Condition
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
   
#Only on when sampling,
SCInputz.test_unit_PH = "Sublot"
SCInputz.sample_size_PH = 375 # (Input) g #Sample Size in grams for Pre Harvest
SCInputz.n_samples_slot_PH = 1 # (Input) Samples per sublot of product
SCInputz.No_Grabs_PH = 60
SCInputz.Limit_PH = 0
SCInputz.RR_PH_Trad = "Sublot" #Reject by Sublot


#Running The Model.
Main_Mod_Outs = MainModel3z.F_MainLoop()

#Getting the outputs from the function.
OutputDF_Base_PHS4d = Main_Mod_Outs[1]
ProgDF_Base_PHS4d = Main_Mod_Outs[0]
PropProgDF_Base_PHS4d = Main_Mod_Outs[2]
FinalConts_Base_PHS4d = Main_Mod_Outs[6]

#Final Contmination Baseline Scenario
Final_CFU_Base_PHS4d =ProgDF_Base_PHS4d["Final Product Facility"]

#Final Prop Contaminated
Final_Prop_Base_PHS4d = PropProgDF_Base_PHS4d["PropCont_A_FP"]

#Creating boxplot for exploration
plt.boxplot(Final_CFU_Base_PHS4d)
plt.ticklabel_format(style='plain', axis='y')

#Percent Reduction by System Initial vs Final
(One_CFU_lb-Final_CFU_Base_PHS4d.mean())/One_CFU_lb #Average Reduction.

#%%
#Scenario 4 Holding Time on Everything Else Off

reload(SCInputz)  # Reload Inputz
reload(Listz)  # Reload Lists

#Holding Time: 
ScenCondz.Holding_Time= True #Defaults to 1 Day holding Time

#Turning off Pre-Cooling
SCInputz.Pre_CoolingYN = False 

# Turning of Washing. 
SCInputz.Washing_YN = False

#Harvest Pre-Wash: 
SCInputz.C_Spray_HYN =False


SCInputz.BGHazard_lvl = One_CFU_lb
'''
SCInputz.PSHazard_lvl = One_CFU_lb  #CFU # background contamination
SCInputz.PSCluster_Size = 1000 #lb 1%
SCInputz.PSNo_Cont_Clusters = 1 #4 1 1% Cluster
'''
#Sampling Condition
# Sampling Conditions, Baseline all conditions are off
ScenCondz.Baseline_Sampling = 0  # all others must be 0if this one is 1
ScenCondz.PH_Sampling = 0
ScenCondz.H_Sampling = 0
ScenCondz.R_Sampling = 0
ScenCondz.FP_Sampling = 0
# Pre_Harvest 4 Days
ScenCondz.PHS_4d = 0  # Scenario 1
ScenCondz.PHS_4h = 0  # Scenario 2
ScenCondz.PHS_Int = 0  # Scenario 3


#Running The Model.
Main_Mod_Outs = MainModel3z.F_MainLoop()

#Getting the outputs from the function.
OutputDF_Base_Holding = Main_Mod_Outs[1]
ProgDF_Base_Holding = Main_Mod_Outs[0]
PropProgDF_Base_Holding = Main_Mod_Outs[2]
FinalConts_Base_Holding = Main_Mod_Outs[6]

#Final Contmination Baseline Scenario
Final_CFU_Base_Holding =ProgDF_Base_Holding["Final Product Facility"]
#Final Prop Contaminated
Final_Prop_Base_Holding = PropProgDF_Base_Holding["PropCont_A_FP"]

#Creating boxplot for exploration
plt.boxplot(Final_CFU_Base_Holding)
plt.ticklabel_format(style='plain', axis='y')

#Percent Reduction by System Initial vs Final
(One_CFU_lb-Final_CFU_Base_Holding.mean())/One_CFU_lb #Average Reduction.


#%%
#Scenario #5 Only Intervention if Pre-Cooling

reload(SCInputz)  # Reload Inputz
reload(Listz)  # Reload Lists

#Holding Time: 
ScenCondz.Holding_Time= False#Defaults to 1 Day holding Time

#Turning off Pre-Cooling
SCInputz.Pre_CoolingYN =True

# Turning of Washing. 
SCInputz.Washing_YN = False

#Harvest Pre-Wash: 
SCInputz.C_Spray_HYN =False


SCInputz.BGHazard_lvl = One_CFU_lb
'''
SCInputz.PSHazard_lvl = One_CFU_lb  #CFU # background contamination
SCInputz.PSCluster_Size = 1000 #lb 1%
SCInputz.PSNo_Cont_Clusters = 1 #4 1 1% Cluster
'''
#Sampling Condition
# Sampling Conditions, Baseline all conditions are off
ScenCondz.Baseline_Sampling = 0  # all others must be 0if this one is 1
ScenCondz.PH_Sampling = 0
ScenCondz.H_Sampling = 0
ScenCondz.R_Sampling = 0
ScenCondz.FP_Sampling = 0
# Pre_Harvest 4 Days
ScenCondz.PHS_4d = 0  # Scenario 1
ScenCondz.PHS_4h = 0  # Scenario 2
ScenCondz.PHS_Int = 0  # Scenario 3


#Running The Model.
Main_Mod_Outs = MainModel3z.F_MainLoop()

#Getting the outputs from the function.
OutputDF_Base_Precool = Main_Mod_Outs[1]
ProgDF_Base_Precool = Main_Mod_Outs[0]
PropProgDF_Base_Precool = Main_Mod_Outs[2]
FinalConts_Base_Precool = Main_Mod_Outs[6]

#Final Contmination Baseline Scenario
Final_CFU_Base_Precool =ProgDF_Base_Precool["Final Product Facility"]
#Final Prop Contaminated
Final_Prop_Base_Precool = PropProgDF_Base_Precool["PropCont_A_FP"]

#Creating boxplot for exploration
plt.boxplot(Final_CFU_Base_Precool)
plt.ticklabel_format(style='plain', axis='y')

#Percent Reduction by System Initial vs Final
(One_CFU_lb-Final_CFU_Base_Precool.mean())/One_CFU_lb #Average Reduction.


#%%
#Scenario #6 Only Intervention if Pre-Harvest SprayWash

reload(SCInputz)  # Reload Inputz
reload(Listz)  # Reload Lists

#Holding Time: 
ScenCondz.Holding_Time= False#Defaults to 1 Day holding Time

#Turning off Pre-Cooling
SCInputz.Pre_CoolingYN =False
# Turning of Washing. 
SCInputz.Washing_YN = False

#Harvest Pre-Wash: 
SCInputz.C_Spray_HYN =True


SCInputz.BGHazard_lvl = One_CFU_lb
'''
SCInputz.PSHazard_lvl = One_CFU_lb  #CFU # background contamination
SCInputz.PSCluster_Size = 1000 #lb 1%
SCInputz.PSNo_Cont_Clusters = 1 #4 1 1% Cluster
'''
#Sampling Condition
# Sampling Conditions, Baseline all conditions are off
ScenCondz.Baseline_Sampling = 0  # all others must be 0if this one is 1
ScenCondz.PH_Sampling = 0
ScenCondz.H_Sampling = 0
ScenCondz.R_Sampling = 0
ScenCondz.FP_Sampling = 0
# Pre_Harvest 4 Days
ScenCondz.PHS_4d = 0  # Scenario 1
ScenCondz.PHS_4h = 0  # Scenario 2
ScenCondz.PHS_Int = 0  # Scenario 3


#Running The Model.
Main_Mod_Outs = MainModel3z.F_MainLoop()

#Getting the outputs from the function.
OutputDF_Base_Prewash = Main_Mod_Outs[1]
ProgDF_Base_Prewash = Main_Mod_Outs[0]
PropProgDF_Base_Prewash = Main_Mod_Outs[2]
FinalConts_Base_Prewash = Main_Mod_Outs[6]

#Final Contmination Baseline Scenario
Final_CFU_Base_Prewash =ProgDF_Base_Prewash["Final Product Facility"]
#Final Prop Contaminated
Final_Prop_Base_Prewash = PropProgDF_Base_Prewash["PropCont_A_FP"]

#Creating boxplot for exploration
plt.boxplot(Final_CFU_Base_Prewash)
plt.ticklabel_format(style='plain', axis='y')

#Percent Reduction by System Initial vs Final
(One_CFU_lb-Final_CFU_Base_Prewash.mean())/One_CFU_lb #Average Reduction.

#%% Scenario 7 PH Sampling 4D, Washing ON ,Pre-cooling on and everything else on and normal baseline contamination reduction
    #PH Sample: 1 Sample/Sublot, 
    #Rejection Rule: "Lot
    #Sample Mass: 365g per sublot
    # GRabs per Sublot = N60

reload(SCInputz)  # Reload Inputz
reload(Listz)  # Reload Lists

#Holding Time: 
ScenCondz.Holding_Time= True#Defaults to 1 Day holding Time

#Turning off Pre-Cooling
SCInputz.Pre_CoolingYN =True

# Turning of Washing. 
SCInputz.Washing_YN = True

#Harvest Pre-Wash: 
SCInputz.C_Spray_HYN =True

SCInputz.BGHazard_lvl = One_CFU_lb
'''
SCInputz.PSHazard_lvl = One_CFU_lb  #CFU # background contamination
SCInputz.PSCluster_Size = 1000 #lb 1%
SCInputz.PSNo_Cont_Clusters = 1 #4 1 1% Cluster
'''

#Sampling Condition
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
   
#Only on when sampling,
SCInputz.test_unit_PH = "Sublot"
SCInputz.sample_size_PH = 375 # (Input) g #Sample Size in grams for Pre Harvest
SCInputz.n_samples_slot_PH = 1 # (Input) Samples per sublot of product
SCInputz.No_Grabs_PH = 60
SCInputz.Limit_PH = 0
SCInputz.RR_PH_Trad = "Sublot" #Reject by Sublot


#Running The Model.
Main_Mod_Outs = MainModel3z.F_MainLoop()

#Getting the outputs from the function.
OutputDF_All = Main_Mod_Outs[1]
ProgDF_All = Main_Mod_Outs[0]
PropProgDF_All = Main_Mod_Outs[2]
FinalConts_All = Main_Mod_Outs[6]

#Final Contmination Baseline Scenario
Final_CFU_All =ProgDF_All["Final Product Facility"]
#Final Prop Contaminated
Final_Prop_All = PropProgDF_All["PropCont_A_FP"]

#Creating boxplot for exploration
plt.boxplot(Final_CFU_All)
plt.ticklabel_format(style='plain', axis='y')

#Percent Reduction by System Initial vs Final
(One_CFU_lb-Final_CFU_All.mean())/One_CFU_lb #Average Reduction.

#%%



#%%
#Comparing Scenarios for Final contamination 

#Adding Types To merge
Final_CFU_Baseline = Final_CFU_Baseline.to_frame()
Final_CFU_Baseline["Type"] = "Baseline"
A = Final_CFU_Baseline["Final Product Facility"]


Final_CFU_Base_Wash = Final_CFU_Base_Wash.to_frame()
Final_CFU_Base_Wash["Type"] = "Baseline, Wash"
B = Final_CFU_Base_Wash["Final Product Facility"]

Final_CFU_Base_PHS4d=Final_CFU_Base_PHS4d.to_frame()
Final_CFU_Base_PHS4d["Type"] = "Baseline, Sampling"
C = Final_CFU_Base_PHS4d["Final Product Facility"]


Final_CFU_Base_Holding=Final_CFU_Base_Holding.to_frame()
Final_CFU_Base_Holding["Type"] = "Baseline, Holding"
D = Final_CFU_Base_Holding["Final Product Facility"]


Final_CFU_Base_Precool=Final_CFU_Base_Precool.to_frame()
Final_CFU_Base_Precool["Type"] = "Baseline, Pre-Cool"
E = Final_CFU_Base_Precool["Final Product Facility"]


Final_CFU_Base_Prewash=Final_CFU_Base_Prewash.to_frame()
Final_CFU_Base_Prewash["Type"] = "Baseline, Harvest Wash"
F = Final_CFU_Base_Prewash["Final Product Facility"]

Final_CFU_All = Final_CFU_All.to_frame()
Final_CFU_All["Type"] = "All Interventions"
Z = Final_CFU_All["Final Product Facility"]

#Initial 
Initial_CFU_V  = [One_CFU_lb]
Initial_CFU_V=pd.DataFrame(Initial_CFU_V, columns = ["Final Product Facility"])
Initial_CFU_V["Type"] = "Initial Levels"

#Combining them
Final_Compared=pd.concat([#Initial_CFU_V,
                          Final_CFU_Baseline, 
                          Final_CFU_Base_Wash,
                          Final_CFU_Base_PHS4d,
                          Final_CFU_Base_Holding,
                          Final_CFU_Base_Precool,
                          Final_CFU_Base_Prewash,
                          Final_CFU_All], 
                         axis=0, 
                         ignore_index=True)



#Initial levels represent the initial contamination level before or after PH

    #2-8 days before harvest. Triangular distribution.     
H=sns.catplot(x="Type", y="Final Product Facility", 
            data=Final_Compared)
#H.map(sns.swarmplot, 'Type', 'Final Product Facility', color='k')
plt.xlabel("Sampling Scenario")
plt.ylabel("Total CFUs")
plt.title("CFUs Initial vs Strategies")
plt.xticks(rotation=70)

H=sns.catplot(x="Type", y="Final Product Facility", kind = "bar" ,
            data=Final_Compared)
plt.xlabel("Sampling Scenario")
plt.ylabel("Total CFUs")
plt.title("CFUs Initial vs Strategies")
plt.xticks(rotation=70)

#Desnity Plots for Final Contamination. 
#g = sns.FacetGrid(Final_Compared, col="Type", col_wrap=3)
#g.map_dataframe(sns.histplot, x="Final Product Facility")


h=sns.displot( data =Final_Compared, 
            x = "Final Product Facility" , 
            col = "Type", 
            col_wrap=3,
             stat = "probability",
             bins = 30,
            facet_kws=dict(sharey=False,sharex= False))
plt.suptitle("Distribution of CFUs in Final Product",) 

def specs(x, **kwargs):
    plt.axvline(x.mean(), c='red', ls='-', lw=2.5)
    plt.axvline(x.median(), c='orange', ls='--', lw=2.5)

h.map(specs,"Final Product Facility" )


#sns.displot(Final_Compared, x="Final Product Facility", col="Type", kind="kde", common_norm=False, col_wrap=3)

#Statistical analysis. 
from scipy import stats
import scikit_posthocs as sp
stats.kruskal(A,B,C,D,E,F,Z)
data = [A,B,C,D,E,F,Z]
sp.posthoc_dunn(data, p_adjust = 'bonferroni')  

#%%
#Percent Contaminated at each stage. 
#Adding Types To merge
Final_Prop_Baseline = Final_Prop_Baseline.to_frame()
Final_Prop_Baseline["Type"] = "No Sampling, No Wash"
x_prp = Final_Prop_Baseline["PropCont_A_FP"]

#totalcontaminated pakages
x_totCont = PropProgDF["TotalCont_A_FP"].to_frame()
x_totCont["Type"] = "No Sampling, No Wash"

#-------------

Final_Prop_Base_Wash = Final_Prop_Base_Wash.to_frame()
Final_Prop_Base_Wash["Type"] = "No Sampling, Wash"
y_prp = PropProgDF_Base_Wash["PropCont_A_FP"]

y_totCont = PropProgDF_Base_Wash["TotalCont_A_FP"].to_frame()
y_totCont["Type"] = "No Sampling, Wash"


#-------------------
Final_Prop_Base_PHS4d=Final_Prop_Base_PHS4d.to_frame()
Final_Prop_Base_PHS4d["Type"] = "Sampling, No Wash"
z_prp = PropProgDF_Base_PHS4d["PropCont_A_FP"]

z_totCont = PropProgDF_Base_PHS4d["TotalCont_A_FP"].to_frame()
z_totCont["Type"] = "Sampling, No Wash"

#----------------------
Final_Prop_All = Final_Prop_All.to_frame()
Final_Prop_All["Type"] = "Sampling, Wash"
xy_prp = PropProgDF_All["PropCont_A_FP"]

xy_totCont = PropProgDF_All["TotalCont_A_FP"].to_frame()
xy_totCont["Type"] = "Sampling, Wash"



#Combining them for final proportions
Final_Compared_Prop=pd.concat([Final_Prop_Baseline, 
                          Final_Prop_Base_Wash,
                          Final_Prop_Base_PHS4d,
                          Final_Prop_All], 
                         axis=0, 
                         ignore_index=True)

#sum of all 

Final_Compared_TotCont=pd.concat([x_totCont, 
                             y_totCont,
                             z_totCont,
                             xy_totCont], 
                             axis=0, 
                             ignore_index=True)



#Desnity Plots for proportion of contaminated final packages
#g = sns.FacetGrid(Final_Compared_Prop, col="Type", col_wrap=3)
#g.map_dataframe(sns.histplot, x="PropCont_A_FP", binwidth=0.005, stat = "probability")


g=sns.displot( data =Final_Compared_Prop, 
            x = "PropCont_A_FP" , 
            col = "Type", 
            col_wrap=3,
             stat = "probability",
            facet_kws=dict(sharey=False,sharex= False))

def specs(x, **kwargs):
    plt.axvline(x.mean(), c='red', ls='-', lw=2.5)
    plt.axvline(x.median(), c='orange', ls='--', lw=2.5)

g.map(specs,"PropCont_A_FP" )




#Barplot for proportion of contaminated final packages. 
j = sns.barplot(data = Final_Compared_Prop, y = "Type", x = "PropCont_A_FP")

#Bar plot for total contaminated final packages.
j = sns.barplot(data = Final_Compared_TotCont, y = "Type", x = "TotalCont_A_FP")

#%%

#Total CFUs, for all finished product bags. rrrrrrrrrrrrrrrrrrrrrr

#Baseline no Sampling
FinalConts  = [item for sublist in FinalConts for item in sublist]
dfFinalConts = pd.DataFrame(FinalConts, columns=["CFU"])
dfFinalConts["CFU_g"] = dfFinalConts["CFU"]/(5*454)
sns.displot(dfFinalConts["CFU_g"], bins=30,stat = "probability")
cont_Packages=sum(dfFinalConts["CFU_g"]>0)
Non_contPackages= sum(dfFinalConts["CFU_g"]==0)
RejectedPackages = ((SCInputz.Field_Weight/Inputz.Pack_Weight_FP)*SCInputz.N_Iterations -len(dfFinalConts["CFU_g"]))
cont_Packages/(Non_contPackages+RejectedPackages)*100


#Washing
FinalConts_Base_Wash  = [item for sublist in FinalConts_Base_Wash for item in sublist]
dfFinalConts_Base_Wash = pd.DataFrame(FinalConts_Base_Wash, columns=["CFU"])
dfFinalConts_Base_Wash["CFU_g"] = dfFinalConts_Base_Wash["CFU"]/(5*454)
sns.displot(dfFinalConts_Base_Wash["CFU_g"], bins=30,stat = "probability")
cont_Packages=sum(dfFinalConts_Base_Wash["CFU_g"]>0)
Non_contPackages= sum(dfFinalConts_Base_Wash["CFU_g"]==0)
RejectedPackages = ((SCInputz.Field_Weight/Inputz.Pack_Weight_FP)*SCInputz.N_Iterations -len(dfFinalConts_Base_Wash["CFU_g"]))
cont_Packages/(Non_contPackages+RejectedPackages)*100


#Sampling No Wash
FinalConts_Base_PHS4d  = [item for sublist in FinalConts_Base_PHS4d for item in sublist]
dfFinalConts_Base_PHS4d = pd.DataFrame(FinalConts_Base_PHS4d, columns=["CFU"])
dfFinalConts_Base_PHS4d["CFU_g"] = dfFinalConts_Base_PHS4d["CFU"]/(5*454)
sns.displot(dfFinalConts_Base_PHS4d["CFU_g"], bins=30,stat = "probability")
cont_Packages=sum(dfFinalConts_Base_PHS4d["CFU_g"]>0)
Non_contPackages= sum(dfFinalConts_Base_PHS4d["CFU_g"]==0)
RejectedPackages = ((SCInputz.Field_Weight/Inputz.Pack_Weight_FP)*SCInputz.N_Iterations -len(dfFinalConts_Base_PHS4d["CFU_g"]))
cont_Packages/(Non_contPackages+RejectedPackages)*100

#Sampling and Wash.
FinalConts_All  = [item for sublist in FinalConts_All for item in sublist]
dfFinalConts_All = pd.DataFrame(FinalConts_All, columns=["CFU"])
dfFinalConts_All["CFU_g"] = dfFinalConts_All["CFU"]/(5*454)
sns.displot(dfFinalConts_All["CFU_g"], bins=30,stat = "probability")
cont_Packages=sum(dfFinalConts_All["CFU_g"]>0)
Non_contPackages= sum(dfFinalConts_All["CFU_g"]==0)
RejectedPackages = ((SCInputz.Field_Weight/Inputz.Pack_Weight_FP)*SCInputz.N_Iterations -len(dfFinalConts_All["CFU_g"]))
cont_Packages/(Non_contPackages+RejectedPackages)*100

