# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 08:53:41 2021

@author: gareyes3
"""

import math
import pandas as pd
import numpy as np

F_W= 200000
P_W = 50
Y =None
X = None
Rat_H = 2
Rat_W = 5

Part_tot = F_W/P_W

Y = math.sqrt(Part_tot/Rat_H)
X = math.sqrt(Part_tot/Rat_W)

X*Y

Part_tot/(Rat_H*Rat_W)

W = math.sqrt(Part_tot/(Rat_H*Rat_W))

Y = Rat_H*W
X= Rat_W*W

X*Y


def F_Mapping (Field_Weight, Partition_Weight, Ratio_Height, Ratio_Width):
    Part_tot = Field_Weight/Partition_Weight
    W = math.sqrt(Part_tot/( Ratio_Height* Ratio_Width))
    Y = int(Rat_H*W)
    X= int(Rat_W*W)
    d = pd.DataFrame(np.zeros((Y, X)))
    return d
    


d2 =F_Mapping(Field_Weight = 200000, Partition_Weight=50, Ratio_Height=5, Ratio_Width=1)
    
    
    