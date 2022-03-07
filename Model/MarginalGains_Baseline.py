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
sys.path.append('C:\\Users\reyes\Documents\GitHub\CPS-Farm-to-Facility')

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

#%% MAIN FUCTION THE RUNS THE MODEL WITH THE INTERVENTIONS LISTES
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
                      PreS_Wash = False,
                      Sanitation = False,
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
    SCInputz.Spray_WashYN =PreS_Wash
    
    #Sanitation:
    SCInputz.Sanitation_YN = Sanitation
    
        
    #Running The Model.
    Main_Mod_Outs = MainModel3z.F_MainLoop()
    
    #Getting the outputs from the function.
    OutputDF = Main_Mod_Outs[1]
    ProgDF = Main_Mod_Outs[0]
    PropProgDF = Main_Mod_Outs[2]

    return [OutputDF,ProgDF,PropProgDF,Cont_Levels_PH,Scenario_No]

#%% Important Functions for the Analysys

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

def F_Sampling_Power (DF, Step_CFU_Acc, Step_CFU_Rej):
    Total_Contam = len(DF[(DF[Step_CFU_Acc]>0) | (DF[Step_CFU_Rej]>0) ])
    Total_Contam_Rej = len(DF[ (DF[Step_CFU_Rej]>0) ])
    Power = Total_Contam_Rej/Total_Contam
    return [Total_Contam, Total_Contam_Rej, Power]

def  CFU_Sampling_Stage (DF,Step_col_Name):
    Before_PHSInt= DF[Step_col_Name]
    return Before_PHSInt[Before_PHSInt>0].describe()

def Mean_Quantiles(df,columnname,q1,q2) : 
    mean_1 = df[columnname].mean()*100
    quantiles_1= df[columnname].quantile([q1,q2])
    return(mean_1, quantiles_1)
    

def F_Outputs_Table(List_of_Outputs):
    rep = 0
    Columns_Final_Outs = [
        "Final_CFU_Acc_Portion_mean",
        "Final_CFU_Acc_Portion_5CI",
        "Final_CFU_Acc_Portion_95CI",
        "Final_CFU_Rej_Portion_mean",
        "Final_CFU_Rej_Portion_5CI",
        "Final_CFU_Rej_Portion_95CI",
        "Prevalence_Acc_Mean",
        "Prevalence_Acc_5CI",
        "Prevalence_Acc_95CI",
        "Prevalence_Rej_Mean",
        "Prevalence_Rej_5CI",
        "Prevalence_Rej_95CI",
        "Ratio_Product_accepted",
        "Pooled_CFU_g_mean",
        "Pooled_CFU_g_5CI",
        "Pooled_CFU_g_5CI",   
        
    ]
    
    Outputs_Df =pd.DataFrame(np.NaN, index= range(len(List_of_Outputs)), columns =Columns_Final_Outs)
    for i in List_of_Outputs:
        #Subseting Dataframe for the accepted
        Subset_Acc_NI_PHS4d= i[0][i[0]['FP_Wei_Acc'] == 100_000].index
        Subset_Rej_NI_PHS4d= i[0][i[0]['FP_Wei_Acc'] != 100_000].index
        
        #Final CFUs based on if accepted or rejected
            #Accepted
        Final_CFU_Acc_Portion_mean=i[1][i[1].index.isin(Subset_Acc_NI_PHS4d)]["Final Product Facility"].mean()
        Final_CFU_Acc_Portion_90CI=i[1][i[1].index.isin(Subset_Acc_NI_PHS4d)]["Final Product Facility"].quantile([0.05,0.95])
            #Rejected
        Final_CFU_Rej_Portion_mean=i[1][i[1].index.isin(Subset_Rej_NI_PHS4d)]["Final Product Facility"].mean()
        Final_CFU_Rej_Portion_90CI=i[1][i[1].index.isin(Subset_Rej_NI_PHS4d)]["Final Product Facility"].quantile([0.05,0.95])
        
        #Prevalence of contaminated packages 
            #Accepted
        Prevalence_Acc_Mean=i[2][i[2].index.isin(Subset_Acc_NI_PHS4d)]["PropCont_A_FP_Whole"].mean()
        Prevalence_Acc_90CI=i[2][i[2].index.isin(Subset_Acc_NI_PHS4d)]["PropCont_A_FP_Whole"].quantile([0.05,0.95])
            #Rejected
        Prevalence_Rej_Mean=i[2][i[2].index.isin(Subset_Rej_NI_PHS4d)]["PropCont_A_FP_Whole"].mean()
        Prevalence_Rej_90CI=i[2][i[2].index.isin(Subset_Rej_NI_PHS4d)]["PropCont_A_FP_Whole"].quantile([0.05,0.95])
            #Pooled Stuff
        Pooled_CFU_g_mean= ((i[1][i[1].index.isin(Subset_Acc_NI_PHS4d)]["Final Product Facility"])/ (i[0][i[0].index.isin(Subset_Acc_NI_PHS4d)]["FP_Wei_Acc"]*454)).mean()
        Pooled_CFU_g_90CI= ((i[1][i[1].index.isin(Subset_Acc_NI_PHS4d)]["Final Product Facility"])/ (i[0][i[0].index.isin(Subset_Acc_NI_PHS4d)]["FP_Wei_Acc"]*454)).quantile([0.05,0.95])
        
        #Ratio of product accepted all iterations (weight)
        i[0][i[0]['FP_Wei_Acc'] == 50] = 0
        Ratio_Product_accepted=i[0]['FP_Wei_Acc'].sum()/(100*100_000)
        
        Outputs_Df.at[rep,"Final_CFU_Acc_Portion_mean"] = Final_CFU_Acc_Portion_mean
        Outputs_Df.at[rep,"Final_CFU_Acc_Portion_5CI"] = Final_CFU_Acc_Portion_90CI.to_list()[0]
        Outputs_Df.at[rep,"Final_CFU_Acc_Portion_95CI"] = Final_CFU_Acc_Portion_90CI.to_list()[1]
        
        
        Outputs_Df.at[rep,"Final_CFU_Rej_Portion_mean"] = Final_CFU_Rej_Portion_mean
        Outputs_Df.at[rep,"Final_CFU_Rej_Portion_5CI"] = Final_CFU_Rej_Portion_90CI.to_list()[0]
        Outputs_Df.at[rep,"Final_CFU_Rej_Portion_95CI"] = Final_CFU_Rej_Portion_90CI.to_list()[1]
        
        Outputs_Df.at[rep,"Prevalence_Acc_Mean"] = Prevalence_Acc_Mean
        Outputs_Df.at[rep,"Prevalence_Acc_5CI"] = Prevalence_Acc_90CI.to_list()[0]
        Outputs_Df.at[rep,"Prevalence_Acc_95CI"] = Prevalence_Acc_90CI.to_list()[1]
        
        Outputs_Df.at[rep,"Prevalence_Rej_Mean"] = Prevalence_Rej_Mean
        Outputs_Df.at[rep,"Prevalence_Rej_5CI"] = Prevalence_Rej_90CI.to_list()[0]
        Outputs_Df.at[rep,"Prevalence_Rej_95CI"] = Prevalence_Rej_90CI.to_list()[1]
        
        Outputs_Df.at[rep,"Ratio_Product_accepted"] = Ratio_Product_accepted
        
        Outputs_Df.at[rep,"Pooled_CFU_g_mean"] = Pooled_CFU_g_mean
        Outputs_Df.at[rep,"Pooled_CFU_g_5CI"] =  Pooled_CFU_g_90CI.to_list()[0]
        Outputs_Df.at[rep,"Pooled_CFU_g_95CI"] =  Pooled_CFU_g_90CI.to_list()[1]
        
        
        
        rep=rep+1
    
    return Outputs_Df
#%% Effect of Individual Interventions
Baseline_NI =  scenario_function()

#Effect of Holding
Baseline_NI_Holding =  scenario_function(Holding=True)

#Effect of PreCooling
Baseline_NI_Precooling =  scenario_function(Pre_Cooling=True)

#Effect of Wash
Baseline_NI_Wash =  scenario_function(Washing=True)

#Harvest Wash
Baseline_NI_Sp_Wash =  scenario_function(PreS_Wash=True)


Baseline_NI_PLS = scenario_function(Sanitation=True)


# Data Analysis

List_of_Outs_Ints = [Baseline_NI,
                     Baseline_NI_Holding,
                     Baseline_NI_Precooling,
                     Baseline_NI_Wash,
                     Baseline_NI_Sp_Wash,
                     Baseline_NI_PLS
                     ]

Outputdf_INT = F_Outputs_Table(List_of_Outs_Ints)

#Initial Contamination From BAseline

#Creatring Dataframe with the Final Contmainations
Intervention_Final_Conts = [Baseline_NI[1],
                     Baseline_NI_Holding[1],
                     Baseline_NI_Precooling[1],
                     Baseline_NI_Wash[1],
                     Baseline_NI_Sp_Wash[1],
                     Baseline_NI_PLS[1]
                     ]


#Creating dataframe of final contamination for every intervention. 
List_of_Final_Conts_Ints = [x["Final Product Facility"] for x in Intervention_Final_Conts]
Column_Names = "BaselineNI Holding Precooling Washing PreSpray_Wash Sanitation".split()
Final_Conts_INT = pd.concat(List_of_Final_Conts_Ints, axis = 1)
Final_Conts_INT.columns = Column_Names
Final_Conts_INT_melted = Final_Conts_INT.melt()

#Plotting the bar graph or boxplot of the differences. 
H=sns.catplot(x="variable", y="value", kind = "box" ,
            data=Final_Conts_INT_melted)
plt.xlabel("Intervention")
plt.ylabel("Total CFUs at Finished Product")
plt.yscale('log')
plt.title("CFU Final Contamination")
plt.xticks(rotation=70)

#Mean and Confidence interval for each
Mean_andCI= [mean_CI_ONE(x) for x in List_of_Final_Conts_Ints]

#Calculating the reduction of the means for each one of them
Reduction = Calc_red(meanCI =Mean_andCI,treatments= 6)

reduction_DF = pd.DataFrame({"Treatment": Column_Names,
                             "Reduction": Reduction} )

reduction_DF=reduction_DF.sort_values('Reduction',ascending=False).reset_index()

#Graph of the difference between the treatments. 
chart = sns.barplot(data = reduction_DF, x = "Treatment", y = "Reduction", order=reduction_DF['Treatment'])
chart.bar_label(chart.containers[0])
plt.title("mean % Reduction obtained by Intervention")
plt.xlabel("Intervention")
plt.ylabel("Percent Reduction from Baseline NI")

#GEtting the confidence interval for the final contamination in dataframe form
Intervention_Comp = pd.DataFrame([mean_CI_ONE(x) for x in List_of_Final_Conts_Ints], columns = ["mean", "95% CI"])

#Proportion of packages contaminated
Intervention_Props = [Baseline_NI[2],
                     Baseline_NI_Holding[2],
                     Baseline_NI_Precooling[2],
                     Baseline_NI_Wash[2],
                     Baseline_NI_Sp_Wash[2],
                     Baseline_NI_PLS[2]
                     ]

#Creating dataframe of final contamination for every intervention. 
Intervention_PropCont_List = [x["PropCont_A_FP_Whole"] for x in Intervention_Props]

Prop_Cont_INT = pd.concat(Intervention_PropCont_List, axis = 1)
Prop_Cont_INT.columns = Column_Names
Prop_Cont_INT_melted = Prop_Cont_INT.melt()

#Plotting the bar graph or boxplot of the differences. 
H=sns.catplot(x="variable", y="value", kind = "bar" ,
            data=Prop_Cont_INT_melted)
plt.xlabel("Intervention")
plt.ylabel("Proportion Contaminated at Final Product")
plt.xticks(rotation=70)

Mean_Props_INT= [mean_CI_ONE(x) for x in Intervention_PropCont_List]

#Histplot
h=sns.displot( data =Prop_Cont_INT_melted, 
            x = "value" , 
            col = "variable", 
            col_wrap=3,
             stat = "count",
             bins = 30,
            facet_kws=dict(sharey=False,sharex= False))
plt.suptitle("Proportion of Paclages Contminated",) 

def specs(x, **kwargs):
    plt.axvline(x.mean(), c='red', ls='-', lw=2.5)
    plt.axvline(x.median(), c='orange', ls='--', lw=2.5)

h.map(specs,"value" )


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
                                 PreS_Wash=True,
                                 Sanitation = True
                                 )
 

#Baseline with intervention. 4 days pre-harvest sampling

Baseline_AI_PHS4d =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 PreS_Wash=True,
                                 Sanitation = True,
                                 PHS4d = True)


### Pre-Harvest Sampling 4h
#Baseline with intervention. 4 hours pre-harvest sampling
Baseline_AI_PHS4h =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 PreS_Wash=True,
                                 Sanitation = True,
                                 PHS4h = True)

### Pre-Harvest Sampling Intense
#Baseline with intervention. Intense pre-harvest sampling
Baseline_AI_PHSInt =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 PreS_Wash=True,
                                 Sanitation = True,
                                 PHSInt = True)

### Harvest Sampling Intense
#Baseline with intervention. Intense Harvest sampling
Baseline_AI_H =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 PreS_Wash=True,
                                 Sanitation = True,
                                 HSTrad = True)

### Receiving Sampling Intense
#Baseline with intervention. Intense Receiving sampling
Baseline_AI_R =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 PreS_Wash=True,
                                 Sanitation = True,
                                 RSTrad = True)

### FPS Sampling Intense
#Baseline with intervention. Intense Receiving sampling
Baseline_AI_FP =  scenario_function(Washing = True,
                                 Holding = True,
                                 Pre_Cooling = True,
                                 PreS_Wash=True,
                                 Sanitation = True,
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

List_of_MainOuts = [Baseline_NI[0],
                     Baseline_NI_PHS4d[0],
                     Baseline_NI_PHS4h[0],
                     Baseline_NI_PHSInt[0],
                     Baseline_NI_H[0],
                     Baseline_NI_R[0],
                     Baseline_NI_FP[0]
                     ]

Baseline_NI_PHS4d[0].columns

List_of_Outs = [Baseline_NI,
                     Baseline_NI_PHS4d,
                     Baseline_NI_PHS4h,
                     Baseline_NI_PHSInt,
                     Baseline_NI_H,
                     Baseline_NI_R,
                     Baseline_NI_FP
                     ]

#Names
Col_Names_NI = "BaselineNI PHS4D_NI PHS4H_NI PHSInt_NI HTrad_NI RSTrad_NI FPSTrad_NI".split()
#Using function        
Outputs_Df=F_Outputs_Table(List_of_Outs)  

Outputs_Df.columns
Outputs_Df["Treatments"] = Col_Names_NI

#Exploring the relationships
sns.scatterplot(data=Outputs_Df, x="Final_CFU_Acc_Portion_mean", y="Ratio_Product_accepted", hue="Treatments")

#Pooled CFU_g, 







#Creating list of Final Contmainations
List_Final_Cont_NI = [x["Final Product Facility"] for x in List_of_Progs_NI]
Col_Names_NI = "BaselineNI PHS4D_NI PHS4H_NI PHSInt_NI HTrad_NI RSTrad_NI FPSTrad_NI".split()
#Creating and Melting the Dataframe of Final Contminations
DF_Final_Cont_NI = pd.concat(List_Final_Cont_NI, axis = 1)
DF_Final_Cont_NI.columns = Col_Names_NI
DF_Final_Cont_NI_melted = DF_Final_Cont_NI.melt()

#Creating Cat plot bar or box, change arguement
H=sns.catplot(x="variable", y="value", kind = "box" ,
            data=DF_Final_Cont_NI_melted)
plt.xlabel("Intervention")
plt.ylabel("Total CFUs at Finished Product")
plt.yscale('log')
plt.title("CFU Final Contamination: Baseline No INterventions")
plt.xticks(rotation=70)



#Means compared to each other. 
Final_Cont_NI_MeanCI= [mean_CI_ONE(x) for x in List_Final_Cont_NI]

Reduction_Cont_NI = Calc_red(meanCI =Final_Cont_NI_MeanCI,treatments= 7)

DF_Reduction_Cont_NI = pd.DataFrame({"Treatment": Col_Names_NI,
                             "Reduction": Reduction_Cont_NI} )

DF_Reduction_Cont_NI=DF_Reduction_Cont_NI.sort_values('Reduction',ascending=False).reset_index()

chart = sns.barplot(data = DF_Reduction_Cont_NI, x = "Treatment", y = "Reduction", order=DF_Reduction_Cont_NI['Treatment'])
chart.bar_label(chart.containers[0])
plt.xlabel("Intervention")
plt.ylabel("Percent Reduction from Baseline NI")



#Sampling Results: 

#PHS4d
F_Sampling_Power(Baseline_NI_PHS4d[0],"PH_CFU_Acc","PH_CFU_Rej")
CFU_Sampling_Stage (Baseline_NI_PHS4d[1],"Bef Pre-Harvest Samp")
#PHS4h
F_Sampling_Power(Baseline_NI_PHS4h[0],"PH_CFU_Acc","PH_CFU_Rej")
CFU_Sampling_Stage (Baseline_NI_PHS4h[1],"Bef Pre-Harvest Samp")
#PHSInt    
F_Sampling_Power(Baseline_NI_PHSInt[0],"PH_CFU_Acc","PH_CFU_Rej")
CFU_Sampling_Stage (Baseline_NI_PHSInt[1],"Bef Pre-Harvest Samp")
#HS   
F_Sampling_Power(Baseline_NI_H[0],"H_CFU_Acc","H_CFU_Rej")
CFU_Sampling_Stage (Baseline_NI_H[1],"Bef Harvest Samp")
#RS
F_Sampling_Power(Baseline_NI_R[0],"R_CFU_Acc","R_CFU_Rej")
CFU_Sampling_Stage (Baseline_NI_R[1],"Bef Receiving Samp")
#FPS
F_Sampling_Power(Baseline_NI_FP[0],"FP_CFU_Acc","FP_CFU_Rej")
CFU_Sampling_Stage (Baseline_NI_FP[1],'Bef Final Prod S')

#Final CFUs for all. 
#prints the mean total CFUs and the CIs
Final_Cont_NI_MeanCI

#Getting the Prevalence of Contaminated Packages.

Mean_Quantiles(df = Baseline_NI[2],columnname ="PropCont_A_FP_Whole" ,q1 = 0.05,q2 = 0.95)  

#Proportion of packages contaminated
Intervention_Props_NI = [Baseline_NI[2],
                     Baseline_NI_PHS4d[2],
                     Baseline_NI_PHS4h[2],
                     Baseline_NI_PHSInt[2],
                     Baseline_NI_H[2],
                     Baseline_NI_R[2],
                     Baseline_NI_FP[2]
                     ]

#Creating dataframe of final contamination for every intervention. 
Intervention_PropCont_List_NI = [x["PropCont_A_FP_Whole"] for x in Intervention_Props_NI]

Prop_Cont_NI = pd.concat(Intervention_PropCont_List_NI, axis = 1)
Prop_Cont_NI.columns = Col_Names_NI
Prop_Cont_NI_melted = Prop_Cont_NI.melt()

#Plotting the bar graph or boxplot of the differences. 
H=sns.catplot(x="variable", y="value", kind = "box" ,
            data=Prop_Cont_NI_melted)
plt.xlabel("Intervention")
plt.ylabel("Proportion Contaminated at Final Product")
plt.xticks(rotation=70)

Mean_Props_NI= [mean_CI_ONE(x) for x in Intervention_PropCont_List_NI]

#Histplot
h=sns.displot( data =Prop_Cont_NI_melted, 
            x = "value" , 
            col = "variable", 
            col_wrap=3,
             stat = "count",
             bins = 30,
            facet_kws=dict(sharey=False,sharex= False))
plt.suptitle("Proportion of Paclages Contminated",) 

def specs(x, **kwargs):
    plt.axvline(x.mean(), c='red', ls='-', lw=2.5)
    plt.axvline(x.median(), c='orange', ls='--', lw=2.5)

h.map(specs,"value" )

 

### Baseline All Interventions, good system.

#Creating list of contamination progression
List_of_Progs_AI = [Baseline_AI[1],
                     Baseline_AI_PHS4d[1],
                     Baseline_AI_PHS4h[1],
                     Baseline_AI_PHSInt[1],
                     Baseline_AI_H[1],
                     Baseline_AI_R[1],
                     Baseline_AI_FP[1]
                     ]



#Creating list of Final Contmainations
List_Final_Cont_AI = [x["Final Product Facility"] for x in List_of_Progs_AI]
Col_Names_AI = "BaselineAI PHS4D_AI PHS4H_AI PHSInt_AI HTrad_AI RSTrad_AI FPSTrad_AI".split()
#Creating and Melting the Dataframe of Final Contminations
DF_Final_Cont_AI = pd.concat(List_Final_Cont_AI, axis = 1)
DF_Final_Cont_AI.columns = Col_Names_AI
DF_Final_Cont_AI_melted = DF_Final_Cont_AI.melt()

#Creating Cat plot bar or box, change arguement
H=sns.catplot(x="variable", y="value", kind = "box" ,
            data=DF_Final_Cont_AI_melted)
plt.xlabel("Intervention")
plt.ylabel("Total CFUs at Finished Product")
plt.yscale('log')
plt.title("CFU Final Contamination: Baseline All Interventions")
plt.xticks(rotation=70)

#Means compared to each other. 
Final_Cont_AI_MeanCI= [mean_CI_ONE(x) for x in List_Final_Cont_AI]

for i in range(7):
    print(Final_Cont_AI_MeanCI[i][0]/Final_Cont_AI_MeanCI[0][0])


Reduction_Cont_AI = Calc_red(meanCI =Final_Cont_AI_MeanCI,treatments= 7)

DF_Reduction_Cont_AI = pd.DataFrame({"Treatment": Col_Names_AI,
                             "Reduction": Reduction_Cont_AI} )

DF_Reduction_Cont_AI=DF_Reduction_Cont_AI.sort_values('Reduction',ascending=False).reset_index()

chart = sns.barplot(data = DF_Reduction_Cont_AI, x = "Treatment", y = "Reduction", order=DF_Reduction_Cont_AI['Treatment'])
chart.bar_label(chart.containers[0])
plt.xlabel("Intervention")
plt.ylabel("Percent Reduction from BaselineAI")



#Sampling Results: 

#PHS4d
F_Sampling_Power(Baseline_AI_PHS4d[0],"PH_CFU_Acc","PH_CFU_Rej")
CFU_Sampling_Stage (Baseline_AI_PHS4d[1],"Bef Pre-Harvest Samp")
#PHS4h
F_Sampling_Power(Baseline_AI_PHS4h[0],"PH_CFU_Acc","PH_CFU_Rej")
CFU_Sampling_Stage (Baseline_AI_PHS4h[1],"Bef Pre-Harvest Samp")
#PHSInt    
F_Sampling_Power(Baseline_AI_PHSInt[0],"PH_CFU_Acc","PH_CFU_Rej")
CFU_Sampling_Stage (Baseline_AI_PHSInt[1],"Bef Pre-Harvest Samp")
#HS   
F_Sampling_Power(Baseline_AI_H[0],"H_CFU_Acc","H_CFU_Rej")
CFU_Sampling_Stage (Baseline_AI_H[1],"Bef Harvest Samp")
#RS
F_Sampling_Power(Baseline_AI_R[0],"R_CFU_Acc","R_CFU_Rej")
CFU_Sampling_Stage (Baseline_AI_R[1],"Bef Receiving Samp")
#FPS
F_Sampling_Power(Baseline_AI_FP[0],"FP_CFU_Acc","FP_CFU_Rej")
CFU_Sampling_Stage (Baseline_AI_FP[1],'Bef Final Prod S')

#Final CFUs for all. 
#prints the mean total CFUs and the CIs
Final_Cont_AI_MeanCI

#Getting the Prevalence of Contaminated Packages.

Mean_Quantiles(df = Baseline_AI[2],columnname ="PropCont_A_FP_Whole" ,q1 = 0.05,q2 = 0.95)  

#Proportion of packages contaminated
Intervention_Props_AI = [Baseline_AI[2],
                     Baseline_AI_PHS4d[2],
                     Baseline_AI_PHS4h[2],
                     Baseline_AI_PHSInt[2],
                     Baseline_AI_H[2],
                     Baseline_AI_R[2],
                     Baseline_AI_FP[2]
                     ]

#Creating dataframe of final contamination for every intervention. 
Intervention_PropCont_List_AI = [x["PropCont_A_FP_Whole"] for x in Intervention_Props_AI]

Prop_Cont_AI = pd.concat(Intervention_PropCont_List_AI, axis = 1)
Prop_Cont_AI.columns = Col_Names_AI
Prop_Cont_AI_melted = Prop_Cont_AI.melt()

#Plotting the bar graph or boxplot of the differences. 
H=sns.catplot(x="variable", y="value", kind = "bar" ,
            data=Prop_Cont_AI_melted)
plt.xlabel("Intervention")
plt.ylabel("Proportion Contaminated at Final Product")
plt.xticks(rotation=70)

Mean_Props_AI= [mean_CI_ONE(x) for x in Intervention_PropCont_List_AI]

for i in range(7):
    print(Mean_Props_AI[i][0]/Mean_Props_AI[0][0])

#Histplot
h=sns.displot( data =Prop_Cont_AI_melted, 
            x = "value" , 
            col = "variable", 
            col_wrap=3,
             stat = "count",
             bins = 30,
            facet_kws=dict(sharey=False,sharex= False))
plt.suptitle("Proportion of Paclages Contminated",) 

def specs(x, **kwargs):
    plt.axvline(x.mean(), c='red', ls='-', lw=2.5)
    plt.axvline(x.median(), c='orange', ls='--', lw=2.5)

h.map(specs,"value" )





#%%

sns.barplot(data = Baseline_NI[1])
plt.xticks(rotation=-80)
plt.yscale('log')
plt.yticks([1,10,100,1000,10000,100000])
plt.title("Contamination Progression")
plt.ylabel("CFUs in System")



sns.barplot(data = Baseline_AI[1])
plt.xticks(rotation=-80)
plt.yticks([1,10,100,1000,10000,100000])
plt.yscale('log')
plt.title("Contamination Progression")
plt.ylabel("CFUs in System")



sns.barplot(data = Baseline_AI_PHS4d[1])
plt.xticks(rotation=-80)
plt.yticks([1,10,100,1000,10000,100000])
plt.yscale('log')
plt.title("Contamination Progression")
plt.ylabel("CFUs in System")



dfBaseline_NI_melted= pd.melt(Baseline_NI[1]["Final Product Facility"])
dfBaseline_NI_melted["Type"] = "BaselineNI"



dfBaseline_NI_melted= Baseline_NI[1]["Final Product Facility"]
dfBaseline_NI_melted["Type"] = "BaselineNI"

dfBaseline_NI_PH4D_melted= Baseline_NI_PHS4d[1]["Final Product Facility"]
dfBaseline_NI_PH4D_melted["Type"] = "BaselineNI_PH4d"

NI_compared = pd.concat([dfBaseline_NI_melted, dfBaseline_NI_PH4D_melted], 0)

sns.barplot(data = NI_compared, x  = "variable", y= "value", hue = "Type")
plt.xticks(rotation=-80)
plt.yticks([1,10,100,1000,10000,100000])
plt.yscale('log')
plt.title("Contamination Progression")
plt.ylabel("CFUs in System")


dfBaseline_AI_melted= pd.melt(Baseline_AI[1])
dfBaseline_AI_melted["Type"] = "BaselineAI"




dfBaseline_AI_PH4D_melted= pd.melt(Baseline_AI_PHS4d[1])
dfBaseline_AI_PH4D_melted["Type"] = "BaselineAI_PH4d"

AI_compared = pd.concat([dfBaseline_AI_melted, dfBaseline_AI_PH4D_melted], 0)

sns.barplot(data = AI_compared, x  = "variable", y= "value", hue = "Type")
plt.xticks(rotation=-80)
plt.yticks([1,10,100,1000,10000,100000])
plt.yscale('log')
plt.title("Contamination Progression")
plt.ylabel("CFUs in System")


df_comparisons = pd.DataFrame ({"Baseline NI": Baseline_NI[1]["Final Product Facility"],
                              "PH4d": Baseline_NI_PHS4d[1]["Final Product Facility"] })
df_comparisons_melt = pd.melt(df_comparisons)


sns.barplot(data =df_comparisons_melt, x  = "variable", y= "value")
plt.xticks(rotation=-80)
#plt.yticks([1,10,100,1000,10000,100000])
#plt.yscale('log')
plt.title("Contamination at Final Product")
plt.ylabel("CFUs ")


df_comparisons_AI = pd.DataFrame ({"Baseline AI": Baseline_AI[1]["Final Product Facility"],
                              "PH4d": Baseline_AI_PHS4d[1]["Final Product Facility"] })
df_comparisons_melt_AI = pd.melt(df_comparisons_AI)


sns.barplot(data =df_comparisons_melt_AI, x  = "variable", y= "value")
plt.xticks(rotation=-80)
#plt.yticks([1,10,100,1000,10000,100000])
#plt.yscale('log')
plt.title("Contamination at Final Product")
plt.ylabel("CFUs ")