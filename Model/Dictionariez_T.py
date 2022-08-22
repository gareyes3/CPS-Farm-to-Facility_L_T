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

"H1_2 H1_3, H1_4 H1_5 H1_6, H1_7 H1_8, H1_9"

Columns_Final_Outs = [
    "Total CFU",
    "Total CFU_ACC",
    "Total_Weight_Harvested"
    ]




