# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:11:53 2021

@author: gareyes3
"""

#Filtering out the rejected lots. 

if ScenCondz.PHS_Int ==1:
    if sum(LL_Rej_Lots_PH)>0:
        df_MeanT = df.iloc[[0]]
        df_MeanT['CFU'] = 0
    df = df[~df['Lot'].isin(LL_Rej_Lots_PH)] 
    if sum(LL_Rej_Lots_PH)>0:
        df= df_MeanT
    
else: 
    df = df[~df['Sublot'].isin(LL_Rej_Lots_PH)]
    
    
def F_Rejection_Rule (df, LL_Rej_Lots, Test_Unit):
    #Test_Unit = "Lot" or "Sublot"
    Unique_TestUnit=list(df[Test_Unit].unique())
    if set(Unique_TestUnit)<= set(LL_Rej_Lots):
        df_Blank = df.iloc[[0]]
        df_Blank.loc[:, ['CFU']] = 0
        df_Blank.loc[:, ['Weight']] = 0
        df = df_Blank
    else:
        df = df[~df[Test_Unit].isin(LL_Rej_Lots)]
    return df
    
LL_Rej_Lots_PH = [1,6]
        
df_trial = F_Rejection_Rule(df = df, LL_Rej_Lots = LL_Rej_Lots_PH , Test_Unit = "Sublot")


df.loc[:, ['CFU']]=600
df.iloc[0,:]


List1 = [3,4,6]
List2 = [6,3,4,7]

set(List1) <= set(List2)
