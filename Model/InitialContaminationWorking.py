# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 13:59:11 2022

@author: Gustavo Reyes
"""

#Initial Contamination figuring it out
import numpy as np
import SCInputz
import random
import funz
from scipy.stats import beta


#Assisting Functions
def pert(a, b, c, *, size=1, lamb=4):
    r = c - a
    alpha = 1 + lamb * (b - a) / r
    beta = 1 + lamb * (c - b) / r
    return float(a + np.random.beta(alpha, beta, size=size) * r)

def betagen(a,b,mini,maxi):    
    return float(beta.rvs(a , b)* (maxi - mini) + mini)


#Contamination from irrigation water pang et al
def F_InitialCont():
    #Using base pert distribution
    #Calculation of total CFUs
    Cont_CFU_g = float(pert(0,0,634))
    g_field = SCInputz.Field_Weight*454 #454 g in 1 lb. 
    Final_Cont = int(Cont_CFU_g*g_field)
    return Final_Cont

#Daily Event

Holding_Time = int(np.random.triangular(2,4,8))
probability_irrigation_day = (1/7)
days=list(range(1,(14-Holding_Time)+1))
random.choices(days,[0.8]*len(days))

days_picked = [i for i in days if probability_irrigation_day>np.random.uniform(0,1)]

F_InitialCont()





#Scenario 1, irrigation water contaminated.
Ecoli_soil = np.random.normal(0.549,0.816) #log10 CFU/g
P_Ecoli_Water = 0.35
PosYN_Ecoli_Water = np.random.binomial(1,P_Ecoli_Water)
C_Ecoli_Water = (10**np.random.normal(0.604,0.357))/10 #CFU/ml water

Tr_Irr_Water = np.random.uniform(1.8,21.6) #ml/g produce
Pr_Irr_Splashing = pert(0.02,0.04,0.05)
Pr_Rain_Splashing = 1
Soil_Transfer = betagen(0.4,0.8,0.05,16.4)
P_Soil_Plant = np.random.uniform(0.35,0.9)

Increase_Irrigation =C_Ecoli_Water*Tr_Irr_Water*PosYN_Ecoli_Water #CFU/g
Increase_IrrigationCFU = Increase_Irrigation*(454*100_000)
        
#Scenario 2 Rain splashing
Increase_RainSplash = (10**Ecoli_soil)*Soil_Transfer*P_Soil_Plant*Pr_Rain_Splashing
Increase_RainSplashCFU = Increase_RainSplash*(454*100_000)

#Scenario 3 Irrigation water splash
Increase_IrrigationSplash = (10**Ecoli_soil)*Soil_Transfer*P_Soil_Plant*Pr_Irr_Splashing
Increase_IrrigationSplashCFU = Increase_IrrigationSplash *(454*100_000)

#Scenario 4 Ferral Swine Defecation foliar irrigation: (Clustered Contamination)
amount_ferralloc = 4260 #mass of feces a day #456 g
amount_feralprec = 1_000 #g
amount_cattleprec = 10_000 #g

Cont_Ferral=np.random.lognormal(-1.26,2.2)
Cont_Ferral_CFU=10**Cont_Ferral
CFU_ferralloc_CFU = amount_ferralloc*Cont_Ferral_CFU
print(CFU_ferralloc_CFU)

def transfer_1(val):
    if val<=0.619:
        trans = 1.3*(val-0)/(0.619-0)
    elif (val>=0.619) and (val<=0.946):
        trans = 1.3+((340-1.3)*(val-0.619)/(0.946-0.619))
    else:
       trans = 340+((230000-340)*(val-0.946)/(1-0.946)) 
    return trans

#Transfer Ratio
tr=transfer_1(np.random.uniform(0,1))/(1.29*10**8)
print(tr)

CFU_ferralloc_CFU*tr

#Scenario 5 Ferral swine defectation






#We will do the final 14 DAYS
Contamination_Event= np.random.choice([1,2,3,4])
#1 = Contaminated Irrigation water
#2=  Contaminated feces from feral swine
#3 = Contamination from runoff of contamination 

Month = np.random.choice([1,2,3,4,5,6,7,8,9,10,11,12 ])
Irrigation_m = [0.861194671,0.921357972,0.972496777,0.484588038,0.135367426,0.03824667,0,0.012462398,0.03008165,0.280189085,0.496347228,0]


#cattle feces
np.random.normal(-1.15,2.57) # log CFU _gram
    # 2 ways to soil
    #1. Direct defectation
    #2. Precipitation runoff
    
#Precipitation: 
PrecNorm = (48-0.1)/(59.1-0.1) #normalization of precipitation for a month

amount_ferralloc = 4260 #mass of feces a day #456 g
amount_feralprec = 1_000 #g
amount_cattleprec = 10_000 #g


np.random.lognormal(-29.13,9.72,1)*454*100_000
