# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 09:18:35 2022

@author: gareyes3
"""
#%%
import sys
sys.path
sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility_L_T\Model')
sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility_L_T\Model')

#%%
import Inputz_T
import pandas as pd
import numpy as np
import math

#%%
Field_df=pd.DataFrame({"Tomato_ID": Inputz_T.Individual_Tomatoes,
                       "Plant_ID": Inputz_T.Individual_Plants[0:Inputz_T.Individual_Tomatoes.size],
                       "Pick_ID": Inputz_T.Pick_Random[0:Inputz_T.Individual_Tomatoes.size],
                       "Weight": Inputz_T.Tomato_weight,
                       "Harvester" : 0,
                       "Bucket":0,
                       "Bin": 0,
                       "Case_PH": 0,
                       "CFU": 0,
                       "CFU_BRej":"",
                       "Location": 1,
                       'PositiveSamples':"",
                       "Rej_Acc" :"Acc"
                  })

#%%

def F_CC_Dicing(df):
    Weight = Inputz_T.Tomato_weight #tomato weight in lb
    Weight_kg = Weight*0.454
    V_conts = df["CFU"]
    V_conts = np.array(V_conts)
    count=0
    for i in V_conts[:-1]:
        log_CFU= np.log10(V_conts[count]/(Weight*454))
        log_CFU_trans=log_CFU*math.exp(Weight_kg/-8.31)
        CFU_trans = int((10**log_CFU_trans)*(Weight*454))
        V_conts[count] = V_conts[count]- CFU_trans
        V_conts[count+1] = V_conts[count+1]+CFU_trans
        count = count+1
    df["CFU"] = V_conts
    return(df)
        
df2 = Field_df.copy()
df2.at[0,"CFU"] = 627971

df3 = F_CC_Dicing(df= df2)

sum(df3["CFU"])



