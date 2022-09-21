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
    outputDF.at[i,Step_Column] =np.array(df["CFU"]).sum()
    return outputDF

def Output_Collection_Prog_Prev(df, outputDF, Step_Column,i):
    #df= main model df
    #outputDF = contprogdataframe
    #Step_column = column for the step we are at
    outputDF.at[i,Step_Column] =sum(df["CFU"]>0)/len(df)
    return outputDF


def Output_Collection_Processing(df, outputDF, Step_Column,i):
    #df= main model df
    #outputDF = contprogdataframe
    #Step_column = column for the step we are at
    outputDF.at[i,Step_Column] =np.array(df["CFU"]).sum()
    return outputDF

def Output_Collection_Exp(df, outputDF,i):
    #df= main model df
    #outputDF = contprogdataframe
    #Step_column = column for the step we are at
    
    outputDF.at[i,"Total CFU"] = np.array(df["CFU"]).sum()
    
    df_Acc = df.loc[(df["Rej_Acc"]=="Acc")].copy()
  
    outputDF.at[i,"Total CFU_ACC"] =np.array(df_Acc["CFU"]).sum()
    
    outputDF.at[i,"Total_Weight_Harvested"] = np.array(df_Acc["Weight"]).sum()
    
    Fiedl_df_1= df.loc[df["Pick_ID"] == 1].copy()
    outputDF.at[i,"Total CFU_ACC_Pick1"] = np.array(Fiedl_df_1 ["CFU"]).sum()
    
    Fiedl_df_2 = df.loc[df["Pick_ID"] == 2].copy()    
    outputDF.at[i,"Total CFU_ACC_Pick2"] = np.array(Fiedl_df_2["CFU"]).sum()
    
    Fiedl_df_3 = df.loc[df["Pick_ID"] == 3].copy()

    outputDF.at[i,"Total CFU_ACC_Pick3"] = np.array(Fiedl_df_3["CFU"]).sum()
    
    
    
    return outputDF

def Output_Collection_Sampling(df, outputDF,i, SampType, PickNo, Bef_Aft):
    Total_CFU = np.array(df["CFU"]).sum()
    
    
    Fiedl_df_1 = df.loc[df["Pick_ID"] == PickNo].copy()
    CFU_Avail = np.array(Fiedl_df_1["CFU"]).sum()
    Total_Prev = sum(Fiedl_df_1["CFU"]>0)/len(Fiedl_df_1)
    
    if SampType == "PHS":
        if PickNo == 1:
            if Bef_Aft == "Bef":
                outputDF.at[i,"CFU_Bef_Pick1PHS"] = Total_CFU
                outputDF.at[i,"CFU_Avail Pick 1"] = CFU_Avail
                outputDF.at[i,"Prev_Avail Pick 1"] = Total_Prev
            elif Bef_Aft == "Aft":
                outputDF.at[i,"CFU_Aft_Pick1PHS"] = Total_CFU 
            
            
        if PickNo == 2:
            if Bef_Aft == "Bef":
                outputDF.at[i,"CFU_Bef_Pick2PHS"] = Total_CFU
                outputDF.at[i,"CFU_Avail Pick 2"] = CFU_Avail
                outputDF.at[i,"Prev_Avail Pick 2"] = Total_Prev

            elif Bef_Aft == "Aft":
                outputDF.at[i,"CFU_Aft_Pick2PHS"] = Total_CFU 
        
        if PickNo == 3:
            if Bef_Aft == "Bef":
                outputDF.at[i,"CFU_Bef_Pick3PHS"] = Total_CFU
                outputDF.at[i,"CFU_Avail Pick 3"] = CFU_Avail
                outputDF.at[i,"Prev_Avail Pick 3"] = Total_Prev
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
    outputDF.at[i,Step_Column] = np.array(df2["CFU"]).sum()
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
    "Prev_Avail Pick 1",
    "CFU_Bef_Pick2PHS",
    "CFU_Aft_Pick2PHS",
    "PHS 2 Weight Rejected Bef",
    "PHS 2 Weight Rejected Aft",
    "CFU_Avail Pick 2",
    "Prev_Avail Pick 2",
    "CFU_Bef_Pick3PHS",
    "CFU_Aft_Pick3PHS",
    "PHS 3 Weight Rejected Bef",
    "PHS 3 Weight Rejected Aft",
    "CFU_Avail Pick 3",
    "Prev_Avail Pick 3"
    ]




