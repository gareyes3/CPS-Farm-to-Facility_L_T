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
Days = np.arange(1, (N_Pick*Days_Between_Picks)+1)
Harvest_Days = [14,28,42] #This final Harvest Day has to be the final day as well. 
PHS_Days = [11,25,39]

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
Total_Hazard = 42_000


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

#Pot Packer Storage 
Temp_Post_Pack = 25
Time_Post_Pack = 6

#In Field 
Temp_In_Field = 25


#Total Iterations
Iteration_Number = 1
