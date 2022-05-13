# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 11:31:26 2021

@author: gareyes3
"""
import math
import pandas as pd
import numpy as np
import SCInputz
import Inputz
import MainModel3z
import ScenCondz


Column_Names_Outs = ["Step_CFU_Acc",
                     "Step_CFU_Rej",
                     "Step_CFU_PerR",
                     "Step_Wei_Acc",
                     "Step_Wei_Rej",
                     "Step_Wei_PerR",
                    ]


Column_Names_Progression = ["Contam Event Before PHS",
                            "Bef Pre-Harvest Samp",
                            "Aft Pre-Harvest Samp",
                            "Contam Event After PHS",
                            "Bef Harvest Samp",
                            "Aft Harvest Samp",
                            "Bef Receiving Samp",
                            "After Receiving Samp",
                            "Bef SprayWash",
                            "Bef Shredding",
                            "Bef Conveyor Belt",
                            "Bef Washing",
                            "Bef Shaker Table",
                            "Bef Centrifuge",
                            "Aft Value Addition",
                            "Bef Final Prod S",
                            "Final Product Facility",
                            "Bef CS Samp",
                            "After CS Samp"
                            ]

Column_Names_Mass_Prog = ["Contam Event Before PHS",
                            "Bef Pre-Harvest Samp",
                            "Aft Pre-Harvest Samp",
                            "Contam Event After PHS",
                            "Bef Harvest Samp",
                            "Aft Harvest Samp",
                            "Bef Receiving Samp",
                            "After Receiving Samp"
                            "Bef Shredding",
                            "Bef Conveyor Belt",
                            "Bef Washing",
                            "Bef Shaker Table",
                            "Bef Centrifuge",
                            "Aft Value Addition",
                            "Bef Final Prod S",
                            "Final Product Facility",
                            "Bef CS Samp",
                            "After CS Samp"
                            ]


Column_Per_Contaminated = ["PropCont_CE_B_PHS",
                            "PropCont_B_PHS",
                            "PropCont_A_PHS",
                            "PropCont_CE_A_PHS",
                            "PropCont_B_HS",
                            "PropCont_A_PHS",
                            "PropCont_B_RS",
                            "PropCont_A_RS",
                            "PropCont_B_SprayWash",
                            "PropCont_B_Shredding",
                            "PropCont_B_CBelt",
                            "PropCont_B_Washing",
                            "PropCont_B_ST",
                            "PropCont_B_Cent",
                            "PropCont_A_VA",
                            "PropCont_B_FPS",
                            "PropCont_A_FP",
                            "PropCont_B_CS",
                            "PropCont_A_CS",
                            "PropCont_A_FP_Whole",
                            "PropCont_A_CS_Whole"
                            "TotalCont_A_FP",
                            "TotalCont_A_CS"
    ]

Columns_Final_Outs = [
    "I_Per_Cont_Packages",
    "I_Total_CFU",
    "I_Total_CFU_g"
    "F_Per_Cont_Packages",
    "TotalCF",
    "I_Total_CFU",
    "F_Total_CFU_g"
    ]



#Rejected Contaminated
#Rejected Not Contaminated

#Accepted Contaminated
#Accepted Not Contaminated
    


def Output_DF_Creation(Column_Names, Niterations):
    Outputs_Df =pd.DataFrame(np.NaN, index= range(Niterations), columns =Column_Names)
    return Outputs_Df



def Output_Collection_Prog(df, outputDF, Step_Column,i):
    #df= main model df
    #outputDF = contprogdataframe
    #Step_column = column for the step we are at
    Total_CFU = sum(df.CFU)
    outputDF.at[i,Step_Column] = Total_CFU
    return outputDF

def Pop_Output_Colection(df, outputDF, Step_Column, i):
    Pop  = df[df.CFU>0]
    TotalPop = len(Pop)
    Total_whole = len(df.CFU)
    Pop_Final = TotalPop /Total_whole
    outputDF.at[i,Step_Column] =  Pop_Final
    return outputDF

def Prop_Collection_WholeField (df, outputDF, Step_Column, i):
    Pop  = df[df.CFU>0]
    TotalPop = len(Pop)
    Total_whole = (SCInputz.Field_Weight/ Inputz.Pack_Weight_FP)
    Pop_Final = TotalPop /Total_whole
    outputDF.at[i,Step_Column] =  Pop_Final
    return outputDF

def Prop_Sensitivity(df):
    Pop  = df[df.CFU>0]
    TotalPop = len(Pop)
    Total_whole = (SCInputz.Field_Weight/ Inputz.Pack_Weight_FP)
    Pop_Final = TotalPop /Total_whole
    return Pop_Final
    
    


#df.CFU=np.random.uniform(0,1,2000)
#df.CFU[1] = 0

def Output_Collection_Final(df, outputDF, Step, Cont_Before, Weight_Before, i, Niterations):
    #Contaminations
    Cont_Acc = sum(df.CFU)
    Cont_Rej = Cont_Before-Cont_Acc
    if Cont_Acc == 0:
        Cont_PerR = None
    else:
        Cont_PerR = Cont_Rej/(Cont_Acc+Cont_Rej) #Percentage Rejected by Finished product sampling
    #Weight
    Wei_Acc = sum(df.Weight)
    Wei_Rej = Weight_Before-Wei_Acc
    Wei_PerR =  Wei_Rej/(Wei_Rej+Wei_Acc)
    
    outputDF.at[i,"Step_CFU_Acc"] = Cont_Acc
    outputDF.at[i,"Step_CFU_Rej"] = Cont_Rej
    outputDF.at[i,"Step_CFU_PerR"] = Cont_PerR
    outputDF.at[i,"Step_Wei_Acc"] = Wei_Acc
    outputDF.at[i,"Step_Wei_Rej"] = Wei_Rej
    outputDF.at[i,"Step_Wei_PerR"] = Wei_PerR
    if i == Niterations -1:
        outputDF.columns = outputDF.columns.str.replace("Step", Step) #Updating Head of Columns Change column end iteration.
    
    return outputDF

#%%
#Sens Analysis

'''
##Creation of Random Variables. 

#Contamination Determination Inputs
Total_grams= SCInputz.Field_Weight*454


CFU_10000g = Total_grams/10000 #-4 log
CFU_1000g = Total_grams/1000  #-3 log
CFU_100g = Total_grams/100 #-2 log
CFU_10g = Total_grams/10  #-1 log
CFU_g =  Total_grams #0 log
CFU_0_1g = Total_grams*10 #1 log


CFU_0_01g = Total_grams*100 #2log

#Contamination List
Contamination_List = [CFU_10000g,CFU_1000g,CFU_100g,CFU_10g,CFU_g,CFU_0_1g]
#Clustering List
Clustering_List =[100,1000,10000,100000]
NoClusters_List = [1,2,3,4]
SampleSize_List = [60,120,240,600,1200]
NoSamples_List = [1,2,3,4,5,6,7,8,9,10]
NoGrabs_List = [1,60,120,240,300,600,1200]
'''


Sensitivity_Analysis_Dic = [
                            #Field Setup Factors
                            #"InitialCont" ,
                            "ClusterSize",
                            "Time_CE_H",
                            #"Total_CE_H_Dieoff",
                            
                            #Pre-cooling
                            "Time_H_PC",
                            "Temp_H_PC",
                            "Time_Precooling",
                            "Temp_Precooling",
                            #"Pre_cooling",
                            #Receiving
                            "Time_Storage_R",
                            "Temp_Storage_R",
                            #Processing Factor
                            #"PreWashRed",
                            #"PreWashYN",
                            #"WashingYN",
                            #"OptimizeWashingYN",
                            #"SanitationYN", #New Added saniation after optimied wash
                            "ChSpray_eff", #new
                            "TotalRedPre_wash",
                            "TotalRed_wash",
                            "Tr_Sh_P",
                            "Tr_P_Sh",
                            "Sh_Compliance",
                            "Sh_San_freq",
                            "Sh_San_Eff",
                            "Tr_Cv_P",
                            "Tr_P_Cv",
                            "Cv_Compliance",
                            "Cv_San_freq",
                            "Cv_San_Eff",
                            "Tr_St_P",
                            "Tr_P_St",
                            "St_Compliance",
                            "St_San_freq",
                            "St_San_Eff",
                            "Tr_C_P",
                            "Tr_P_C",
                            "C_Compliance",
                            "C_San_freq",
                            "C_San_Eff",
                            #After finished product
                            "Time_PostPStorage",
                            "Temperature_ColdStoragePostFP",
                            "Trasnportation_TimeFP_C",
                            "Transportation_TempFP_C",
                            "Time_Cust_Sto",
                            "Temp_Cust_Sto",
                            
                            #Sampling
                            #"PHS4d",
                            #"PHS4h",
                            #"PHSInt",
                            #"HS",
                            #"RS",
                            #"FPS",
                            #"CS",
                            
                            
                            "TotalCFUFP",
                            "PropCont"
                        
                            
    ]
    

def Func_LoadInputs (OutputDF,i,df, TotalDieoff,TotalRed_PreWash,TotalRed_Wash ):
    #Setup Factors
    #Initial Contamination Factors
    #OutputDF.at[i, "InitialCont"] =  Inputz.Hazard_Lvl #InitialContmination
    OutputDF.at[i, "ClusterSize"] =   Inputz.Cluster_Size #InitialContmination
    OutputDF.at[i, "Time_CE_H"] =  Inputz.Time_CE_H #Time between contamination event and harvest
    #OutputDF.at[i, "Total_CE_H_Dieoff"] = TotalDieoff  #TotalDieoff between contamination event and harvest. 
    
    '''
    #Sampling Selection
    OutputDF.loc[i, "PH4d"] = ScenCondz.PHS_4d #InitialContmination
    OutputDF.loc[i, "PH4h"] = ScenCondz.PHS_4h #Cluestering Level
    OutputDF.loc[i, "PHInt"] =  ScenCondz.PHS_Int #InitialContmination
    OutputDF.loc[i, "HTrad"] =  ScenCondz.H_Sampling #Time between contamination event and harvest
    OutputDF.loc[i, "RTrad"] =  ScenCondz.R_Sampling #Time between contamination event and harvest
    OutputDF.loc[i, "FPTrad"] =  ScenCondz.FP_Sampling #Time between contamination event and harvest
    '''
    #Harvests
    #Pre-cooling
    OutputDF.at[i, "Time_H_PC"] =  Inputz.Time_H_PreCooling #Time beetween harvest and pre-cooling
    OutputDF.at[i, "Temp_H_PC"] =  Inputz.Temperature_H_PreCooling #Time beetween harvest and pre-cooling
    OutputDF.at[i, "Time_Precooling"] =  Inputz.Time_PreCooling #Pre-cooling process length time
    OutputDF.at[i, "Temp_Precooling"] =  Inputz.Temperature_PreCooling #Pre-cooling process temperature
    #OutputDF.loc[i, "Pre_cooling"] =  SCInputz.Pre_CoolingYN #Number of Grabs at PreHarvest.
    #Receiving
    OutputDF.at[i, "Time_Storage_R"] =  Inputz.Time_Storage_R #Time storage at receiving
    OutputDF.at[i, "Temp_Storage_R"] =  Inputz.Temperature_Storage_R #temperature of receiving storage.
    #Procesing Factord
    #OutputDF.at[i, "PreWashRed"] =  Inputz.Harvest_Cspray_red #Reduction pre-wash
    #OutputDF.loc[i, "WashingYN"] =  SCInputz.Washing_YN #Washing Yes or NotSCInputz.Spray_WashYN
    #OutputDF.loc[i, "PreWashYN"] =  SCInputz.Spray_WashYN #Washing Yes or Not
    #OutputDF.loc[i, "OptimizeWashingYN"] =  SCInputz.Washing_Optimized #Washing Yes or Not
    #OutputDF.loc[i, "SanitationYN"] =  SCInputz.Sanitation_YN #Washing Yes or Not
    
    
    OutputDF.loc[i, "ChSpray_eff"] =  Inputz.Harvest_Cspray_red #Washing Yes or Not
    OutputDF.loc[i, "TotalRedPre_wash"] =  TotalRed_PreWash #Washing Yes or Not
    OutputDF.loc[i, "TotalRed_wash"] =  TotalRed_Wash #Washing Yes or Not
    
    
    OutputDF.at[i, "Tr_Sh_P"] =  Inputz.Tr_Sh_P
    OutputDF.at[i, "Tr_P_Sh"] =  Inputz.Tr_P_Sh
    OutputDF.at[i, "Sh_Compliance"] =  Inputz.Sh_Compliance
    OutputDF.at[i, "Sh_San_freq"] =  Inputz.Sh_San_freq
    OutputDF.at[i, "Sh_San_Eff"] =  Inputz.Sh_San_Eff
    
    OutputDF.at[i, "Tr_Cv_P"] =  Inputz.Tr_Cv_P
    OutputDF.at[i, "Tr_P_Cv"] =  Inputz.Tr_P_Cv
    OutputDF.at[i, "Cv_Compliance"] =  Inputz.Cv_Compliance
    OutputDF.at[i, "Cv_San_freq"] =  Inputz.Cv_San_freq
    OutputDF.at[i, "Cv_San_Eff"] =  Inputz.Cv_San_Eff
    
    OutputDF.at[i, "Tr_St_P"] =  Inputz.Tr_St_P
    OutputDF.at[i, "Tr_P_St"] =  Inputz.Tr_P_St
    OutputDF.at[i, "St_Compliance"] =  Inputz.St_Compliance
    OutputDF.at[i, "St_San_freq"] =  Inputz.St_San_freq
    OutputDF.at[i, "St_San_Eff"] =  Inputz.St_San_Eff
    
    OutputDF.at[i, "Tr_C_P"] =  Inputz.Tr_C_P
    OutputDF.at[i, "Tr_P_C"] =  Inputz.Tr_P_C
    OutputDF.at[i, "C_Compliance"] =  Inputz.C_Compliance
    OutputDF.at[i, "C_San_freq"] =  Inputz.C_San_freq
    OutputDF.at[i, "C_San_Eff"] =  Inputz.C_San_Eff

    #Finsihed product and beyond
    OutputDF.at[i, "Time_PostPStorage"] =  Inputz.Time_PostPStorage
    OutputDF.at[i, "Temperature_ColdStoragePostFP"] =  Inputz.Temperature_ColdStorage
    OutputDF.at[i,  "Trasnportation_TimeFP_C"] =  Inputz.Trasnportation_Time
    OutputDF.at[i, "Transportation_TempFP_C"] =  Inputz.Transportation_Temp
    OutputDF.at[i, "Time_Cust_Sto"] =  Inputz.Time_PostPCS
    OutputDF.at[i, "Temp_Cust_Sto"] =  Inputz.Temperature_PostPCS
    
    #sampling
    #OutputDF.loc[i, "PHS4d"] =  ScenCondz.PHS_4d,
    #OutputDF.loc[i, "PHS4h"] =  ScenCondz.PHS_4h,
    #OutputDF.loc[i, "PHSInt"] =  ScenCondz.PHS_Int,
    #OutputDF.loc[i, "HS"] =  ScenCondz.HS_Trad,
    #OutputDF.loc[i, "RS"] =  ScenCondz.R_Sampling,
    #OutputDF.loc[i, "FPS"] =  ScenCondz.FPS_Trad,
    #OutputDF.loc[i, "CS"] =   ScenCondz.C_Sampling,
    
    #Output
    OutputDF.loc[i, "TotalCFUFP"] =  df["CFU"].sum()
    OutputDF.loc[i, "PropCont"] = Prop_Sensitivity(df)
    
    
    return   OutputDF

    








































'''
df_prog = Output_DF_Creation(Column_Names =Column_Names_Progression, Niterations =20)
df_outs = Output_DF_Creation(Column_Names =Column_Names_Outs, Niterations =20)


df_prog = Output_Collection_Prog(df = df,
                                outputDF = df_prog,
                                Step_Column = "Bef Pre-Harvest Samp", 
                                i =11 )


ContBEf = 10000
weightBEf = 100000
df_outs = Output_Collection_Final(df = df, 
                                outputDF = df_outs, 
                                Step = "PH", 
                                Cont_Before = 10000, 
                                Weight_Before =1000000, 
                                i = 10, 
                                Niterations = 20)

'''