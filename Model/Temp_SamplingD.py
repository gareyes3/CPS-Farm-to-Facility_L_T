# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 15:12:54 2021

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
                print(Index)
                CFU = Sampled_Grab["CFU"]
                CFU_grab = CFU*(Grab_Weight/(Partition_Weight*454))
                P_Detection=1-math.exp(-CFU_grab)
                RandomUnif = random.uniform(0,1)
                if RandomUnif <P_Detection:
                    df.at[Index, 'Grabs']  = NewGrabs
    return (df)


df2 = F_Sampling_2(df = df, 
                        Test_Unit = "Sublot", 
                        NSamp_Unit = 2, 
                        Samp_Size = 300, 
                        Partition_Weight = 1000, 
                        NoGrab = 60)


df.at[1, 'Grabs']  = queso


#New Sampling Function
def F_Sampling_2 (df, Test_Unit, NSamp_Unit, Samp_Size, Partition_Weight, NoGrab, Limit):
    if Limit == 0:
        Unique_TestUnit = list(df[Test_Unit].unique())
        Grab_Weight = Samp_Size/NoGrab
        for i in (Unique_TestUnit):
            for l in range (NSamp_Unit):
                for j in range(NoGrab):
                    Sampled_Grab =df[df[Test_Unit] == i].sample(1, replace= True)
                    Index = Sampled_Grab.index
                    CFU = Sampled_Grab["CFU"]
                    CFU_grab = CFU*(Grab_Weight/(Partition_Weight*454))
                    P_Detection=1-math.exp(-CFU_grab)
                    RandomUnif = random.uniform(0,1)
                    if RandomUnif <P_Detection:
                        df.at[Index,"Accept"] = False
        return (df)
    elif Limit > 0:
        Unique_TestUnit = list(df[Test_Unit].unique())
        Grab_Weight = Samp_Size/NoGrab
        PositiveSamples = []
        for i in (Unique_TestUnit):
            for l in range (NSamp_Unit):
                PositiveGrabs  = []
                for j in range(NoGrab):
                    Sampled_Grab =df[df[Test_Unit] == i].sample(1, replace= True)
                    Index = Sampled_Grab.index
                    CFU = Sampled_Grab["CFU"]
                    CFU_grab = CFU*(Grab_Weight/(Partition_Weight*454))
                    P_Detection=1-math.exp(-CFU_grab)
                    RandomUnif = random.uniform(0,1)
                    if RandomUnif <P_Detection:
                        Grab  = 1
                        df.at[Index,"Accept"] = False
                    elif RandomUnif >P_Detection:
                        Grab =0
                    PositiveGrabs.append(Grab)
                SumGrabs = sum(PositiveGrabs)
                PositiveSamples.append(SumGrabs)
                print(PositiveSamples)
        return (df)