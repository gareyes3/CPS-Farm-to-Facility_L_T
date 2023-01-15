# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 12:37:55 2022

@author: gareyes3
"""
import numpy as np
import math
#Washing FC 

10**np.random.uniform(Log_Trans_Lower,Log_Trans_Upper)


Field_df.loc[list(range(100)),"CFU"] = 100000


Field_df_1 = Field_df.loc[list(range(1000)),"CFU"]


#def Tomato_Wash(df):

FC_lvl = 150 #np.random.triangular(0,5,10)
if FC_lvl<10:
    log_red_Wash_mean = (FC_lvl*0.04)+0.3
elif FC_lvl>10:
    log_red_Wash_mean = (FC_lvl*0.0056)+0.5952
    
logred_sd = 0.175

logred_cont = np.random.normal(log_red_Wash_mean, logred_sd)

#Transfer to uncontaminated pieces. 
Log_Trans_Upper = (-0.6798*FC_lvl)-0.6003
Log_Trans_Lower = (-1.3596*FC_lvl)-0.6

Field_df_1 =Field_df.loc[Field_df["Location"]==2].copy() #location 4 is wash water
Field_df_1_conts = Field_df_1["CFU"].copy()

Tras_old= 0


for i in list(Field_df_1_conts.index):
    #Parameters from https://www.sciencedirect.com/science/article/pii/S0963996916306081#f0010
    #Maffei. 
    #Backup https://www.sciencedirect.com/science/article/pii/S0740002019309694?casa_token=dt-V4Cbh89YAAAAA:FoQTt7f3Hly2-k9lJjUXPqkZ-W5tJChevsm2XIz3UTimqrYdUT9zAoqZUQlZWx1OhENvX3zqpqw
    
    Cont = Field_df_1_conts[i]
    
    logred_cont = -np.random.normal(log_red_Wash_mean, logred_sd)
    Percent_Trans = 10**np.random.uniform(Log_Trans_Lower,Log_Trans_Upper)
    
    if logred_cont>=0:
        GrowthCeil = math.ceil(logred_cont)
        Difference = logred_cont-GrowthCeil
        MaxCont = Cont*10**GrowthCeil
        Updated_CFUs = rng.binomial(MaxCont,10**Difference)
    else:
        Updated_CFUs= rng.binomial(Cont,10**logred_cont)

    Reduction = Updated_CFUs
    
    if i == 0:
        Field_df_1_conts[i] = Reduction
    if i >0:
        Field_df_1_conts[i] = Reduction + Tras_old
    Cont = Field_df_1_conts[i]
    Transfer = rng.binomial(Cont,Percent_Trans)
    Tras_old = Transfer
    
Field_df_1.loc[:, "CFU"] = Field_df_1_conts
df.update(Field_df_1)
    
    return df
    
        
Field_df= Tomato_Wash(df = Field_df)
