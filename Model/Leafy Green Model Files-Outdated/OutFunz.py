# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 09:46:17 2021

@author: Gustavo Reyes
"""

import pandas as pd

def F_Melting(df, Scenario):
    X_df_contprog2= pd.melt(df)
    X_df_contprog2["Scenario"] = Scenario
    return X_df_contprog2



def F_Output_get(Outdf,step, OutType):
    #Type defines "Cont" or "Weight"
    Stepdf = Outdf.filter(like = step, axis =1)#Filter outputs dataframe based on step where sampling occured.
    if OutType == "PerContR":
        Rest_ofString = "CFU_PerR"
        List_String = [step,Rest_ofString]
        Joinedst = "_".join( List_String)
        out = list(Stepdf[Joinedst])
    elif OutType =="PerWeightR":
        Rest_ofString = "Wei_PerR"
        List_String = [step,Rest_ofString]
        Joinedst = "_".join( List_String)
        out = list(Stepdf[Joinedst])
    elif OutType =="WeightR":
        Rest_ofString = "Wei_Rej"
        List_String = [step,Rest_ofString]
        Joinedst = "_".join( List_String)
        out = list(Stepdf[Joinedst])
    elif OutType =="WeightA":
        Rest_ofString = "Wei_Acc"
        List_String = [step,Rest_ofString]
        Joinedst = "_".join( List_String)
        out = list(Stepdf[Joinedst])
    elif OutType =="ContR":
        Rest_ofString = "CFU_Rej"
        List_String = [step,Rest_ofString]
        Joinedst = "_".join( List_String)
        out = list(Stepdf[Joinedst])
    elif OutType =="ContA":
        Rest_ofString = "CFU_Acc"
        List_String = [step,Rest_ofString]
        Joinedst = "_".join( List_String)
        out = list(Stepdf[Joinedst])     
    else:
        print("Type arguement defined incorrectly")
    return out


def F_Output_get_cols(Outdf, ColNames):
    #Colnames is a list of columns that we wish to extract from the dataframe.
    Outs = Outdf[ColNames]
    return Outs #return Subset of desired Columns
    
    

