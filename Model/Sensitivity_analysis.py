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
                            "ClusterSize"
                            "SampleSize",
                            "SamplesPSublot"
                            "NumberGrabs",
                            "WashingYN"
    ]
    

def Func_LoadInputs (OutputDF,i):
    #Setup Factors
    #Initial Contamination Factors
    OutputDF.at[i, "InitialCont"] = SCInputz.PSHazard_lvl #InitialContmination
    OutputDF.at[i, "ClusteringPer"] = SCInputz.PSNo_Cont_Clusters #Cluestering Level
    OutputDF.at[i, "ClusterSize"] =  SCInputz.PSCluster_Size #InitialContmination
    OutputDF.at[i, "InitialCont"] =  SCInputz.PSCluster_Size #InitialContmination
    #Sampling Factors
    OutputDF.at[i, "SampleSize"] = SCInputz.sample_size_PH #Sample Size at Pe-Harvest
    OutputDF.at[i, "SamplesPSublot"] = SCInputz.n_samples_slot_PH #Number of Samples per sublot
    OutputDF.at[i, "NumberGrabs"] =  SCInputz.No_Grabs_PH #Number of Grabs at PreHarvest.
    #Procesing Factord
    OutputDF.at[i, "WashingYN"] =  SCInputz.No_Grabs_PH #Number of Grabs at PreHarvest.


    


    
    

