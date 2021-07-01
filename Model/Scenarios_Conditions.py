# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:12:47 2021

@author: Gustavo Reyes
"""

#Sampling Conditions, Baseline all conditions are off
Baseline_Sampling= 0 #all others must be 0if this one is 1
PH_Sampling = 0
H_Sampling = 0
R_Sampling = 0
FP_Sampling =1

#Additional Sampling Conditions. Env and 
Water_SamplingProc = 0
Env_SamplingProc =0
Env_SamplingCust = 0
Water_SamplingCust = 0

#Contamination Challenges
#In Field
Background_C=0
Point_Source_C=0
Systematic_C=0

#Harvester Contamination
Crew_C = 0
Harvester_C = 0

#Processing equipment
PE_C = 0



#Sampling Options

#Pre-Harvest
    #Pre-Harvest sampling must be on
PHS_4d= 0 #Scenario 1
PHS_4h = 0#Scenario 2
PHS_Int = 0 #Scenario 3

#Harvest: 
    #HArvest Sampling must be one
HS_Trad = 0
HS_Agg = 0

#Final Product Sampling
    #Final Product sampling must be on.
FPS_Trad =0
FPS_Agg = 1 