# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 09:26:20 2021

@author: Gustavo Reyes
"""
import pandas as pd
import numpy as np
import scipy.stats as stats
import math
import os
import random
import seaborn as sns
from matplotlib import pyplot as plt
import Funz
from itertools import cycle


#Total Cells in Unit

CFU = 10
weight =1000
sampweight = 100 #g
Z_1 =sampweight/weight
Z_2=CFU*Z_1

P_Detection=1-math.exp(-Z_2)


def F_SamplingSlots (df,NLots,NoSampleLot,sample_size,Cluster_Unit_weight, Limit, Grabs ):
    Results=[]
    Uniquesublots =list(df.Sublot.unique())
    for i in (Uniquesublots):
        Reject_Lis=[]
        for l in range (NoSampleLot):
            Sampled_Grabs =df[df.Sublot == i].sample(Grabs, replace= True)
            Sampled_Grabs =list(Sampled_Grabs.CFU)
            Grab_Weight = sample_size/Grabs
            Detected = []
            for j in Sampled_Grabs: 
                CFU_grab = j*(Grab_Weight/(Cluster_Unit_weight*454))
                P_Detection=1-math.exp(-CFU_grab)
                if random.uniform(0,1)<P_Detection:
                    Reject_YN=1
                else:
                    Reject_YN=0
                Detected.append(Reject_YN)
                if sum(Detected)>0:
                    Detected_YN = 1
                elif sum(Detected) ==0:
                    Detected_YN =0
        Reject_Lis.append(Detected_YN)
        print(Reject_Lis)
        a=sum(Reject_Lis)
        if a > Limit:
            AR= False
        else:
            AR= True
        Results.append(AR)
        print("Results",Results)
    data1 =  {'slot_number': Uniquesublots,
           'Accept_Reject': Results}
    dT = pd.DataFrame(data1)
    dT= dT.loc[dT['Accept_Reject'] == False]
    ListR= list(dT.slot_number)
    return(ListR)

def F_Sampling(df,Test_Unit,NSamp_Unit,Samp_Size, Clust_Weight, Limit, NoGrab ):
    Results=[]
    Unique_TestUnit=list(df[Test_Unit].unique())
    for i in (Unique_TestUnit):
        Reject_Lis=[]
        for l in range (NSamp_Unit):
            Sampled_Grabs =df[df[Test_Unit] == i].sample(NoGrab, replace= True)
            Sampled_Grabs =list(Sampled_Grabs.CFU)
            Grab_Weight = Samp_Size/NoGrab
            Detected = []
            for j in Sampled_Grabs: 
                CFU_grab = j*(Grab_Weight/(Clust_Weight*454))
                P_Detection=1-math.exp(-CFU_grab)
                if random.uniform(0,1)<P_Detection:
                    Reject_YN=1
                else:
                    Reject_YN=0
                Detected.append(Reject_YN)
                if sum(Detected)>0:
                    Detected_YN = 1
                elif sum(Detected) ==0:
                    Detected_YN =0
        Reject_Lis.append(Detected_YN)
        print(Reject_Lis)
        a=sum(Reject_Lis)
        if a > Limit:
            AR= False
        else:
            AR= True
        Results.append(AR)
        print("Results",Results)
    data1 =  {Test_Unit: UniquePallets,
           'Accept_Reject': Results}
    dT = pd.DataFrame(data1)
    dT= dT.loc[dT['Accept_Reject'] == False]
    ListR= list(dT[Test_Unit])
    return(ListR)


df[1,'Weight']


Rest_11 = F_SamplingSlots(df=df, NLots= slot_number , NoSampleLot = 1, sample_size =sample_size_H ,Cluster_Unit_weight = Cluster_Unit_weight , Limit = 0, Grabs = 60)
Rest_12 = F_Sampling(df = df,Test_Unit = "Sublot", NSamp_Unit = slot_number, Samp_Size = 300, Clust_Weight =Cluster_Unit_weight , Limit =0, NoGrab=60)


Column = 'Sublot'
df[Column]
UniquePallets=list(df[Column].unique())

def F_Sampling(df,Test_Unit, NSamp_Unit, Samp_Size, Clust_Weight, Limit, NoGrab ):
    Results=[]
    Unique_TestUnit=list(df[Test_Unit].unique())
    for i in (Unique_TestUnit):
        Reject_Lis=[]
        for l in range (NSamp_Unit):
            Sampled_Grabs =df[df[Test_Unit] == i].sample(NoGrab, replace= True)
            Sampled_Grabs =list(Sampled_Grabs.CFU)
            Grab_Weight = Samp_Size/NoGrab
            Detected = []
            for j in Sampled_Grabs: 
                CFU_grab = j*(Grab_Weight/(Clust_Weight*454))
                P_Detection=1-math.exp(-CFU_grab)
                if random.uniform(0,1)<P_Detection:
                    Reject_YN=1
                else:
                    Reject_YN=0
                Detected.append(Reject_YN)
                if sum(Detected)>0:
                    Detected_YN = 1
                elif sum(Detected) ==0:
                    Detected_YN =0
        Reject_Lis.append(Detected_YN)
        print(Reject_Lis)
        a=sum(Reject_Lis)
        if a > Limit:
            AR= False
        else:
            AR= True
        Results.append(AR)
        print("Results",Results)
    data1 =  {Test_Unit: Unique_TestUnit,
           'Accept_Reject': Results}
    dT = pd.DataFrame(data1)
    dT= dT.loc[dT['Accept_Reject'] == False]
    ListR= list(dT[Test_Unit])
    return(ListR)

def F_SamplingFProd (df, Test_Unit, N_SampPacks, Clust_Weight, Grab_Weight):
    Results=[]
    Clust_Weight = df.loc[1,"Weight"]
    Sampled_Packs = list(df[Test_Unit].sample(N_SampPacks))
    for i in Sampled_Packs:
        CFU = df.loc[df['PackNo'] == i, 'CFU'].values[0]
        CFU_grab = CFU*(Grab_Weight/(Clust_Weight*454))
        P_Detection=1-math.exp(-CFU_grab)
        if random.uniform(0,1)<P_Detection:
            Reject_YN=1
        else:
            Reject_YN=0
        Results.append(Reject_YN)
    return Results

    
df33= F_SamplingFProd(df=df2, Test_Unit='PackNo', N_SampPacks=10, Clust_Weight=454, Grab_Weight= 10)  


n = random.randint(0,len(df.index)-5)
five_random_consecutive_rows = df[n:n+5]



thold = 1
Reduction = (thold/2.45/24)**0.3
print(Reduction)
