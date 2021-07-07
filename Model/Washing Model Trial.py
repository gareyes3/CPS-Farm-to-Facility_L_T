# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 11:38:01 2021

@author: gareyes3
"""

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


Running_Time = 1
dO  = K0*Running_Time
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
dC = (-SigC*C) - (BC*O*C) +  (Rate*X*2)*12   
