# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 11:31:26 2021

@author: gareyes3
"""
import math
import pandas as pd

Niteration = 20
i = 3

data_contprog = {"Initial":[""]*Niteration,
             "Bef Pre-Harvest Samp": [""]*Niteration,
             "Aft Pre-Harvest Samp": [""]*Niteration,
             "Bef Harvest Samp":[""]*Niteration,
             }

df_contprog = pd.DataFrame(data_contprog)

df_contprog.at[i,"Initial"]  =3

[""]*Niteration


def Output_Collection_Prog(df, outputDF, Step_column):
    #df= main model df
    #outputDF = contprogdataframe
    #Step_column = column for the step we are at
    Total_CFU = sum(df.CFU)
    outputDF.at[i,Step_column] = Total_CFU
    return outputDF


def Output_Collection_Final(df, outputDF, Step):
    if Step == "PH":
        



        
