# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 13:08:43 2022

@author: gareyes3
"""

#Scen_T
Cont_Scenario = 1
#1  =10, #2 = 10% ,#3 = 1% #4 = 0.1#

#5 Harvester, #6 Bin Contamination

#Sampling Plan
Samp_Plan = 1
    #PHS
    #HS
    #RS
    #PPS
    
Tomatoes_per_sample = 2

Samp_Method = 1
#1 = whole tomato
#2 = tomato mash method

N_Replicates = 25
#Number of replicates taken from the mash


#if 1 we choose the contmaination day, if 0 contamination day is random
Chosen_cont_day = 0
#Day when contamination will happen
Contamination_Day = 0


#Total Iterations. iterations for the loop
Iteration_Number = 50

#Contamination Scenario, initial CFUs that will contaminate field
#if scenario 5 or 6 this contamination will split into three picks. 
Total_Hazard = 132_000

