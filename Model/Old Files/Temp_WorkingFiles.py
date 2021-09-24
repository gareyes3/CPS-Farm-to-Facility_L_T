# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 09:03:08 2021

@author: gareyes3
"""
import Funz
import Inputz
import math
import random
import numpy as np


#New Sampling Function
def F_Sampling_2 (df, Test_Unit, NSamp_Unit, Samp_Size, Partition_Weight, NoGrab):
    Unique_TestUnit = list(df[Test_Unit].unique())
    Grab_Weight = Samp_Size/NoGrab
    for i in (Unique_TestUnit): #From sublot 1 to sublot n (same for pallet,lot,case etc)
        for l in range (1, NSamp_Unit+1): #Number of samples per sublot or lot or pallet.
            for j in range(NoGrab):
                Sampled_Grab =df[df[Test_Unit] == i].sample(1, replace= True)
                Index = Sampled_Grab.index
                Index = Index[0]
                CFU = Sampled_Grab["CFU"]
                CFU_grab = CFU*(Grab_Weight/(Partition_Weight*454))
                P_Detection=1-math.exp(-CFU_grab)
                RandomUnif = random.uniform(0,1)
                if RandomUnif < P_Detection:
                    df.at[Index, 'Grabs']. append(l)
    return (df)


list(range (1,10+1))

df = F_Sampling_2(df =df,Test_Unit ="Sublot", 
                      NSamp_Unit = 10, 
                      Samp_Size =Inputz.sample_size_PH, 
                      Partition_Weight =Inputz.Partition_Weight, 
                      NoGrab =Inputz.No_Grabs_PH )

for row in j.itertuples():
            i  = row[0]

#New Rejection Function
def F_Rejection_Rule2 (df, Test_Unit, limit):
    #Test_Unit = "Lot" or "Sublot"
    Listpositive = []
    for row in df.itertuples():
        i = row[0]
        Positives = len(set(df.at[i, "Grabs"]))
        Listpositive.append(Positives)
    df.Positives =Listpositive
    Positives = df[df["Positives"]> limit]
    Unique_TestUnit=list(df[Test_Unit].unique())
    Unique_Positives = list(Positives[Test_Unit].unique())
    df.Positives = ""
    df.Grabs = [list() for x in range(len(df.index))]
    if set(Unique_TestUnit)<= set(Unique_Positives):
        df_Blank = df.iloc[[0]]
        df_Blank.loc[:, ['CFU']] = 0
        df_Blank.loc[:, ['Weight']] = 1000
        df_Blank.loc[:, ['Accept']] = "All Rej"
        df = df_Blank
    else:
        df = df[~df[Test_Unit].isin(Unique_Positives)]
    return df

def F_Rejection_Rule3 (df, Test_Unit, limit):
    Unique_Test_Unit =list(df[Test_Unit].unique())
    Reject = []
    for  i in Unique_Test_Unit:
        df_Subset = df[df[Test_Unit] == i]
        List_of_grabs = df_Subset['Grabs'].tolist()
        flat_list = [item for sublist in  List_of_grabs for item in sublist]
        Unique_Positives =list(np.unique(flat_list))
        if len(Unique_Positives)>limit:
            Reject.append(i)
    df.Grabs = [list() for x in range(len(df.index))]
    if set(Unique_Test_Unit)<= set(Reject):
        df_Blank = df.iloc[[0]]
        df_Blank.loc[:, ['CFU']] = 0
        df_Blank.loc[:, ['Weight']] = 1000
        df_Blank.loc[:, ['Accept']] = "All Rej"
        df = df_Blank
    else:
        df = df[~df[Test_Unit].isin(Reject)]
    return df



    
df3 = F_Rejection_Rule3 (df =df, Test_Unit= "Sublot", limit = 0)
