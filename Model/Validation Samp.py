# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 10:37:22 2022

@author: gareyes3
"""

import math
from matplotlib import pyplot as plt
from matplotlib.ticker import ScalarFormatter
import seaborn as sns
import random

pdect_list_5=[]
CFU_list= list(range(0,10000,10))
for i in CFU_list:
    CFU = i
    CFU_grab = CFU*(6.5/(5*454))
    P_Detection=1-math.exp(-CFU_grab)
    pdect_list_5.append(P_Detection)
    
    
    
sns.scatterplot(CFU_list,pdect_list)

sns.scatterplot(CFU_list,pdect_list_5)


DF_2k=pd.DataFrame({"col": list(range(0,2000)),
              "CFU": 0})

DF_20K=pd.DataFrame({"col": list(range(0,20000)),
              "CFU": 0})

DF_2k.at[220:239, "CFU"] = 3000
DF_2k["CFU"].sum()


DF_20K.at[220:419, "CFU"] = 300
DF_20K["CFU"].sum()

DF_2k  = df

CFU_list= DF_2k["CFU"]
Finalresults_2k = []
for j in range(1000):
    total = 0
    for i in range(60):
        List_Random=random.choice(list(enumerate(CFU_list)))
        CFU = List_Random[1]
        CFU_grab = CFU*(6.25/(50*454))
        P_Detection=1-math.exp(-CFU_grab)
        pdect_list_5.append(P_Detection)
        RandomUnif = random.uniform(0,1)
        if RandomUnif < P_Detection:
            total=total+1
    Finalresults_2k.append(total)
    
Finalresults_2k=pd.Series(Finalresults_2k)
Finalresults_2k[Finalresults_2k>0].sum()/1000


DF_20K = df

CFU_list= DF_20K["CFU"]
Finalresults = []
for j in range(1000):
    total = 0
    for i in range(60):
        List_Random=random.choice(list(enumerate(CFU_list)))
        CFU = List_Random[1]
        CFU_grab = CFU*(6.25/(5*454))
        P_Detection=1-math.exp(-CFU_grab)
        pdect_list_5.append(P_Detection)
        RandomUnif = random.uniform(0,1)
        if RandomUnif < P_Detection:
            total=total+1
    Finalresults.append(total)
    
Finalresults=pd.Series(Finalresults)
Finalresults[Finalresults>0].sum()/1000

