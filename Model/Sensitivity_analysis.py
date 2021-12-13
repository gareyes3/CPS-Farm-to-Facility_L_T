# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 16:00:57 2021

@author: Gustavo Reyes
"""
import SCInputz
import Inputz
import ScenCondz

#Sensityvity Analysis

#Inputs to Analyze: 
    #1: Initial Contamination
    #2: Contamination Clustering Level
    #3: Sample Size
    #4: Nuber of Grabs
    
    #5: Washing Step 1 or 0
    #6: 
        
#%% Collection Dataframe

Sensitivity_Analysis_Dic = ["InitialCont" ,
                            "ClusteringPer",
                            "SampleSize",
                            "NumberGrabs",
                            "WashingYN"
    ]

Sensitivity_Analysis_Dic_var = [
    #Initial Contamination Inputs
    SCInputz.PSHazard_lvl, #Hazard Level
    SCInputz.PSNo_Cont_Clusters, #Number of Clusters
    SCInputz.PSCluster_Size, #Cluster Size
    # Sampling PH 4D. 
    SCInputz.sample_size_PH, #Sample Size Pre-Harvest
    SCInputz.n_samples_slot_PH, #Number of samples per Sublot
    SCInputz.No_Grabs_PH,
    #Rejection Rule
    SCInputz.RR_PH_Trad,
    #Pre_HArvest
    Inputz.Time_CE_PHS, #Time between CE and PHS
    LV_Die_Off_CE_PHS,#Die-off From CE-PHS
    LV_Die_off_B, #Dieoff from CE
    
    
    
    
    
    
    
    
    
    
    ]


    

def Func_LoadInputs (OutputDF,i,Input_ListString, InputListVar):
    for j in Input_List:
        OutputDF.at[j,]
    
    

