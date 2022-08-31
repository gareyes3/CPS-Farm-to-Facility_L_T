# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 08:27:07 2022

@author: gareyes3
"""

#Dictionary for the tomato model

import math
import pandas as pd
import numpy as np


#%% Function for creating output dataframes.

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


def Output_Collection_Processing(df, outputDF, Step_Column,i):
    #df= main model df
    #outputDF = contprogdataframe
    #Step_column = column for the step we are at
    
    Total_CFU = sum(df.CFU)
    outputDF.at[i,Step_Column] = Total_CFU
    return outputDF

def Output_Collection_Exp(df, outputDF,i):
    #df= main model df
    #outputDF = contprogdataframe
    #Step_column = column for the step we are at
    
    Total_CFU = sum(df.CFU)
    outputDF.at[i,"Total CFU"] = Total_CFU
    
    df_Acc = df.loc[(df["Rej_Acc"]=="Acc")].copy()
    Total_CFU_Acc = sum(df_Acc.CFU)
    outputDF.at[i,"Total CFU_ACC"] = Total_CFU_Acc
    
    Total_Weight_Acc = sum(df_Acc.Weight)
    outputDF.at[i,"Total_Weight_Harvested"] = Total_Weight_Acc
    
    Fiedl_df_1 = df.loc[df["Pick_ID"] == 1].copy()
    Total_CFU_Acc_Pick1 = sum(Fiedl_df_1.CFU)
    outputDF.at[i,"Total CFU_ACC_Pick1"] = Total_CFU_Acc_Pick1
    
    Fiedl_df_2 = df.loc[df["Pick_ID"] == 2].copy()
    Total_CFU_Acc_Pick2 = sum(Fiedl_df_2.CFU)
    outputDF.at[i,"Total CFU_ACC_Pick2"] = Total_CFU_Acc_Pick2
    Fiedl_df_3 = df.loc[df["Pick_ID"] == 3].copy()
    Total_CFU_Acc_Pick3 = sum(Fiedl_df_3.CFU)
    outputDF.at[i,"Total CFU_ACC_Pick3"] = Total_CFU_Acc_Pick3
    
    
    
    return outputDF

def Output_Collection_Sampling(df, outputDF,i, SampType, PickNo, Bef_Aft):
    Total_CFU = sum(df.CFU)
    
    Fiedl_df_1 = df.loc[df["Pick_ID"] == PickNo].copy()
    CFU_Avail = sum(Fiedl_df_1["CFU"])
    
    if SampType == "PHS":
        if PickNo == 1:
            if Bef_Aft == "Bef":
                outputDF.at[i,"CFU_Bef_Pick1PHS"] = Total_CFU
                outputDF.at[i,"CFU_Avail Pick 1"] = CFU_Avail
            elif Bef_Aft == "Aft":
                outputDF.at[i,"CFU_Aft_Pick1PHS"] = Total_CFU 
            
            
        if PickNo == 2:
            if Bef_Aft == "Bef":
                outputDF.at[i,"CFU_Bef_Pick2PHS"] = Total_CFU
                outputDF.at[i,"CFU_Avail Pick 2"] = CFU_Avail

            elif Bef_Aft == "Aft":
                outputDF.at[i,"CFU_Aft_Pick2PHS"] = Total_CFU 
        
        if PickNo == 3:
            if Bef_Aft == "Bef":
                outputDF.at[i,"CFU_Bef_Pick3PHS"] = Total_CFU
                outputDF.at[i,"CFU_Avail Pick 3"] = CFU_Avail
            elif Bef_Aft == "Aft":
                outputDF.at[i,"CFU_Aft_Pick3PHS"] = Total_CFU 
                       
                
                
    return outputDF

def Output_Collection_Sampling_Weight_R(df, outputDF,i, SampType, PickNo, Bef_Aft):    
    Rejected_df = df[df["Rej_Acc"]=="REJ"].copy()
    Total_Weight = sum(Rejected_df["Weight"])
    if SampType == "PHS":
        if PickNo == 1:
            if Bef_Aft == "Bef":
                outputDF.at[i,"PHS 1 Weight Rejected Bef"] = Total_Weight
            elif Bef_Aft == "Aft":
                outputDF.at[i,"PHS 1 Weight Rejected Aft"] = Total_Weight
            
        if PickNo == 2:
            if Bef_Aft == "Bef":
                outputDF.at[i,"PHS 2 Weight Rejected Bef"] = Total_Weight
            elif Bef_Aft == "Aft":
                outputDF.at[i,"PHS 2 Weight Rejected Aft"] = Total_Weight
        
        if PickNo == 3:
            if Bef_Aft == "Bef":
                outputDF.at[i,"PHS 3 Weight Rejected Bef"] = Total_Weight
            elif Bef_Aft == "Aft":
                outputDF.at[i,"PHS 3 Weight Rejected Aft"] = Total_Weight
    
    
    return outputDF     
    


#df_field_1 =df.loc[df["Location"]==Previous].copy()

def Output_Collection_Prog_Pick(df, outputDF, Step_Column,i, PickNo):
    #df= main model df
    #outputDF = contprogdataframe
    #Step_column = column for the step we are at
    df2 =df.loc[df["Pick_ID"]==PickNo].copy()
    Total_CFU = sum(df2.CFU)
    outputDF.at[i,Step_Column] = Total_CFU
    return outputDF

#%%
#Column Name for Dataframe Creation

Col_Days = list(np.arange(1, (14)+1))

Proc_Steps = ["Harvest_1", "Shipping Center_1", "Packinghouse_1", "Washing_1", "CB1_1", "Drying_1", "Sorting_1", "Packing_1", "PP_1",
"Harvest_2", "Shipping Center_2", "Packinghouse_2", "Washing_2", "CB1_2", "Drying_2", "Sorting_2", "Packing_2", "PP_2",
"Harvest_3", "Shipping Center_3", "Packinghouse_3", "Washing_3", "CB1_3", "Drying_3", "Sorting_3", "Packing_3", "PP_3"]

"Harvest_"+str(1)

Columns_Final_Outs = [
    "Total CFU",
    "Total CFU_ACC",
    "Total CFU_ACC_Pick1",
    "Total CFU_ACC_Pick2",
    "Total CFU_ACC_Pick3",
    "Total_Weight_Harvested",
    "CFU_Bef_Pick1PHS",
    "CFU_Aft_Pick1PHS",
    "PHS 1 Weight Rejected Bef",
    "PHS 1 Weight Rejected Aft",
    "CFU_Avail Pick 1",
    "CFU_Bef_Pick2PHS",
    "CFU_Aft_Pick2PHS",
    "PHS 2 Weight Rejected Bef",
    "PHS 2 Weight Rejected Aft",
    "CFU_Avail Pick 2",
    "CFU_Bef_Pick3PHS",
    "CFU_Aft_Pick3PHS",
    "PHS 3 Weight Rejected Bef",
    "PHS 3 Weight Rejected Aft",
    "CFU_Avail Pick 3",
    ]




