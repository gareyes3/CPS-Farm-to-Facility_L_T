# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 08:41:01 2021

@author: gareyes3
"""

import math
import random
import Inputz
import time
import numpy as np

math.sqrt(100000)
100000/50

#New Sampling Function
def F_Sampling_2 (df, Test_Unit, NSamp_Unit, Samp_Size, Partition_Weight, NoGrab):
    Unique_TestUnit = list(df[Test_Unit].unique())
    Grab_Weight = Samp_Size/NoGrab
    for i in (Unique_TestUnit):
        for l in range (NSamp_Unit):
            for j in range(NoGrab):
                Sampled_Grab =df[df[Test_Unit] == i].sample(1, replace= True)
                Index = Sampled_Grab.index
                Index = Index[0]
                CFU = Sampled_Grab["CFU"]
                CFU_grab = CFU*(Grab_Weight/(Partition_Weight*454))
                P_Detection=1-math.exp(-CFU_grab)
                RandomUnif = random.uniform(0,1)
                if RandomUnif < P_Detection:
                    df.at[Index, 'Grabs']. append(NSamp_Unit)
    return (df)


start = time.time()
df3 = F_Sampling_2(df =df,Test_Unit ="Lot", 
                              NSamp_Unit = Inputz.n_samples_slot_PH, 
                              Samp_Size =Inputz.sample_size_PH, 
                              Partition_Weight =Inputz.Partition_Weight, 
                              NoGrab =300 )
end = time.time()
print(f"Runtime of the program is {end - start}")





Cdf = Funz.F_Chloride_lvl(300) 
mask = Cdf["Time"].values ==3
mask2 =Cdf[mask] 
mask2=mask2.reset_index()
C = mask2.at[0,"C"]


      





def F_Washing_ProcLines (List_GB3, Wash_Rate, Cdf):
    for j in List_GB3:
        WashT = len(j.index)
        #DF_Clvl = F_DF_Clvl(WashT)
        
        Times_W = np.arange(0, WashT, 1).tolist()
        Times_W = [round(num, 1) for num in Times_W]
        
        Blw = 0.47 #ml/g min: is the pathogen binding rate to pieces of shredded lettuce heads
        alpha = 0.52#Inactivation rate of pathogen via FC L/mgmin
        V = (3200 *1000) #L #From Luo et al 2012. 
        Rate = Wash_Rate/2.2  #45.45 #kg/min #From Luo et al 2012. 
        Wash_Time = 2.3 #min 
        c1 = 1/Wash_Time #Reciprocal of average time. 
        L = (Rate*1000)/(c1) #g of lettuce in the tak at the same time
        Xl = 0
        Xw =0  #pathogen in process water MPN/ml
        
        L_Xw = []
        L_Xl = []
        for i in Times_W:
            #Defining Initial Contamination
            Time = i
            AvCont = j.at[i,"CFU"] /(j.at[i,"Weight"]*454)
            AvContAfter = AvCont*10**-0.8
            mask = Cdf["Time"].values ==3
            mask2 =Cdf[mask] 
            mask2=mask2.reset_index()
            C = mask2.at[0,"C"]
            
            #C =   float(Cdf.loc[Cdf['Time'] == Time, 'C'])
            #C= F_Chloride_lvl(Time_Wash= Time)
            Bws = ((AvCont- AvContAfter)*Rate)/V
            CXw = Bws - (Blw*Xw*(L/V)) - (alpha*Xw*C)
            Xw = Xw+CXw
            if Xw<0:
                Xw = 0
            L_Xw.append(Xw)
            Xl = AvCont
            CXl = (Blw*Xw) - (alpha*Xl*C) - (c1*Xl)
            Xl =Xl +CXl
            if Xl < 0:
                Xl = 0
            L_Xl.append(Xl)
            AvCont = Xl
            CFU_2 = AvCont*((j.at[i,"Weight"]*454))
            j.at[i,"CFU"] =  CFU_2 
    return (List_GB3) 

'''
def F_CrossContProLine (gb2, Tr_P_S, Tr_S_P):
    ContS_L=[]
    for j in gb2:
        ContS=0
        for row in j.itertuples():
            i  = row[0]
            ContP = j.CFU[i] #Contamination product
            TotTr_P_S= np.random.binomial(ContP,Tr_P_S) #Transfer from Product to Surfaces
            TotTr_S_P = np.random.binomial(ContS,Tr_S_P) #Trasnfer from Surfaves to product
            ContPNew = ContP-TotTr_P_S+TotTr_S_P #New Contmination on Product
            ContS=ContS+TotTr_P_S-TotTr_S_P #Remiining Contamination in Surface for upcoming batches
            j.at[i,("CFU")]=ContPNew #Updating the Contamination in the Data Frame
        ContS_L.append(ContS)
    Outputs = [gb2,ContS_L]
    return Outputs


'''

''
def F_CrossContProLine (gb2, Tr_P_S, Tr_S_P):
    ContS_L=[]
    for j in gb2:
        ContS=0
        for i, row in j.iterrows():
            ContP = j.CFU[i] #Contamination product
            TotTr_P_S= np.random.binomial(ContP,Tr_P_S) #Transfer from Product to Surfaces
            TotTr_S_P = np.random.binomial(ContS,Tr_S_P) #Trasnfer from Surfaves to product
            ContPNew = ContP-TotTr_P_S+TotTr_S_P #New Contmination on Product
            ContS=ContS+TotTr_P_S-TotTr_S_P #Remiining Contamination in Surface for upcoming batches
            j.at[i,("CFU")]=ContPNew #Updating the Contamination in the Data Frame
        ContS_L.append(ContS)
    Outputs = [gb2,ContS_L]
    return Outputs
''

df.loc[3,"CFU"]
df.at[3,"CFU"] = 5000

df.at[3,"CFU"]
for row in df.itertuples():
    index_2 = row[0]
    print( index_2)

vector56 = [1,2,3,4,5,6]
range(len(vector56))

start = time.time()
db7 = F_CrossContProLine (gb2 =gb2, Tr_P_S = .1, Tr_S_P =.1)
end = time.time()
print(f"Runtime of the program is {end - start}")

start = time.time()
gb8 = F_Washing_ProcLines(List_GB3 =gb2, Wash_Rate = Inputz.Wash_Rate, Cdf =  DF_Chlevels)
end = time.time()
print(f"Runtime of the program is {end - start}")








