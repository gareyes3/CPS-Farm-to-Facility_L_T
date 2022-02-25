# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 09:54:26 2022

@author: gareyes3
"""
# Libraries
import numpy as np
import SCInputz
import random
import Funz
from scipy.stats import beta
import InFunz
import ContScen
import Inputz
import math


#Assisting Functions
def pert(a, b, c, *, size=1, lamb=4):
    r = c - a
    alpha = 1 + lamb * (b - a) / r
    beta = 1 + lamb * (c - b) / r
    return float(a + np.random.beta(alpha, beta, size=size) * r)

def betagen(a,b,mini,maxi):    
    return float(beta.rvs(a , b)* (maxi - mini) + mini)


#Contamination from irrigation water pang et al
def F_InitialCont():
    #Using base pert distribution
    #Calculation of total CFUs
    Cont_CFU_g = float(pert(0,0,634))
    g_field = SCInputz.Field_Weight*454 #454 g in 1 lb. 
    Final_Cont = int(Cont_CFU_g*g_field)
    return Final_Cont
#%% Contamination Functions:
def Irrigation_Water_Cont():
    #Ecoli_soil = np.random.normal(0.549,0.816) #log10 CFU/g
    #P_Ecoli_Water = 0.35
    #PosYN_Ecoli_Water = np.random.binomial(1,P_Ecoli_Water)
    C_Ecoli_Water = (10**np.random.normal(0.604,0.357))/10 #CFU/ml water
    
    Tr_Irr_Water = np.random.uniform(1.8,21.6) #ml/g produce
    #Pr_Irr_Splashing = pert(0.02,0.04,0.05)
    #Pr_Rain_Splashing = 1
    #Soil_Transfer = betagen(0.4,0.8,0.05,16.4)
    #P_Soil_Plant = np.random.uniform(0.35,0.9)
    
    Increase_Irrigation =C_Ecoli_Water*Tr_Irr_Water #CFU/g
    Increase_IrrigationCFU = Increase_Irrigation*(454*100_000)
    return Increase_IrrigationCFU

#%%
#Inputs.
#Time Inputs 

df= InFunz.F_InDF(Partition_Units = SCInputz.Partition_Units,
                  Field_Weight = SCInputz.Field_Weight, 
                  slot_number = SCInputz.slot_number)

#Pre-Contamination Information
Scenario_no = 1 # np.random.choice([1,2,3,4,5])
Total_Days = 14
PHS_Time = 0.1666
PHS_Day = math.ceil(PHS_Time)

#Times from Initial to PHS:
Time_I_PHS = Total_Days-PHS_Time
Time_I_PHS_FullD=int(math.modf(Time_I_PHS)[1])
Time_I_PHS_PartD=math.modf(Time_I_PHS)[0]

#Times from PHS to H
Time_PHS_H =Total_Days-Time_I_PHS
Time_PHS_H_FullD =int(math.modf(Time_PHS_H)[1])
Time_PHS_H_PartD =math.modf(Time_PHS_H)[0]

#Holding Time Days:
Holding_Time = int(pert(2,4,8)) #Irrigation

#Irrigation:
Time_Cutoff_Irrigation = Total_Days-Holding_Time

#Irrigation information
probability_irrigation_day = (1/7)
irrigation_days=list(range(1,(14-Holding_Time+1))) #1 is 1st day, 14 is harvest.
Normalized_Irrigation=len(irrigation_days)/7
Final_Irrigation_Days = [i for i in irrigation_days if (probability_irrigation_day*Normalized_Irrigation)>np.random.uniform(0,1)]
#Removing irrigtion day if 
#if PHS_Day in Final_Irrigation_Days:
#   Final_Irrigation_Days.remove(PHS_Day)


#Contamintion Function Irrigation Based: 
TotalTime = 0 #Time Tracker
#Contamination part 1: From Beginning-to-PHS
for i in range(Time_I_PHS_FullD): #Loop to repeat over the full days before PHS
    #Determining Contamination Scenario
    if Scenario_no == 1: #scenario 1: Irrigation water contamination
        #Calculating total CFU in Field for irrigation fields
        if TotalTime in Final_Irrigation_Days:
            Cont = Irrigation_Water_Cont()
            print(Cont)
            #Adding Uniform Contmaination to the field
            df = ContScen.F_systematic_C(df =df, 
                          Hazard_lvl = Cont,
                          No_Cont_Clusters=1,
                          Cluster_Size=100_000, 
                          Partition_Weight= 50)
            
        df = Funz.Applying_dieoff(df=df, Dieoff=Funz.F_Simple_DieOff(1))
    TotalTime = TotalTime+1
    
    
if Time_I_PHS_PartD >0: #Only if the partial day is greater than o
    #Part 2: Partial Day, deciding if contamination occurs in the first or second part of the day
    if np.random.uniform(0,1)<Time_I_PHS_PartD: 
        Happens_YN_1part=1 
    else: 
        Happens_YN_1part=0
    
    if Happens_YN_1part==1:
            if TotalTime in Final_Irrigation_Days:
                Cont = Irrigation_Water_Cont()  
                print(Cont)
                #Adding Uniform Contmaination to the field
                df = ContScen.F_systematic_C(df =df, 
                              Hazard_lvl = Cont,
                              No_Cont_Clusters=1,
                              Cluster_Size=100_000, 
                              Partition_Weight= 50)      
    #Dieoff for first part of the day:
    df = Funz.Applying_dieoff(df=df, Dieoff=Funz.F_Simple_DieOff(Time_I_PHS_PartD))
    TotalTime = TotalTime+Time_I_PHS_PartD
    

#Part 2 After Sampling
if Time_PHS_H_PartD > 0: #If Time between PHS-H is less than 1
    if Happens_YN_1part==0:
        if TotalTime in Final_Irrigation_Days:
            Cont = Irrigation_Water_Cont()
            print(Cont)   
            #Adding Uniform Contmaination to the field
            df = ContScen.F_systematic_C(df =df, 
                          Hazard_lvl = Cont,
                          No_Cont_Clusters=1,
                          Cluster_Size=100_000, 
                          Partition_Weight= 50) 
        
        df = Funz.Applying_dieoff(df=df, Dieoff=Funz.F_Simple_DieOff(Time_PHS_H_PartD))
    TotalTime = TotalTime+Time_PHS_H_PartD


for i in range(Time_PHS_H_FullD):
    if Scenario_no ==1:
        if TotalTime in Final_Irrigation_Days:
            #Calculating total CFU in Field
            Cont = Irrigation_Water_Cont() 
            print(Cont)
            #Adding Uniform Contmaination to the field
            df = ContScen.F_systematic_C(df =df, 
                          Hazard_lvl = Cont,
                          No_Cont_Clusters=1,
                          Cluster_Size=100_000, 
                          Partition_Weight= 50) 
        
    df = Funz.Applying_dieoff(df=df, Dieoff=Funz.F_Simple_DieOff(1))
    TotalTime = TotalTime+1


df["CFU"].sum()
