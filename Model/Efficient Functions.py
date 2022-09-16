# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 13:28:22 2022

@author: gareyes3
"""

import Funz_T
import Inputz_T
import numpy as np
import random
import pandas as pd
import numpy as np
import math
import time

from numpy.random import Generator, PCG64
rng = Generator(PCG64())



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

Field_df["CFU"] = 100

def F_CrossContProLine_tom (df, Tr_P_S, Tr_S_P,  Location, Sanitation_Freq_lb = 0, StepEff = 0 , compliance = 0):
        df_field_1 =df.loc[df["Location"]==Location].copy()
        rateweight = 0.57
        every_x_many = int(Sanitation_Freq_lb/rateweight)
        ContS=0
        vectorCFU = df_field_1["CFU"].copy()
        index_vec = np.array(vectorCFU.index)
        vectorCFU = np.array(vectorCFU)
        newvector=[]
        if every_x_many > 0:
            Cleaning_steps = np.arange(0, len(vectorCFU) , every_x_many )
        for i in index_vec:
            if compliance>0: #to not run if there is no sanitation.
                if random.uniform(0,1)<compliance:
                    if every_x_many > 0:
                        if i in Cleaning_steps:
                            ContS = ContS*10**StepEff
                            print ("cleaned")
            ContP = vectorCFU[i] #Contamination product
            TotTr_P_S= rng.binomial(ContP,Tr_P_S) #Transfer from Product to Surfaces
            TotTr_S_P = rng.binomial(ContS,Tr_S_P) #Trasnfer from Surfaces to product
            ContPNew = ContP-TotTr_P_S+TotTr_S_P #New Contmination on Product
            ContS=ContS+TotTr_P_S-TotTr_S_P #Remiining Contamination in Surface for upcoming batches
            newvector.append(ContPNew)
        df_field_1.loc[:,"CFU"] = newvector
        df.update(df_field_1)
        return df

start_df = time.time()
Field_df=F_CrossContProLine_tom (df = Field_df, 
                                 Tr_P_S = Inputz_T.Tr_P_CB, 
                                 Tr_S_P = Inputz_T.Tr_CB_P,
                                 Location = 1,
                                 Sanitation_Freq_lb = 0, 
                                 StepEff = 0 , 
                                 compliance = 0 )

print(time.time() - start_df, "CC")

aaaaa=np.zeros(5)
aaaaa =np.append(aaaaa,2)
aaaaa.append(10)

np.array([])
