# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 10:09:49 2021

@author: gareyes3
"""
import math
import random

def F_Sampling_2 (df, Test_Unit, NSamp_Unit, Samp_Size, Partition_Weight, NoGrab):
    Unique_TestUnit = list(df[Test_Unit].unique())
    Grab_Weight = Samp_Size/NoGrab
    for i in (Unique_TestUnit):
        for l in range (NSamp_Unit):
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


df_2 =F_Sampling_2(df = df, Test_Unit = "Sublot", NSamp_Unit = 10, Samp_Size =30, Partition_Weight =1000, NoGrab= 60)

def F_Rejection_Rule2 (df, Test_Unit, limit):
    #Test_Unit = "Lot" or "Sublot"
    Listpositive = []
    for i, row in df.iterrows():
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

import pandas as pd


