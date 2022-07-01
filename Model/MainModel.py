# -*- coding: utf-8 -*-
"""
Created on Mon May 23 13:22:12 2022

@author: gareyes3
"""

#%%
import sys
sys.path
sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility_L_T\Model')
sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility_L_T\Model')

#%%
import numpy as np
import pandas as pd
import random 
from numpy.random import Generator, PCG64
rng = Generator(PCG64())

#Own Libraries
import Funz
import T_Inputz
import InFunz
import ContScen

#%%

#Creating the initial dataframe for this harvest. 
i=1

#Intiializing dataframe that tracks the contmaination that may remain in the plant
field_cont = InFunz.F_InFieldCont_T(Partition_Units =T_Inputz.Partition_Units ,Field_Weight =T_Inputz.Pick_Weight) 

#Initializing dataframe of actual contamination. 
df= InFunz.F_InDF_T(Partition_Units = T_Inputz.Partition_Units,
                  Field_Weight = T_Inputz.Pick_Weight,
                  Pick_No = i)

#Contaminating Field/ Field Dataframe. 

ContScen.F_systematic_C(df = df, 
               Hazard_lvl = 100000,
               No_Cont_Clusters = 1,
               Cluster_Size = 32.022, 
               Partition_Weight = 32.022)

df["Harvester"] = Funz.F_Assign_Harvesters(df = df, n_harvesters = T_Inputz.N_Harvesters)

#%%
#Basic Information
Tomato_weight = 123/454 #for medium tomato
Tomato_Sequence = int(35_000/0.27)
Individual_Tomatoes = np.arange(1,Tomato_Sequence)

Individual_Plants = np.repeat(np.arange(1,int(np.ceil(Tomato_Sequence/120))),120+1)
Pick_Sequence = [1,2,3]*(int(np.ceil(Tomato_Sequence/3)))
Pick_Random = random.sample(Pick_Sequence, len(Pick_Sequence))

#Harvest information
Total_Harvesters = 14

#Model
#Creation of the initial dataframe
Field_df=pd.DataFrame({"Tomato_ID": Individual_Tomatoes,
                       "Plant_ID": Individual_Plants[0:Individual_Tomatoes.size],
                       "Pick_ID": Pick_Random[0:Individual_Tomatoes.size],
                       "Weight": 0.27,
                       "Harvester" : 0,
                       "CFU": 0,
                       "Location": 1,
                  })

#Harvest
Harvester_Pattern = np.repeat(list(range(1,15)),118)
Harvester_Pattern_Full=np.tile(Harvester_Pattern,int(np.ceil(Tomato_Sequence/len(Harvester_Pattern))))
count = 0
for i in Field_df['Pick_ID'].to_numpy():
    if i == 1:
        Field_df.loc[count, "Harvester"] = Harvester_Pattern_Full[count]
        Field_df.loc[count, "Location"] = 2
    count = count+1

#Contamination Scenarios: 
#1. Bird Droppings
#Percent of total tomatoes contaminated by bird droppings? 

Percent_Contaminated = 0.1 #Percentage of tomatoes contaminated
Percent_D_Contaminatinated= Percent_Contaminated/100


Hazard_lvl = 100_000
No_Cont_Clusters = 2
No_Cont_PartitionUnits = int((len(Field_df[Field_df["Location"]==2]))*Percent_Contaminated/100)

Field_df_1 =Field_df.loc[Field_df["Location"]==2]

#Determining the hazard level per cluster
Hazard_lvl_percluster= Hazard_lvl / No_Cont_Clusters #(No_Cont_PartitionUnits*No_Cont_Clusters)
for i in range(0,No_Cont_Clusters):
    n = random.randint(0,len(Field_df_1.index)- No_Cont_PartitionUnits)
    x_random_consecutive_rows = Field_df_1[n:n + No_Cont_PartitionUnits]
    x_random_consecutive_rows = list(x_random_consecutive_rows.index)
    #using multinomial creating array to contaminated the desired outputs
    #probaility defined by the number of partitions. 
    Contamination_Pattern = rng.multinomial(Hazard_lvl_percluster,[1/No_Cont_PartitionUnits]*No_Cont_PartitionUnits,1)
    df.at[x_random_consecutive_rows,'CFU']= Field_df_1.loc[x_random_consecutive_rows,'CFU'] + Contamination_Pattern[0]


