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


WT = 1 #Wash time in Min
D= 6 #Free Chlorine dose mg/(mL*min^2)
DPfc = 6 #Free chloride adjustment period.

C = 0 #(mg/L) #Concentration of Free Chrloride available
O= 0 # (mg/l) #chemical oxygen demand
K0 = 32.3 # free chroliride demand per min

V = 1000
Rpw = 0.025

SigC = 1.70*10**-3
BC = 5.38*10**-4
alpha_1 = 0.502
BLW = 0.38

r1= 12.75 #(mg/(ml/min**2))
r2 = 7.47 #(mg/(ml/min**2))
r3 = 5.56 #(mg/(ml/min**2))
 
X=1 #0 or 1 depending if we are in feeding time or not
r0 = 2 #min duration of dose
Rate = r1

Running_Time = 12
O = Running_Time*K0
C = 25
X=0
print(O)
dC= (-SigC*C) - (BC*O*C) +  (Rate*X*2)     #dC is change in free chrloride to repect to time. 
print(dC)


L_Dc=[]
for i in range(30):
    Running_Time = i
    dO  = K0*Running_Time
    C=
    if Running_Time == 0 or 1 or 2:
        X= 1
        Rate = 12.75
    elif Running_Time == 12 or 13 or 14:
        X= 1
        Rate = 7.47
    elif Running_Time == 24 or 25 or 26:
        X= 1
        Rate = 7.47
    else:
        X = 0
        Rate = 0
    dC = ((-SigC*C) - (BC*O*C) +  (Rate*X*2)  )*Running_Time
    L_Dc.append(dC)
    
 
#Initital Conditions
O = 0
C = 0
 
L_c=[]
for i in range(1,30+1):
    Running_Time = i
    if Running_Time == 1 or 2:
        X= 1
        Rate = 12.75
    elif Running_Time == 12 or 13:
        X= 1
        Rate = 7.47
    elif Running_Time == 24 or 25:
        X= 1
        Rate = 7.47
    else:
        X = 0
        Rate = 0
    dO  = K0*Running_Time
    O=O+dO
    dC = ((-SigC*C) - (BC*O*C) +  (Rate*X*1))
    C = C+dC
    print(C)
    L_c.append(C)
    

L_c=[]
O = 0
C = 0


Running_Time = 1
Time_Ints=1
X=1
Rate = 12.75
dO  = K0*Time_Ints
O=O+dO
dC = ((-SigC*C) - (BC*O*C) +  (Rate*X*Time_Ints))
C = C+dC
print(C)
L_c.append(C)


#Setup
L_c=[]
L_dC=[]
Time_Wash=25
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
    

plt.plot(L_c)

plt.plot(L_dC)



Bws = 1.95 #mpn/ ml*l
Blw = 0.38 #ml/g min
Xw =4  #pathogen in process water MPN/ml
L = 2000 #kg of lettuce in wash tank
V = 100000 #Wash Tank Volume L
C= C
alpha = 0.75

Xl = 0.35  #pathogen on the lettuce in the tanks MPN/g
C1 = 2.3/ 8.3

CXw = Bws - Blw*Xw*(L/V) - alpha*Xw*C
print(CXw)

CXl = Blw* Xw - alpha*Xl*C - C1*Xl
print(CXl)

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




