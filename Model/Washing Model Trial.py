# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 11:38:01 2021

@author: gareyes3


"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import math
import random
import itertools
from matplotlib import pyplot as plt






'''
#Setup
Time_Wash=Agg_WashTime
Times = np.arange(0, Time_Wash+0.1, 0.1).tolist()
Times = [round(num, 1) for num in Times]

C= 0 # ini #(mg/L) #Concentration of Free Chrloride available
O = 0  # Initial Oxygen deman
Pre_runningT = 0
RK = 1 #Dosing Period. 
Ro = 12 #Chlorine dosing period, ever 12 minutes
Ro0 = 2 #Minutes duration of dose
SigC = 1.70*(10**-3)
BC = 5.38*(10**-4)
K0 = 32.3 # free chroliride demand per min

r1= 12.75 #(mg/(ml/min**2))
r2 = 7.47 #(mg/(ml/min**2))
r3 = 5.56 #(mg/(ml/min**2))

'''

V = 890 #L

def F_Chloride_lvl (Time_Wash):
    Times = np.arange(0, Time_Wash+0.1, 0.1).tolist()
    Times = [round(num, 1) for num in Times]
    #Addition Rates
    r1= 12.75 #(mg/(ml/min**2))
    r2 = 7.47 #(mg/(ml/min**2))
    r3 = 5.56 #(mg/(ml/min**2))
    #Dose
    Ro = 12 #Chlorine dosing period, ever 12 minutes
    Ro0 = 2 #Minutes duration of dose
    #Time
    Pre_runningT = 0
    K0 = 32.3 # free chroliride demand per min
    C= 0 # ini #(mg/L) #Concentration of Free Chrloride available
    O = 0  # Initial Oxygen deman
    #Other parameters
    SigC = 1.70*(10**-3)
    BC = 5.38*(10**-4)
    for i in Times: 
        Running_Time = i
        Time_Interval = Running_Time-(Pre_runningT)
        if 0<= Running_Time <= (0+Ro0) :
            Rate = r1
            X = 1
        elif Ro <= Running_Time <= (Ro+Ro0) :
            Rate = r2
            X = 1
        elif 2*Ro <= Running_Time <= (2*Ro+Ro0) : 
            Rate = r3
            X = 1
        else: 
            X = 0
        dO = K0*Time_Interval
        O = O+dO
        decay = ((-SigC*Time_Interval)*C) - ((BC*Time_Interval)*O*C) 
        Increase = (Rate*X*Time_Interval)
        dC = decay + Increase
        C = C+dC
        Pre_runningT = i
    return C

C = F_Chloride_lvl(Time_Wash= 0.2)



TrialDF["CFU"] = 0
TrialDF.at[0,"CFU"] = 3000

#Bws = 1.95 #mpn/ ml*l : is the effective pathogen rate entering wash water (cfu/mL min)
Xw =0  #pathogen in process water MPN/ml
Xl = 0
WaterCont_List = []


TrialDF = gb2[0]
Agg_WashTime =0
WashT_Per_Pallet = 3 #min
Agg_WashTime = Agg_WashTime+WashT_Per_Pallet

for i, row in TrialDF.iterrows():
    AvCont = TrialDF.at[i,"CFU"] /(TrialDF.at[i,"Weight"]*454)
    AvContAfter = AvCont*10**-0.8
    FeedRate = (TrialDF.at[i,"Weight"]/WashT_Per_Pallet)*454
    Blw = 0.38 #ml/g min: is the pathogen binding rate to pieces of shredded lettuce heads
    L = 2225 #g of lettuce in wash tank
    V = 890000 #Wash Tank Volume L
    C= C
    alpha = 0.75
    Bws = ((AvCont- AvContAfter)*FeedRate)/V
    C1 = 2.3/ WashT_Per_Pallet
    
    CXw = Bws - (Blw*Xw*(L/V))- (alpha*Xw*C)
    Xw = Xw+CXw
    WaterCont_List.append(Xw)
    
    Xl = AvCont
    CXl = (Blw*Xw) -( alpha*Xl*C) - (C1*Xl)
    Xl =Xl +CXl
    print(Xl)
    AvCont = AvCont+CXl
    CFU_2 = AvCont*((TrialDF.at[i,"Weight"]*454))
    TrialDF.at[i,"CFU"] =  CFU_2

print(WaterCont_List)
WaterCont_List




#%%

for i in Times: 
    Running_Time = i
    Time_Interval = Running_Time-(Pre_runningT)
    if 0<= Running_Time <= (0+Ro0) :
        Rate = r1
        X = 1
        print("Yes")
    elif Ro <= Running_Time <= (Ro+Ro0) :
        Rate = r2
        X = 1
    elif 2*Ro <= Running_Time <= (2*Ro+Ro0) : 
        Rate = r3
        X = 1
    else: 
        X = 0
    dO = K0*Time_Interval
    O = O+dO

    decay = ((-SigC*Time_Interval)*C) - ((BC*Time_Interval)*O*C) 
    Increase = (Rate*X*Time_Interval)
    dC = decay + Increase
    L_dC.append(dC)
    C = C+dC
    L_c.append(C)
    Pre_runningT = i




































