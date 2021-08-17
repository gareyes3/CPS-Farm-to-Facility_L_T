# -*- coding: utf-8 -*-

#Scenario and Conditions
                                                                #Scenarios and Conditions
#Sampling Conditions, Baseline all conditions are off
Baseline_Sampling= 0 #all others must be 0if this one is 1
PH_Sampling = 1
H_Sampling = 0
R_Sampling = 0
FP_Sampling = 0

#Additional Sampling Conditions. Env and 
Water_SamplingProc = 0
Env_SamplingProc =0
Env_SamplingCust = 0
Water_SamplingCust = 0


#Contamination Challenges
#In Field
Background_C=1
Point_Source_C=0
Systematic_C=0

#Harvester Contamination
Crew_C = 0
Harvester_C = 0

#Processing equipment
PE_C = 0
PE_Cont_Loc = 0,#2,3,4,5
#1 = Shredder, #2 = Belt, #3 = Washing, #4 Shaker, #5Centrifuge
Pack_C= 0

#Customer
Customer_Added_Steps = 0 



#Sampling Options

#Pre-Harvest
    #Pre-Harvest sampling must be on
PHS_4d= 1#Scenario 1
PHS_4h = 0#Scenario 2
PHS_Int = 0 #Scenario 3

#Harvest: 
    #HArvest Sampling must be one
HS_Trad = 1 #Scenario 5
HS_Agg = 0#Scenario 6

#Final Product Sampling
    #Final Product sampling must be on.
FPS_Trad =1 #Scenario 7
FPS_Agg = 0  #Scenario 8

