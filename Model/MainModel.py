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
    Field_df_1 =df.loc[df["Location"]==1].copy() #filtering main df into only those that are in a field
    
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
    Field_df_1 =df.loc[df["Location"]==1].copy() #filtering main df into only those that are in a field
    
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
    
    Field_df_1 =df.loc[df['Pick_ID']==Pick_No].copy()
    
    Bin_Pattern =  np.repeat(list(range(1,math.ceil(Field_df_1["Tomato_ID"].size/Tomatoes_per_Bin)+1)), Tomatoes_per_Bin)
    Bin_Pattern_Trimmed = Bin_Pattern[list(range(1,Field_df_1["Tomato_ID"].size+1))]
    
    Field_df_1.loc[:,"Harvester"] = Harvester_Pattern_Full[list(range(Field_df_1["Harvester"].size))]
    Field_df_1.loc[:,"Location"] = 2
    Field_df_1.loc[:,"Bin"] = Bin_Pattern_Trimmed
    
    df.update(Field_df_1)
    return df

def Harvester_Cont_Function(df, Hazard_Level, Pick_No, Cont_Harvester_No):
    Field_df_1 =df.loc[(df['Pick_ID']==Pick_No) & (df['Harvester'] == Cont_Harvester_No )]
    Size_1 = Field_df_1['Harvester'].size
    cont_pattern=rng.multinomial(Hazard_Level,[1/Size_1]*Size_1,1) 
    Field_df_1.loc["","CFU"] = cont_pattern[0]
    df.update(Field_df_1)
    return df

def Bin_Cont_Function(df, Hazard_Level, Pick_No, Cont_Bin_No):
    Field_df_1 =df.loc[(df['Pick_ID']==Pick_No) & (df['Bin'] == Cont_Bin_No)]
    Size_1 = Field_df_1['Bin'].size
    cont_pattern=rng.multinomial(Hazard_Level,[1/Size_1]*Size_1,1) 
    Field_df_1.loc["","CFU"] = cont_pattern[0]
    df.update(Field_df_1)
    return df


#Tomato Growth Model

#Tomato Growth Model. 
def growth_mod_tomatoes(x, Temp, Time):
    #Time in hour
    #Temp in deg celcious
    growth_rate = ((0.026*Temp) - 0.107)**2 # from https://doi.org/10.4315/0362-028X-73.8.1502
    total_growth = growth_rate*Time
    print(total_growth)
    updated_cont = x*(10**total_growth)
    return updated_cont


def die_off_tomatoes(x ,Time):
    Time_d =  Time/24
    #Time in hours
    die_off_rate = 0.5 #log  CFU/days
    total_die_off = die_off_rate*Time_d
    #updated_cont = x*(10**-total_die_off)
    
    updated_cont = rng.binomial(x,10**-total_die_off)
    return updated_cont


def applying_dieoff(df,Time):
    df.loc[:,"CFU"]=df["CFU"].apply(func=die_off_tomatoes, Time = Time)
    return df


def Survival_Salmonella_cucum(x,Time, RH, Temp):
    #time  in H
    
    #model obtained fromhttps://www.sciencedirect.com/science/article/pii/S0740002021001052#fig4
    Log_Change_7= 4.48385-0.00199*(Temp)*RH
    Day_Log_h = Log_Change_7/24/7 #Change in log CFU per hour
    
    total_change = -(Day_Log_h*Time)
    
    if total_change>=0:
        GrowthCeil = math.ceil(total_change)
        Difference = total_change-GrowthCeil
        MaxCont = x*10**GrowthCeil
        Updated_CFUs = rng.binomial(MaxCont,10**Difference)
    else:
        Updated_CFUs= rng.binomial(x,10**total_change)
    
    return Updated_CFUs



def applying_survival_salmonella_cucum(df, Time, RH, Temp):
    df.loc[:,"CFU"]=df["CFU"].apply(func= Survival_Salmonella_cucum, 
                                                Time = Time,
                                                RH = RH,
                                                Temp = Temp)
    return df




#%%%
#Basic Information
Tomato_weight = 260/454 #for medium tomato
Tomato_Sequence = int(132_000/Tomato_weight)
Individual_Tomatoes = np.arange(1,Tomato_Sequence)
Tomatoes_Per_Plant = 120
Tomatoes_Per_Bucket = int(32/Tomato_weight)
Bin_Weight = 1000
Tomatoes_per_Bin = math.ceil(Bin_Weight/Tomato_weight)

#total pick information
N_Pick = 3
Days_Between_Picks = 7
Days = np.arange(1, (N_Pick*Days_Between_Picks)+1)
Harvest_Days = [7,14,21]
PHS_Days = [4,11,18]

#individual sequences for functions
Individual_Plants = np.repeat(np.arange(1,int(np.ceil(Tomato_Sequence/Tomatoes_Per_Plant))),Tomatoes_Per_Plant+1)
Pick_Sequence = list(range(1,N_Pick+1))*(int(np.ceil(Tomato_Sequence/3)))
Pick_Random = random.sample(Pick_Sequence, len(Pick_Sequence))


#Harvest information
Total_Harvesters = 55
Total_Bins = 44
#Probabilities

Pr_bird_drop = 0.2 #probability of bird contamination fields
Pr_of_rain = 0.1 #probability that it will rain in a given day
Pr_harvester_cont = 0.05 #probability that a harvester is contmainated
Pr_bucket_cont = 0.05 #probability that a bucket is contaminated
Pr_Bin_cont = 0.05 #probability that a bin is contaminated


#Contamination Scenario
    #Small Cluster
Total_Hazard = 100_000


#Processing Factors
RH_Florida= 74.5
#From the Field to the Shipping Center
Temp_F_Sc = 25 #C need to parametrize
Time_F_Sc = 0.5 #hr

#Shipping Center Storage
Temp_Sc = 25
Time_Sc = 2 #hr

#Shipping Center to packing
Temp_Sc_Pack = 25
Time_Sc_Pack = 2 #hr

#Packer Storage
Temp_Pack = 25
Time_Pack = 4 #hr

    
#%%
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


#%%

Cont_Scenario = 1
    #1 = Rainfall event  (uniform contamination)
    #2 = Bird feces, 0.01 percent of fieldl contaminaated (point source contamination)
    #3 = harvester / bucket contamination, small clusters spread throughout the field
    #4 = Bins , medium size clusters spread across the field. 
    
    

#Simulating Days
Current_Pick = 1

#Contaminated Bin

for i in Days:
    #Contmaination Event Due to Rain
    if (np.random.uniform(0,1)<Pr_of_rain):
        #This function contaminated the field uniformly. 100% of the field cont. 
        Field_df = field_cont_percetage(df = Field_df, 
                                        percent_cont = 100,
                                        Hazard_lvl = Total_Hazard, 
                                        No_Cont_Clusters = 1)
        #Contaminated field with Rain
        print("Field Cont with Rain")
    
    #Contmaination Event Due to Rain
    if (np.random.uniform(0,1)<Pr_bird_drop):
        #Contaminated field with 0.1% contamination, simulated bird droping. 
        Field_df = field_cont_percetage(df = Field_df, 
                                        percent_cont = 0.1,
                                        Hazard_lvl = Total_Hazard, 
                                        No_Cont_Clusters = 1)
        print("Field Cont with Bird Dropping")
    
    if i in PHS_Days:
        
    
    #This is where process starts, along with simulated harvest. 
    if i in Harvest_Days:
        print("The product was harvested")
        Field_df = Harvesting_Function(df = Field_df, Total_Harvesters = Total_Harvesters, 
                                      Tomatoes_Per_Bucket = Tomatoes_Per_Bucket,
                                      Tomato_Sequence = Tomato_Sequence, 
                                      Pick_No = Current_Pick)
        #Harvester contmaination
        if (np.random.uniform(0,1)<Pr_harvester_cont):
            #Picking the contaminated harvester at random
            Contam_Harvester = random.sample(list(range(1,Total_Harvesters+1)),1)[0]
            #applying the contmainated harvester function to the Data. 
            Field_df =Harvester_Cont_Function(df = Field_df,
                                    Hazard_Level = 100_000, 
                                    Pick_No =Current_Pick  , 
                                    Cont_Harvester_No =Contam_Harvester )
            
       #Bin Contmaination
        if (np.random.uniform(0,1)<Pr_Bin_cont):
            #Picking the contaminated harvester at random
            Contam_Bin = random.sample(list(range(1,Total_Bins+1)),1)[0]
            #applying the contmainated harvester function to the Data. 
            Field_df =Bin_Cont_Function(df = Field_df,
                                    Hazard_Level = 100_000, 
                                    Pick_No =Current_Pick  , 
                                    Cont_Bin_No = Contam_Bin )
        
        #Establishing which pick we are int
        Current_Pick = Current_Pick+1
        
        #Transportation from the field to the shipping center
        #Here we need to caculate die-off for the tranportation of growth due to transportation. 
        Field_df = applying_survival_salmonella_cucum(df = Field_df , 
                                                      Time = Time_F_Sc,
                                                      RH = RH_Florida,
                                                      Temp = Temp_F_Sc)
        
        #At Shipping center, temporary storage in open bins
        Field_df = applying_survival_salmonella_cucum(df = Field_df , 
                                                      Time = Time_Sc,
                                                      RH = RH_Florida,
                                                      Temp = Temp_Sc)
        
        #From shipping center to packing facility.
        Field_df = applying_survival_salmonella_cucum(df = Field_df , 
                                                      Time = Time_Sc_Pack,
                                                      RH = RH_Florida,
                                                      Temp = Temp_Sc_Pack)
        
        #Temporary Storage in Packing Facility
        Field_df = applying_survival_salmonella_cucum(df = Field_df , 
                                                      Time = Time_Pack,
                                                      RH = RH_Florida,
                                                      Temp = Temp_Pack)
        
        #Processing
        #Wasing. 
        


#%%


Field_df = applying_survival_salmonella_cucum(df = Field_df , 
                                              Time = 24,
                                              RH = 100,
                                              Temp = 21)
