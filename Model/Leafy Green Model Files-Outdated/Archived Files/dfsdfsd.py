# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 13:49:05 2021

@author: gareyes3
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

CFU= [0,0,0,0,0,0,0,0,0,0,1000,0,0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,0,
    0,0,0,0,1000,0,0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0,1000,
    0,0,0,0,0,0,0,0,0,0,0,1000,0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,0,
    0,0,0,0,0,1000, 0,0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0,1000,0,0,0,0,0,0,1000, 
    0,0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0,1000,0,0,0,0,0,0]
df = pd.DataFrame(CFU)
df=df.rename(columns={0 : "CFU"})

plt.figure(figsize = (10,10))
plt.axis('off')
plt.imshow(df, cmap='viridis',extent=[100,0,0,1], aspect=1000)
plt.show()

#CFU_Non = (TR(decimal)*(CFU non inoculatred + CFU wash Water))
def Washing_Batch(df, New_water_every_xpacks):
    Contamination_Vector = df['CFU']
    Rangeofiterations = list(range(0,len(Contamination_Vector)))
    if New_water_every_xpacks == 0:
         every_so = []
    else:
        every_so = Rangeofiterations[::New_water_every_xpacks]
    Log_Red_WashW = np.random.uniform(1.87,2.23)
    TrRatetoNI = (1*10**np.random.normal(0.0,0.3))/100 #check this fit
    Cont_Water =0
    for i in range(len(Contamination_Vector)):
        if i in every_so:
            Cont_Water = 0
        print(i)
        Cont =  Contamination_Vector[i]
        if Cont>0:
            New_Cont = Cont*10**-Log_Red_WashW
            Cont_Water = Cont - New_Cont
            Contamination_Vector[i] = New_Cont
        elif Cont ==0:
            Transfer_W_NI = Cont_Water*TrRatetoNI
            New_Cont = Transfer_W_NI
            Cont_Water = Cont_Water -Transfer_W_NI 
            Contamination_Vector[i] = New_Cont
    df["CFU"] = Contamination_Vector
    return df

      
df2 =Washing_Batch(df=df,New_water_every_xpacks=5)

                                        

np.random.binomial(ContP,Tr_P_S)

dedede = list(range(0,len(CFU)))
every_so = dedede[::0]
Log_Red_WashW = np.random.uniform(1.87,2.23)
