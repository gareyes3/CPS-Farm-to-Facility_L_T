# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 12:40:30 2022

@author: gareyes3
"""
import numpy as np
import pandas as pd
import random 
import math
from numpy.random import Generator, PCG64
rng = Generator(PCG64())
import matplotlib.pyplot as plt
import seaborn as sns

import time

#Inputz_T
#%%
def get_trasn_rate(mean,sd):
    Signal = 0
    A = np.random.normal(mean,sd)
    if A<0:
        while  A<0:
             A = np.random.normal(mean,sd) 
        print(A)
    return A
            

#%%%

#Basic Information
Tomato_weight = 260/454 #for medium tomato #260g tomato
Tomato_Sequence = int(132_000/Tomato_weight)
Individual_Tomatoes = np.arange(1,Tomato_Sequence)
Tomatoes_Per_Plant = 120
Tomatoes_Per_Bucket = int(32/Tomato_weight)
Bin_Weight = 1000
Tomatoes_per_Bin = math.ceil(Bin_Weight/Tomato_weight)

#total pick information
N_Pick = 3
Days_Between_Picks = 14
Days = range(1, (N_Pick*Days_Between_Picks)+1)
Harvest_Days = [14,28,42] #This final Harvest Day has to be the final day as well. 
PHS_Days = [11,25,39]

#individual sequences for functions
Individual_Plants = np.repeat(np.arange(1,int(np.ceil(Tomato_Sequence/Tomatoes_Per_Plant))),Tomatoes_Per_Plant+1)
Pick_Sequence = list(range(1,N_Pick+1))*(int(np.ceil(Tomato_Sequence/3)))
Pick_Random = random.sample(Pick_Sequence, len(Pick_Sequence))


#Harvest information
Total_Harvesters = 55
Total_Bins = 44


#Trasnfer Rates Conveyor Belt: 
Tr_CB_P = get_trasn_rate(mean = 0.01,sd = 0.0045)
Tr_P_CB = get_trasn_rate(mean = 0.02,sd = 0.0085)

#Trasnfer Rates: 
Tr_Dr_P = get_trasn_rate(mean = 0.01,sd = 0.0045)
Tr_P_Dr = get_trasn_rate(mean = 0.02,sd = 0.0085)

#Trasnfer Rates: 
Tr_SRT_P = get_trasn_rate(mean = 0.01,sd = 0.0045)
Tr_P_SRT = get_trasn_rate(mean = 0.02,sd = 0.0085)


#Contamination Scenario



#Processing Factors
RH_Florida= 74.5
RH_Ripening = 90
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

#Pot Packer Storage Ripening Room
Temp_Post_Pack = 20
Time_Post_Pack = random.uniform(24,48) #hr 

#In Field 
Temp_In_Field = 25

#Washing FC_Level

FC_lvl = np.random.triangular(25,100,200)




