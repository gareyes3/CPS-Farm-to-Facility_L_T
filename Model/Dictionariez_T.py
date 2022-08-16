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

#%%
#Column Name for Dataframe Creation

Col_Days = list(np.arange(1, (41)+1))



