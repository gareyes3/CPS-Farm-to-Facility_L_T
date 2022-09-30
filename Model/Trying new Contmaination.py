# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 13:33:52 2022

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
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import reload 

import time
#Own Libraries
import Funz_T
import Inputz_T
import Scen_T
import DepInputz

import Funz
import T_Inputz
import InFunz
import ContScen
import Dictionariez_T


def random_chunk(lst, chunk_size):
    nb_chunks = int(math.ceil(len(lst)/chunk_size))
    choice = random.randrange(nb_chunks) # 0 <= choice < nb_chunks
    return lst[choice*chunk_size:(choice+1)*chunk_size]
        #broken
        
def random_chunk2(lst, chunk_size):
    nb_chunks = int(math.ceil(len(lst)/chunk_size))
    choice = random.randrange(nb_chunks) # 0 <= choice < nb_chunks
    #print(choice)
    list_out= lst[choice*chunk_size:(choice+1)*chunk_size]
    while len(list_out)<chunk_size:
        choice = random.randrange(nb_chunks)
        list_out= lst[choice*chunk_size:(choice+1)*chunk_size]
    return list_out
#%%
def field_cont_percetage(df, percent_cont, Hazard_lvl, No_Cont_Clusters):
    #This function contaminated the tomato field randomly based on a cluter of X%. 
    Percent_Contaminated =percent_cont #Percentage of tomatoes contaminated
    Percent_D_Contaminatinated= Percent_Contaminated/100 #Percentage in decimal point
    Hazard_lvl = Hazard_lvl #CFUs in contaminated area total Cells
    No_Cont_Clusters = No_Cont_Clusters #in how many clusters will the percentage and cont be split into
    No_Cont_PartitionUnits = int((len(df[(df["Location"]==1) & (df["Rej_Acc"]=="Acc") ]))*Percent_D_Contaminatinated) #how many tomatoes are contmainated based on percentage
    Field_df_1 =df.loc[(df["Location"]==1) & (df["Rej_Acc"]=="Acc")].copy() #filtering main df into only those that are in a field
    
    if len(Field_df_1)>0: #The field is only contamiated if the Product is still in accepted condition
    #Determining the hazard level per cluster
        Hazard_lvl_percluster= Hazard_lvl / No_Cont_Clusters #(No_Cont_PartitionUnits*No_Cont_Clusters)
        for i in range(0,No_Cont_Clusters):
            random_Chunky = list(random_chunk(lst = Field_df_1.index, chunk_size = No_Cont_PartitionUnits)) #creating random chunk
            Contamination_Pattern = rng.multinomial(Hazard_lvl_percluster,[1/No_Cont_PartitionUnits]*No_Cont_PartitionUnits,1) #spliting cont into chunks length
            Field_df_1.loc[random_Chunky, "CFU"] = Field_df_1.loc[random_Chunky, "CFU"] + Contamination_Pattern[0] #adding contmaination
            
    df.update(Field_df_1)
    
    return df




Field_df=pd.DataFrame({"Tomato_ID": Inputz_T.Individual_Tomatoes,
                   "Plant_ID": Inputz_T.Individual_Plants[0:Inputz_T.Individual_Tomatoes.size],
                   "Pick_ID": Inputz_T.Pick_Random[0:Inputz_T.Individual_Tomatoes.size],
                   "Weight": Inputz_T.Tomato_weight,
                   "Harvester" : 0,
                   "Bucket":0,
                   "Bin": 0,
                   "Case_PH": 0,
                   "CFU": 0,
                   "CFU_BRej":"",
                   "Location": 1,
                   'PositiveSamples':"",
                   "Rej_Acc" :"Acc"
              })

Field_df.PositiveSamples = [list() for x in range(len(Field_df.index))]
#print(time.time() - start_df, "df Creation")
        

Field_df["CFU"] = 1000


Field_df['Location'] = np.random.choice(list([1,2,3]), len(Field_df))


def field_cont_percetage2(df, percent_cont, Hazard_lvl,No_Cont_Clusters):
    No_Cont_Clusters = 1
    #This function contaminated the tomato field randomly based on a cluter of X%. 
    Percent_Contaminated =percent_cont #Percentage of tomatoes contaminated
    Percent_D_Contaminatinated= Percent_Contaminated/100 #Percentage in decimal point
    Hazard_lvl = Hazard_lvl #CFUs in contaminated area total Cells
    
    No_Cont_PartitionUnits= int(len(df)*Percent_D_Contaminatinated)
    Field_df_1 =df.loc[(df["Location"]==1) & (df["Rej_Acc"]=="Acc")].copy()
    
    if len(Field_df_1)>0:
        Hazard_lvl_percluster= Hazard_lvl / No_Cont_Clusters #(No_Cont_PartitionUnits*No_Cont_Clusters)
        for i in range(0,No_Cont_Clusters):
            random_Chunky = np.array(random_chunk(lst = Field_df.index, chunk_size = No_Cont_PartitionUnits)) #creating random chunk
            Contamination_Pattern = rng.multinomial(Hazard_lvl_percluster,[1/No_Cont_PartitionUnits]*No_Cont_PartitionUnits,1) #spliting cont into chunks length
            random_Chunky_s= random_Chunky[np.isin(random_Chunky,np.array(Field_df_1.index))]
            Contamination_Pattern_s = Contamination_Pattern[0][range(0,len(random_Chunky_s))]
            Field_df_1.loc[random_Chunky_s, "CFU"] = Field_df_1.loc[random_Chunky_s, "CFU"] + Contamination_Pattern_s
            #Field_df_1.loc[random_Chunky, "CFU"] = Field_df_1.loc[random_Chunky, "CFU"] + Contamination_Pattern[0] #adding contmaination
            
        df.update(Field_df_1)
        return df
        
Field_df2=field_cont_percetage2(df= Field_df, percent_cont = 1, Hazard_lvl = 100_000,No_Cont_Clusters =2)

Field_df2["CFU"].sum()


###%% New Sampling Plans

##Composite Mash. 
def F_Sampling_T_Mash (df, Pick_No, Location, NSamp_Unit, NoGrab, Subsample_Mass):
    
    df_field_1 =df.loc[(Field_df["Pick_ID"]==1) & (df["Location"]==1)].copy()
    if len(df_field_1)>0:
        #print(Location, "Location")
        #print(df["Location"])
        #Unique_TestUnit = list(df[Test_Unit].unique())
        #Grab_Weight = Partition_Weight #In lb
        #for i in (Unique_TestUnit): #From sublot 1 to sublot n (same for pallet,lot,case etc)
        for l in range (1, NSamp_Unit+1): #Number of samples per sublot or lot or pallet.
            CFU_hh=df_field_1["CFU"]
            #print(len(CFU_hh),"Length")
            List_Random=CFU_hh.sample(n=NoGrab)
            Total_Cells_Mash = sum(List_Random)
            Total_Weight_Mash = Inputz_T.Tomato_weight*NoGrab*454
            Cont_Mash=Total_Cells_Mash/Total_Weight_Mash
            #CFU_grab=np.random.binomial(Total_Cells_Mash,0.0050987)
            
            P_Detection=1-math.exp(-(Cont_Mash*Subsample_Mass))
            RandomUnif = random.uniform(0,1)
            if RandomUnif < P_Detection:
                for i in list(List_Random.index):
                    df_field_1.at[i, 'PositiveSamples'].append(l)
    df.update(df)
    return (df)

Field_df3=F_Sampling_T_Mash (df = Field_df, Pick_No = 1, Location = 1, NSamp_Unit = 1, NoGrab = 20, Subsample_Mass = 25)




