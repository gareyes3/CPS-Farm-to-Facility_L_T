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

#Assisting Functions
def pert(a, b, c, *, size=1, lamb=4):
    r = c - a
    alpha = 1 + lamb * (b - a) / r
    beta = 1 + lamb * (c - b) / r
    return a + np.random.beta(alpha, beta, size=size) * r



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
