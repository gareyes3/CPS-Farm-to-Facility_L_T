# -*- coding: utf-8 -*-
"""
Validatoon of Sampling strateges

Created on Thu Sep 23 08:47:14 2021

@author: gareyes3
"""

#Validation of sampling strategies


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
import statistics

#Main Model Loops
import MainModel3z

#%% 
#Progression DataFrame. 
Progression_DFS = []
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

def Variable_Choosing_DF(df, Hazard_lvl, Background_C, Point_Source_C, Systematic_C):
    #Adding Contamination depending on challenge Background
    if Background_C == True:
        df = ContScen.F_Background_C(df=df, 
                                     Hazard_lvl = Hazard_lvl, 
                                     Partition_Units= Inputz.Partition_Units)
        
    #Adding Contamination depending on challenge Point_Source
    if Point_Source_C ==True:
        df=ContScen.F_Point_Source_C(df=df, 
                                     Hazard_lvl=Hazard_lvl,
                                     No_Cont_Clusters =Inputz.PSNo_Cont_Clusters, 
                                     Cluster_Size = Inputz.PSCluster_Size, 
                                     Partition_Weight = Inputz.Partition_Weight)
    
        
    #Adding Contamination depending on challenge Systematic Sampling
    if Systematic_C == True:
        df = ContScen.F_systematic_C(df=df, Hazard_lvl=Hazard_lvl,
                                     No_Cont_Clusters =Inputz.SysNo_Cont_Clusters,
                                     Cluster_Size= Inputz.SysCluster_Size,
                                     Partition_Weight = Inputz.Partition_Weight)
    
    return df

IterationsSampling= 100

#%%
#Contamination here is 1 CFU/ lb. 
#We can change that. 

def Sampling_By_Mass (Sample_Size, Sampling_Unit, Rejection_Unit, Hazard_level):
    OutputList100g = []
    for i in list(range(IterationsSampling)):
        print(i)
        #Creation of the Data Frame to Track: 
        df= InFunz.F_InDF(Partition_Units = Inputz.Partition_Units,
                          Field_Weight = Inputz.Field_Weight, 
                          slot_number = Inputz.slot_number) 
         
        #Creating dataframe based on selection   
        df = Variable_Choosing_DF(df = df, Hazard_lvl = Hazard_level, Background_C= True, Point_Source_C= False, Systematic_C= False)
        
        #Sampling Function
        #Composite mass to be 10
        df = Funz.F_Sampling_2(df =df,Test_Unit =Sampling_Unit, 
                                  NSamp_Unit = Inputz.n_samples_slot_PH, 
                                  Samp_Size =Sample_Size, 
                                  Partition_Weight =Inputz.Partition_Weight, 
                                  NoGrab =Inputz.No_Grabs_PH)
        
        Cont_Before = sum(df.CFU) #Contamination before rejection sampling
        print(Cont_Before)
    
        df=Funz.F_Rejection_Rule3(df =df, Test_Unit = Rejection_Unit, limit = 0) 
        
        Cont_After = sum(df.CFU)
        ContAcc_P = Cont_After/Cont_Before #Percentage Rejected by H sampling
        
        OutputList100g.append(ContAcc_P)
    
    return OutputList100g


#1 CFU per Kilogram. 
Out_60g = Sampling_By_Mass(Sample_Size= 60, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 220000)
Out_120g = Sampling_By_Mass(Sample_Size= 120, Sampling_Unit="Lot", Rejection_Unit= "Lot", Hazard_level= 220000)
Out_300g = Sampling_By_Mass(Sample_Size= 300, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 220000)
Out_600g = Sampling_By_Mass(Sample_Size= 600, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 220000)
Out_1200g = Sampling_By_Mass(Sample_Size= 1200, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 220000)


statistics.mean(Out_60g)

L_Final_Conts_1 = {
                60 :Out_60g,
                120 :Out_120g,
                300 :Out_300g,
                600 :Out_600g,
                1200 :Out_1200g,
          }

df_L_Final_Conts_1 = pd.DataFrame(L_Final_Conts_1)
df_L_Final_Conts_melted_1 = pd.melt(df_L_Final_Conts_1)
df_L_Final_Conts_melted_1["Contamination level"] = "1CFU/kg"
Scenariosplot =sns.lineplot(x="variable", y="value", data=df_L_Final_Conts_melted_1 )
plt.xlabel("Sample Size")
plt.ylabel("% CFU Accepted by Sampling Plan")




#1 CFU per 10Kilogram. 
Out_60g = Sampling_By_Mass(Sample_Size= 60, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 22000)
Out_120g = Sampling_By_Mass(Sample_Size= 120, Sampling_Unit="Lot", Rejection_Unit= "Lot", Hazard_level= 22000)
Out_300g = Sampling_By_Mass(Sample_Size= 300, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 22000)
Out_600g = Sampling_By_Mass(Sample_Size= 600, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 22000)
Out_1200g = Sampling_By_Mass(Sample_Size= 1200, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 22000)




L_Final_Conts_2 = {
                60 :Out_60g,
                120 :Out_120g,
                300 :Out_300g,
                600 :Out_600g,
                1200 :Out_1200g,
          }

df_L_Final_Conts_2 = pd.DataFrame(L_Final_Conts_2)
df_L_Final_Conts_melted_2 = pd.melt(df_L_Final_Conts_2)
df_L_Final_Conts_melted_2["Contamination level"] = "1CFU/10kg"
Scenariosplot =sns.lineplot(x="variable", y="value", data=df_L_Final_Conts_melted_2 )
plt.xlabel("Sample Size")
plt.ylabel("% CFU Accepted by Sampling Plan")


#1 CFU per 100 grams. 
Out_60g = Sampling_By_Mass(Sample_Size= 60, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 2200000)
Out_120g = Sampling_By_Mass(Sample_Size= 120, Sampling_Unit="Lot", Rejection_Unit= "Lot", Hazard_level= 2200000)
Out_300g = Sampling_By_Mass(Sample_Size= 300, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 2200000)
Out_600g = Sampling_By_Mass(Sample_Size= 600, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 2200000)
Out_1200g = Sampling_By_Mass(Sample_Size= 1200, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 2200000)




L_Final_Conts_3 = {
                60 :Out_60g,
                120 :Out_120g,
                300 :Out_300g,
                600 :Out_600g,
                1200 :Out_1200g,
          }

df_L_Final_Conts_3= pd.DataFrame(L_Final_Conts_3)
df_L_Final_Conts_melted_3 = pd.melt(df_L_Final_Conts_3)
df_L_Final_Conts_melted_3["Contamination level"] = "1CFU/100g"
Scenariosplot =sns.lineplot(x="variable", y="value", data=df_L_Final_Conts_melted_3 )
plt.xlabel("Sample Size")
plt.ylabel("% CFU Accepted by Sampling Plan")


#1 CFU per 10 grams. 
Out_60g = Sampling_By_Mass(Sample_Size= 60, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 22000000)
Out_120g = Sampling_By_Mass(Sample_Size= 120, Sampling_Unit="Lot", Rejection_Unit= "Lot", Hazard_level= 22000000)
Out_300g = Sampling_By_Mass(Sample_Size= 300, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 22000000)
Out_600g = Sampling_By_Mass(Sample_Size= 600, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 22000000)
Out_1200g = Sampling_By_Mass(Sample_Size= 1200, Sampling_Unit="Lot", Rejection_Unit= "Lot",Hazard_level= 22000000)




L_Final_Conts_4 = {
                60 :Out_60g,
                120 :Out_120g,
                300 :Out_300g,
                600 :Out_600g,
                1200 :Out_1200g,
          }

df_L_Final_Conts_4= pd.DataFrame(L_Final_Conts_4)
df_L_Final_Conts_melted_4 = pd.melt(df_L_Final_Conts_4)
df_L_Final_Conts_melted_4["Contamination level"] = "1CFU/10g"
Scenariosplot =sns.lineplot(x="variable", y="value", data=df_L_Final_Conts_melted_4)
plt.xlabel("Sample Size")
plt.ylabel("% CFU Accepted by Sampling Plan")


All_Sampling = [df_L_Final_Conts_melted_1,df_L_Final_Conts_melted_2,df_L_Final_Conts_melted_3,df_L_Final_Conts_melted_4]
All_Sampling_Df = pd.concat(All_Sampling)

sns.lineplot(x="variable", y="value", hue = "Contamination level" ,data=All_Sampling_Df)
plt.xlabel("Sample Size")
plt.ylabel("% of contamination Accepted")
plt.title("Area Contamination, Uniform")
# Put the legend out of the figure
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

