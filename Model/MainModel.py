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
import math
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

#This function create a random chunk of X rows in a dataframe (each row in this mdoel represents one individual tomato)
def random_chunk(lst, chunk_size):
    nb_chunks = int(math.ceil(len(lst)/chunk_size))
    choice = random.randrange(nb_chunks) # 0 <= choice < nb_chunks
    return lst[choice*chunk_size:(choice+1)*chunk_size]

def field_cont_percetage(df, percent_cont, Hazard_lvl, No_Cont_Clusters):
    #This function contaminated the tomato field randomly based on a cluter of X%. 
    Percent_Contaminated =percent_cont #Percentage of tomatoes contaminated
    Percent_D_Contaminatinated= Percent_Contaminated/100 #Percentage in decimal point
    Hazard_lvl = Hazard_lvl #CFUs in contaminated area total Cells
    No_Cont_Clusters = No_Cont_Clusters #in how many clusters will the percentage and cont be split into
    No_Cont_PartitionUnits = int((len(df[df["Location"]==1]))*Percent_D_Contaminatinated) #how many tomatoes are contmainated based on percentage
    Field_df_1 =df.loc[df["Location"]==1] #filtering main df into only those that are in a field
    
    #Determining the hazard level per cluster
    Hazard_lvl_percluster= Hazard_lvl / No_Cont_Clusters #(No_Cont_PartitionUnits*No_Cont_Clusters)
    for i in range(0,No_Cont_Clusters):
        random_Chunky = list(random_chunk(lst = Field_df_1.index, chunk_size = No_Cont_PartitionUnits)) #creating random chunk
        Contamination_Pattern = rng.multinomial(Hazard_lvl_percluster,[1/No_Cont_PartitionUnits]*No_Cont_PartitionUnits,1) #spliting cont into chunks length
        Field_df_1.loc[random_Chunky, "CFU"] = Field_df_1.loc[random_Chunky, "CFU"] + Contamination_Pattern[0] #adding contmaination

    df.update(Field_df_1)
    
    return df

def field_cont_ntomatoes(df, ntomatoes_cont_pclust, Hazard_lvl, No_Cont_Clusters):
    #This function contaminated the tomato field randomly based on a cluter of X%. 
    Hazard_lvl = Hazard_lvl #CFUs in contaminated area total Cells
    No_Cont_Clusters = No_Cont_Clusters #in how many clusters will the percentage and cont be split into
    No_Cont_PartitionUnits = ntomatoes_cont_pclust #how many tomatoes are contmainated per cluster
    Field_df_1 =df.loc[df["Location"]==1] #filtering main df into only those that are in a field
    
    #Determining the hazard level per cluster
    Hazard_lvl_percluster= Hazard_lvl / No_Cont_Clusters #(No_Cont_PartitionUnits*No_Cont_Clusters)
    for i in range(0,No_Cont_Clusters):
        random_Chunky = list(random_chunk(lst = Field_df_1.index, chunk_size = No_Cont_PartitionUnits)) #creating random chunk
        Contamination_Pattern = rng.multinomial(Hazard_lvl_percluster,[1/No_Cont_PartitionUnits]*No_Cont_PartitionUnits,1) #spliting cont into chunks length
        Field_df_1.loc[random_Chunky, "CFU"] = Field_df_1.loc[random_Chunky, "CFU"] + Contamination_Pattern[0] #adding contmaination

    df.update(Field_df_1)
    
    return df

def Harvesting_Function(df, Total_Harvesters, Tomatoes_Per_Bucket,Tomato_Sequence, Pick_No):
    Harvester_Pattern = np.repeat(list(range(1,Total_Harvesters+1)),Tomatoes_Per_Bucket)
    Harvester_Pattern_Full=np.tile(Harvester_Pattern,int(np.ceil(Tomato_Sequence/len(Harvester_Pattern))))

    Field_df_1 =df.loc[df['Pick_ID']==Pick_No]
    Field_df_1["Harvester"] = Harvester_Pattern_Full[list(range(Field_df_1["Harvester"].size))]
    Field_df_1["Location"] = 2
    
    df.update(Field_df_1)
    return df

def Harvester_Cont_Function(df, Hazard_Level, Pick_No, Cont_Harvester_No):
    Field_df_1 =df.loc[(df['Pick_ID']==Pick_No) & (df['Harvester'] == Cont_Harvester_No )]
    Size_1 = Field_df_1['Harvester'].size
    cont_pattern=rng.multinomial(Hazard_Level,[1/Size_1]*Size_1,1) 
    Field_df_1["CFU"] = cont_pattern[0]
    df.update(Field_df_1)
    return df

#%%

#Basic Information
Tomato_weight = 250/454 #for medium tomato
Tomato_Sequence = int(105_000/Tomato_weight)
Individual_Tomatoes = np.arange(1,Tomato_Sequence)
Tomatoes_Per_Plant = 120
Tomatoes_Per_Bucket = int(32/Tomato_weight)


#total pick information
N_Pick = 3
Days_Between_Picks = 7


Individual_Plants = np.repeat(np.arange(1,int(np.ceil(Tomato_Sequence/Tomatoes_Per_Plant))),Tomatoes_Per_Plant+1)
Pick_Sequence = list(range(1,N_Pick+1))*(int(np.ceil(Tomato_Sequence/3)))
Pick_Random = random.sample(Pick_Sequence, len(Pick_Sequence))

#Harvest information
Total_Harvesters = 14

#Probabilities

Pr_bird_drop = 0.2 #probability of bird contamination fields

#Model
#Creation of the initial dataframe
Field_df=pd.DataFrame({"Tomato_ID": Individual_Tomatoes,
                       "Plant_ID": Individual_Plants[0:Individual_Tomatoes.size],
                       "Pick_ID": Pick_Random[0:Individual_Tomatoes.size],
                       "Weight": Tomato_weight,
                       "Harvester" : 0,
                       "CFU": 0,
                       "Location": 1,
                  })


#Harvest
   
Field_df = Harvesting_Function(df = Field_df, Total_Harvesters = Total_Harvesters, 
                               Tomatoes_Per_Bucket = Tomatoes_Per_Bucket,
                               Tomato_Sequence =Tomato_Sequence,
                               Pick_No = 2)

#Contamination if harvesterter is contaminated. 
Field_df = Harvester_Cont_Function(df =Field_df , Hazard_Level = 100_000, Pick_No = 2, Cont_Harvester_No = 12)


#Contamination Scenarios: 
#1. Bird Droppings
#Percent of total tomatoes contaminated by bird droppings? 

Field_df = field_cont_percetage(df = Field_df, percent_cont = 0.1, Hazard_lvl = 50_000, No_Cont_Clusters= 1)

Field_df= field_cont_ntomatoes(df=Field_df, ntomatoes_cont_pclust= 10, Hazard_lvl = 50_000, No_Cont_Clusters = 2)



#Tomato Growth Model. 
def growth_mod_tomatoes(x, Temp, Time):
    #Time in hour
    #Temp in deg celcious
    growth_rate = ((0.026*Temp) - 0.107)**2 # from https://doi.org/10.4315/0362-028X-73.8.1502
    total_growth = growth_rate*Time
    print(total_growth)
    updated_cont = x*(10**total_growth)
    return updated_cont

#df_trial = pd.DataFrame(data={'col1': [1, 4, 6, 2, 7], 'col2': [6, 7, 1, 2, 8]}) 
#df_trial['col1'] = df_trial['col1'].apply(growth_mod_tomatoes, args = (25,10))


Total_Days = N_Pick*Days_Between_Picks
Harvest_Days = []


#%%%
#Basic Information
Tomato_weight = 250/454 #for medium tomato
Tomato_Sequence = int(105_000/Tomato_weight)
Individual_Tomatoes = np.arange(1,Tomato_Sequence)
Tomatoes_Per_Plant = 120
Tomatoes_Per_Bucket = int(32/Tomato_weight)
Tomatoes_per_Bin = int(1000/Tomato_weight)

#total pick information
N_Pick = 3
Days_Between_Picks = 7

#individual sequences for functions
Individual_Plants = np.repeat(np.arange(1,int(np.ceil(Tomato_Sequence/Tomatoes_Per_Plant))),Tomatoes_Per_Plant+1)
Pick_Sequence = list(range(1,N_Pick+1))*(int(np.ceil(Tomato_Sequence/3)))
Pick_Random = random.sample(Pick_Sequence, len(Pick_Sequence))


#Harvest information
Total_Harvesters = 14

#Probabilities

Pr_bird_drop = 0.2 #probability of bird contamination fields
Pr_of_rain = 0.1 #probability that it will rain in a given day
Pr_harvester_cont = 0.05 #probability that a harvester is contmainated
Pr_bucket_cont = 0.05 #probability that a bucket is contaminated
Pr_Bin_cont = 0.05 #probability that a bin is contaminated


#Model
#Creation of the initial dataframe
Field_df=pd.DataFrame({"Tomato_ID": Individual_Tomatoes,
                       "Plant_ID": Individual_Plants[0:Individual_Tomatoes.size],
                       "Pick_ID": Pick_Random[0:Individual_Tomatoes.size],
                       "Weight": Tomato_weight,
                       "Harvester" : 0,
                       "Bucket":0,
                       "Bin": 0,
                       "CFU": 0,
                       "Location": 1,
                  })


Currennt_Pick = 0 

def Harvesting_Function(df, Total_Harvesters, Tomatoes_Per_Bucket,Tomato_Sequence, Pick_No):
    Harvester_Pattern = np.repeat(list(range(1,Total_Harvesters+1)),Tomatoes_Per_Bucket)
    Harvester_Pattern_Full=np.tile(Harvester_Pattern,int(np.ceil(Tomato_Sequence/len(Harvester_Pattern))))
    
    Field_df_1 =df.loc[df['Pick_ID']==Pick_No]
    
    Bin_Pattern =  np.repeat(list(range(1,math.ceil(Field_df_1["Tomato_ID"].size/Tomatoes_per_Bin))), Tomatoes_per_Bin)
    Bin_Pattern_Trimmed = Bin_Pattern[list(range(Field_df_1["Tomato_ID"].size))]
    
    Field_df_1["Harvester"] = Harvester_Pattern_Full[list(range(Field_df_1["Harvester"].size))]
    Field_df_1["Location"] = 2
    
    df.update(Field_df_1)
    return df

Field_df = Harvester_Cont_Function(df =Field_df , Hazard_Level = 100_000, Pick_No = 2, Cont_Harvester_No = 12)

#Deciding which bin will be contmainated. 



for i in range(Total_Days):
    
    
