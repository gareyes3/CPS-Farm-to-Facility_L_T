# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 09:31:30 2021

@author: Gustavo Reyes
"""


                                                       #Inputs for the Model, Initial Inputs
import ScenCondz
import ContCondz
import Funz
import numpy as np   

                                                 
                                                              
#%% Die off

# 0 Die-off in Field for first 3 contamination Events
Break_Point=Funz.Func_NormalTrunc(0.11,3.71,0.68,0.98) #Breaking point for Die Off from Belias et al. 
Dieoff1 = Funz.F_DieOff1() #from Belias et al. 
Dieoff2 = Funz.F_DieOff2() #from Belias et al. 

#Lag Consumed for Growth models, always starts at 0, updated in model.
Lag_Consumed_Prev = 0


#%% Time Pre-Harvest HArvest
#Time between Contamination Event and Harvest Sampling *** Scenario Control
if ScenCondz.Holding_Time == True: #Should always be true unless scenario analysis. 
    Time_CE_H = np.random.triangular(2,4,8) #days
elif ScenCondz.Holding_Time == False:
    Time_CE_H = np.random.triangular(0,4,8) #days 



#Time Options for the Sampling Scenarios 1,2,3
if ScenCondz.PHS_Int ==True :
    Time_PHS_H = 0 #Days #time from pre harvest sampling to harvest Sampling
elif ScenCondz.PHS_4h ==True:
    Time_PHS_H = 0.166 # 4Hours before harvest
elif ScenCondz.PHS_4d ==True:
    Time_PHS_H = 4 #4 days before harvest
else:
    Time_PHS_H = 0 #if not, baseline is always 4 hours


    
#Here because of math
if Time_PHS_H>Time_CE_H:
    Time_CE_PHS = 0 #No time in contamination Event. 
elif Time_PHS_H<=Time_CE_H:
    Time_CE_PHS= Time_CE_H-Time_PHS_H #Days Time from Contamination Event (Irrigation) to Pre-Harvest Sampling

#%% Pre-Cooling- HArvest

#Chrlorine Pray
Harvest_Cspray_red = np.random.uniform(1.1,1.4) # log reduction achieved by chlorination spray. Prachi Pahariya 2022. 

#PreCooling. 
Time_H_PreCooling = np.random.uniform(2,4)
Temperature_H_PreCooling = np.random.uniform(15,17)

Time_PreCooling = np.random.uniform(0.4,0.6)  #Hours 25-35 minutes
Temperature_PreCooling = 3 #Precooling 3 C https://www.buschvacuum.com/us/en/news-media/pre-cooling-lettuces-reliably-thanks-to-cutting-edge-vacuum-technology.html


#%% Field Pack
#Field Packed Lettuce:
Case_Weight_FieldPack = 25 #lb


#%% Receiving

#Storage at Receiving
Time_Storage_R = 5
Temperature_Storage_R = 5
#PAllet size
Pallet_Weight = 4000  #weight of pallet in lb. 
 

#%% Processing
Time_R_PC = 2  #Days around 2hr, Time between 
Processing_Lines = 4 #Number of processing lines of product

# B Cold Storage
#Infor for cold storage die-off. 
Time_ColdStorage = 24 #Houts
Temperature_ColdStorage = np.random.normal(5.1,0.27) #C 

#Food Processing Events, Transfer Rates from 
#TR1 = np.random.triangular(0,0.01,0.02) #Transfer (%) from contaminated lettuce to flume
#TR2 = np.random.triangular(0,0.02,0.02) #Transfer (%) from contaminated lettuce to shredder
#TR3 = np.random.triangular(0,0.01,0.02) #Transfer (%) from contaminated lettuce to shaker
#TR4 = np.random.triangular(0.01,0.04,0.08) #Transfer (%) from contaminated lettuce to centrifuge
#TR5 = np.random.triangular(0,0.01,0.024) #Transfer (%) from contaminated lettuce to conveyor
#Tr_P_S = TR1+TR2+TR3+TR4+TR5 #Total transfer from Contminated Lettuce to Surfaces. 
#Tr_S_P = np.random.triangular(9.9,15.33,18.83) #Total Transfer from Surfaces to new product. 
#ContS=0 #Initial Contamination in Surfaces. 

#Processing Transfer Rates in %/100:
    #Shredder
Tr_Sh_P =np.random.triangular(0.16,0.20,0.28)
Tr_P_Sh =np.random.triangular(0,0.0025,0.0053)
    #Conveyor Belt
Tr_Cv_P =np.random.triangular(0.15,0.18,0.22)
Tr_P_Cv =np.random.triangular(0,0.0062,0.0139)

#Flume tank washing step
Wash_Rate = 100 #lb/min
DF_Chlevels = Funz.F_Chloride_lvl(300) #Simlating Chlorine levels after time.

    #Shaker Table
Tr_St_P =np.random.triangular(0.06,0.28,0.30)
Tr_P_St =np.random.triangular(0,0.0006,0.0038)
    #Centrifuge
Tr_C_P =np.random.triangular(0.23,0.27,0.31)
Tr_P_C =np.random.triangular(0,0.0035,0.0159)

  
#%% Final Product
Pack_Weight_FP = 5 #Weight of each pack. 
N_Lots_FP = 1 #Lost of final product
#Packaging into Cases
Case_Weight = 20 #lb #Only if not field packed


#%% Post Processing Storage
Time_PostPStorage = 24 #hr
Temperature_ColdStorage = 4 #C 

#%%Transportartion post processing
Trasnportation_Time = 63.57 #h from Ryser et al
Transportation_Temp = np.random.triangular(0,4,6) #C

#%%Customer Storage

Time_PostPCS = 24 #hr
Temperature_PostPCS = 4 #C 



    


