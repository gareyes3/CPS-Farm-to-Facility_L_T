# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 11:21:44 2021

@author: gareyes3
"""
import random 
import numpy as np

Vector_of_lettuce = [20,25,15,30]


Cont = 10
Weight = 454 #g #1lb 


#Sredding
Shreder_Contamination = 20 #CFU
TE_S_L = 0.30
TE_L_S = 0.20

Vec_of_n_cont =[]
for i in Vector_of_lettuce:
    Cont_L = i
    Total_TR_S_L = Shreder_Contamination*TE_S_L
    Total_TR_L_S = Cont_L*TE_L_S
    
    Shreder_Contamination = Shreder_Contamination-Total_TR_S_L + Total_TR_L_S
    Cont_L = Cont_L +  Total_TR_S_L- Total_TR_L_S
    Vec_of_n_cont.append(Cont_L)
    
    







Cont