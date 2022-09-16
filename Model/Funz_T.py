# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 12:15:05 2022

@author: gareyes3
"""

#Funz_T
import numpy as np
import pandas as pd
import random 
import math
from numpy.random import Generator, PCG64
rng = Generator(PCG64())
import matplotlib.pyplot as plt
import seaborn as sns


#%%

#This function create a random chunk of X rows in a dataframe (each row in this mdoel represents one individual tomato)
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

def field_cont_ntomatoes(df, ntomatoes_cont_pclust, Hazard_lvl, No_Cont_Clusters):
    #This function contaminated the tomato field randomly based on a cluter of X%. 
    Hazard_lvl = Hazard_lvl #CFUs in contaminated area total Cells
    No_Cont_Clusters = No_Cont_Clusters #in how many clusters will the percentage and cont be split into
    No_Cont_PartitionUnits = ntomatoes_cont_pclust #how many tomatoes are contmainated per cluster
    Field_df_1 =df.loc[(df["Location"]==1) & (df["Rej_Acc"]=="Acc")].copy()  #filtering main df into only those that are in a field
    
    if len(Field_df_1)>0: 
        #Determining the hazard level per cluster
        Hazard_lvl_percluster= Hazard_lvl / No_Cont_Clusters #(No_Cont_PartitionUnits*No_Cont_Clusters)
        for i in range(0,No_Cont_Clusters):
            random_Chunky = list(random_chunk2(lst = Field_df_1.index, chunk_size = No_Cont_PartitionUnits)) #creating random chunk
            Contamination_Pattern = rng.multinomial(Hazard_lvl_percluster,[1/No_Cont_PartitionUnits]*No_Cont_PartitionUnits,1) #spliting cont into chunks length
            Field_df_1.loc[random_Chunky, "CFU"] = Field_df_1.loc[random_Chunky, "CFU"] + Contamination_Pattern[0] #adding contmaination

    df.update(Field_df_1)
    
    return df

def Harvesting_Function(df, Total_Harvesters, Tomatoes_Per_Bucket,Tomato_Sequence, Pick_No, Tomatoes_per_Bin):
    Harvester_Pattern = np.repeat(list(range(1,Total_Harvesters+1)),Tomatoes_Per_Bucket)
    Harvester_Pattern_Full=np.tile(Harvester_Pattern,int(np.ceil(Tomato_Sequence/len(Harvester_Pattern))))
    
    Field_df_1 =df.loc[(df['Pick_ID']==Pick_No) & (df['Rej_Acc']== "Acc") ].copy()
    
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
    Field_df_1.loc[:,"CFU"] = cont_pattern[0]
    df.update(Field_df_1)
    return df

def Bin_Cont_Function(df, Hazard_Level, Pick_No, Cont_Bin_No):
    Field_df_1 =df.loc[(df['Pick_ID']==Pick_No) & (df['Bin'] == Cont_Bin_No)]
    Size_1 = Field_df_1['Bin'].size
    cont_pattern=rng.multinomial(Hazard_Level,[1/Size_1]*Size_1,1) 
    Field_df_1.loc[:,"CFU"] = cont_pattern[0]
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

def Survival_Salmonella_cucum2(Series,Time, RH, Temp):
    #time  in H
    #model obtained fromhttps://www.sciencedirect.com/science/article/pii/S0740002021001052#fig4
    Log_Change_7= 4.48385-0.00199*(Temp)*RH
    Day_Log_h = Log_Change_7/24/7 #Change in log CFU per hour
    total_change = -(Day_Log_h*Time)
    
    if total_change>=0:
        GrowthCeil = math.ceil(total_change)
        Difference = total_change-GrowthCeil
        MaxCont = Series*10**GrowthCeil
        Updated_CFUs = rng.binomial(MaxCont,10**Difference)
    else:
        Updated_CFUs= rng.binomial(Series,10**total_change)
    
    return Updated_CFUs


def applying_survival_salmonella_cucum2(df, Time, RH, Temp, Location):
    
    df_field_1 =df.loc[(df["Location"]==Location)].copy()
    

    
    df_field_1.loc[:,"CFU"] = Survival_Salmonella_cucum2(df_field_1["CFU"],
                                   Time= Time, 
                                   RH = RH, 
                                   Temp = Temp)
    
    df.update(df_field_1)
    return df


def applying_survival_salmonella_cucum(df, Time, RH, Temp, Location):
    
    df_field_1 =df.loc[(df["Location"]==Location)].copy()


    df_field_1.loc[:,"CFU"]=df_field_1["CFU"].apply(func= Survival_Salmonella_cucum, 
                                                Time = Time,
                                                RH = RH,
                                                Temp = Temp)
    df.update(df_field_1)
    return df


def Tomato_Wash(df, Location, FC_lvl):

    #FC_lvl = np.random.triangular(0,5,10)
    if FC_lvl<10:
        log_red_Wash_mean = (FC_lvl*0.04)+0.3
    elif FC_lvl>10:
        log_red_Wash_mean = (FC_lvl*0.0056)+0.5952
        
    logred_sd = 0.175
    
    logred_cont = np.random.normal(log_red_Wash_mean, logred_sd)
    
    #Transfer to uncontaminated pieces. 
    Log_Trans_Upper = (-0.6798*FC_lvl)-0.6003
    Log_Trans_Lower = (-1.3596*FC_lvl)-0.6
    
    Field_df_1 =df.loc[df["Location"]==Location].copy() #location 4 is wash water
    Field_df_1_conts = Field_df_1["CFU"].copy()
    
    Tras_old= 0
    
    for i in list(Field_df_1_conts.index):
        #Parameters from https://www.sciencedirect.com/science/article/pii/S0963996916306081#f0010
        #Maffei. 
        #Backup https://www.sciencedirect.com/science/article/pii/S0740002019309694?casa_token=dt-V4Cbh89YAAAAA:FoQTt7f3Hly2-k9lJjUXPqkZ-W5tJChevsm2XIz3UTimqrYdUT9zAoqZUQlZWx1OhENvX3zqpqw
        Cont = Field_df_1_conts[i]
        
        logred_cont = -np.random.normal(log_red_Wash_mean, logred_sd)
        Percent_Trans = 10**np.random.uniform(Log_Trans_Lower,Log_Trans_Upper)
        
        if logred_cont>=0:
            GrowthCeil = math.ceil(logred_cont)
            Difference = logred_cont-GrowthCeil
            MaxCont = Cont*10**GrowthCeil
            Updated_CFUs = rng.binomial(MaxCont,10**Difference)
        else:
            Updated_CFUs= rng.binomial(Cont,10**logred_cont)
    
        Reduction = Updated_CFUs
        
        if i == 0:
            Field_df_1_conts[i] = Reduction
        if i >0:
            Field_df_1_conts[i] = Reduction + Tras_old
        Cont = Field_df_1_conts[i]
        Transfer = rng.binomial(Cont,Percent_Trans)
        Tras_old = Transfer
        
    Field_df_1.loc[:, "CFU"] = Field_df_1_conts
    df.update(Field_df_1)
    return df


def F_CrossContProLine_tom (df, Tr_P_S, Tr_S_P,  Location, Sanitation_Freq_lb = 0, StepEff = 0 , compliance = 0):
        df_field_1 =df.loc[df["Location"]==Location].copy()
        rateweight = 0.57
        every_x_many = int(Sanitation_Freq_lb/rateweight)
        ContS=0
        vectorCFU = df_field_1["CFU"].copy()
        index_vec = np.array(vectorCFU.index)
        vectorCFU = np.array(vectorCFU)
        newvector=[]
        if every_x_many > 0:
            Cleaning_steps = np.arange(0, len(vectorCFU) , every_x_many )
        for i in index_vec:
            if compliance>0: #to not run if there is no sanitation.
                if random.uniform(0,1)<compliance:
                    if every_x_many > 0:
                        if i in Cleaning_steps:
                            ContS = ContS*10**StepEff
                            print ("cleaned")
            ContP = vectorCFU[i] #Contamination product
            TotTr_P_S= rng.binomial(ContP,Tr_P_S) #Transfer from Product to Surfaces
            TotTr_S_P = rng.binomial(ContS,Tr_S_P) #Trasnfer from Surfaces to product
            ContPNew = ContP-TotTr_P_S+TotTr_S_P #New Contmination on Product
            ContS=ContS+TotTr_P_S-TotTr_S_P #Remiining Contamination in Surface for upcoming batches
            newvector.append(ContPNew)
        df_field_1.loc[:,"CFU"] = newvector
        df.update(df_field_1)
        return df
    

def Case_Packaging(df,Case_Weight,Tomato_Weight, Location):
    
    df_field_1 =df.loc[df["Location"]==Location].copy()
    
    Tomatoes_Case = math.ceil(Case_Weight/Tomato_Weight)
    Total_Packages = len(df_field_1.index)
    Total_Cases = math.ceil(Total_Packages/Tomatoes_Case)
    Case_Pattern = [i for i in range(1, int(Total_Cases)+1) for _ in range(Tomatoes_Case)]
    Crop_No = len(df_field_1.index)
    Case_Pattern=Case_Pattern[:Crop_No]
    df_field_1.loc[:,"Case_PH"] = Case_Pattern
    
    df.update(df_field_1)
    return df

def Update_Location(df, Previous, NewLoc):
    df_field_1 =df.loc[df["Location"]==Previous].copy()
    df_field_1.loc[:,"Location"] =NewLoc
    df.update(df_field_1)
    return df


#Sampling Function

def F_Sampling_T (df, Pick_No, Location, NSamp_Unit, NoGrab):
    
    df_field_1 =df.loc[(df["Pick_ID"]==Pick_No) & (df["Location"]==Location)].copy()
    if len(df_field_1)>0:
        #print(Location, "Location")
        #print(df["Location"])
        #Unique_TestUnit = list(df[Test_Unit].unique())
        #Grab_Weight = Partition_Weight #In lb
        #for i in (Unique_TestUnit): #From sublot 1 to sublot n (same for pallet,lot,case etc)
        for l in range (1, NSamp_Unit+1): #Number of samples per sublot or lot or pallet.
            for j in range(NoGrab):
                CFU_hh=df_field_1["CFU"]
                #print(len(CFU_hh),"Length")
                List_Random=CFU_hh.sample(n=1)
                CFU = List_Random
                Index = List_Random.index[0]
                CFU_grab = CFU#*(Grab_Weight/(Partition_Weight*454))
                P_Detection=1-math.exp(-CFU_grab)
                RandomUnif = random.uniform(0,1)
                if RandomUnif < P_Detection:
                    df_field_1.at[Index, 'PositiveSamples'].append(l)
        df.update(df_field_1)
    return (df)

def F_Rejection_Rule_T (df, Pick_No, Av_Picks, Test_Unit, limit):
    #Unique_Test_Unit =list(df[Test_Unit].unique())
    df_field_1 =df.loc[(df["Pick_ID"].isin(Av_Picks))].copy()
    Reject = []
    #for  i in Unique_Test_Unit:
    df_Subset = df_field_1[df_field_1[Test_Unit] == Pick_No].copy()
    List_of_grabs = df_Subset['PositiveSamples'].tolist()
    flat_list = [item for sublist in  List_of_grabs for item in sublist]
    Unique_Positives =list(np.unique(flat_list))
    if len(Unique_Positives)>limit:
        Reject.append(Test_Unit)
    df_field_1.PositiveSamples = [list() for x in range(len(df_field_1.index))] #this is in case everything gets rejected
    if len(Reject)>0:
     df_field_1.loc[:,"Rej_Acc"] = "REJ"
     df_field_1.loc[:,"CFU_BRej"] = df_field_1["CFU"]
     df_field_1.loc[:,"CFU"] = 0
     
        #df_Blank = df.iloc[[0]]
        #df_Blank.loc[:, ['CFU']] = 0
        #df_Blank.loc[:, ['Weight']] = SCInputz.Partition_Weight
        #df_Blank.loc[:, ['Accept']] = "All Rej"
        #df = df_Blank
    #else:
        #df = df[~df[Test_Unit].isin(Reject)]
    df.update(df_field_1)
    return df