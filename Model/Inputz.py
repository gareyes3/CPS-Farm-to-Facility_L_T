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
                                                              
# 0 Initial Inputs for Field Setup and Challenges


N_Iterations= 5

Field_Weight= 100000 #total lb in field
slot_weight = 10000 #weight of the sublot in field.
Partition_Weight = 1000 #Partition weight for contamination Events, Partition to have better definition of field. 

slot_number = int(Field_Weight/slot_weight) #Number of sublots per field
Partition_Units = int(Field_Weight/Partition_Weight) #Number of partition units per field


# Contamination Challenge Related Information
if ContCondz.Background_C ==True:
    BGHazard_lvl = 50000  #CFU # background contamination
    BGCluster_Size = 100000 #lb
    BGNo_Cont_Clusters = 1 #Number of contamination clusters here one uniform cluster, field size.
    #BackGround Contamination. 

if ContCondz.Point_Source_C ==True:
    PSHazard_lvl = 50000  #CFU # background contamination
    PSCluster_Size = 1000 #lb
    PSNo_Cont_Clusters = 4 #4 1000k lb clusters. 
    
if ContCondz.Systematic_C ==True: 
    SysHazard_lvl = 50000  #CFU # background contamination
    SysCluster_Size = 10000 #lb
    PSNo_Cont_Clusters = 1 #Number of contaminated clusters

 
if ContCondz.Crew_C == True: 
    CrewHazard_lvl = 50000  #CFU # background contamination
    CrewCluster_Size = 5000 #lb
    CrewNo_Cont_Clusters = 4 #Number of contaminated clusters


if ContCondz.Harvester_C==True:
    HCHazard_lvl = 50000  #CFU # background contamination
    HCCluster_Size = 50000 #lb
    HCNo_Cont_Clusters = 1 #Number of contaminated clusters
    
if ContCondz.PE_C == True:
    PECHazard_lvl = 50000  #CFU # background contamination
    Lines_Cont = 1
    
if ContCondz.Pack_C == True:
    PackHazard_lvl = 50000  #CFU # background contamination
    Lines_ContPack = 1        
    
    

# 0 Die-off in Field for first 3 contamination Events
Break_Point=Funz.Func_NormalTrunc(0.11,3.71,0.68,0.98) #Breaking point for Die Off from Belias et al. 
Dieoff1 = Funz.F_DieOff1() #from Belias et al. 
Dieoff2 = Funz.F_DieOff2() #from Belias et al. 

Lag_Consumed_Prev = 0


# 1 Pre-Harvest Inputs

sample_size_PH = 300 # (Input) g #Sample Size in grams for Pre Harvest
n_samples_slot_PH = 1 # (Input) Samples per sublot of product
No_Grabs_PH = 60 
Limit_PH = 0
if ScenCondz.PHS_Int ==True:
    n_samples_lot_PH = 10 # (Input) Samples per lot of product'


# 2 Harvest Inputs

#Options for the Sampling Scenarios 1,2,3
if ScenCondz.PHS_Int ==True :
    Time_PHS_H = 0 #Days #time from pre harvest sampling to harvest Sampling
elif ScenCondz.PHS_4h ==True:
    Time_PHS_H = 0.166 # 4Hours before harvest
elif ScenCondz.PHS_4d ==True:
    Time_PHS_H = 4 #4 days before harvest
else:
    Time_PHS_H = 4 #if not, baseline is always 4 hours

#Time between Contamination Event and Harvest Sampling
Time_CE_H = np.random.triangular(2,4,8) #days
#Here because of math
Time_CE_PHS= int(Time_CE_H-Time_PHS_H) #Days Time from Contamination Event (Irrigation) to Pre-Harvest Sampling
sample_size_H = 300 #g #Sample Size in grams
n_samples_slot_H = 1 # Samples per lot of product
No_Grabs_H = 60 

#PreCooling. 
Time_H_PreCooling = np.random.uniform(2,4)
Temperature_H_PreCooling = np.random.uniform(15,17)


# 3 Receiving
#PreCooling

#Storage at Receiving
Time_Storage_R = 5
Temperature_Storage_R = 5

Pallet_Weight = 4000  #weight of pallet in lb.  
n_samples_pallet = 1 #samples taken per pallet
sample_size_R = 300 #g #Sample Size in grams Receiving
No_Grabs_R = 3


# 4 Processing -Cross Contamination Inputs
# A Pre-Cooling
Time_R_PC = 2  #Days around 2hr
Processing_Lines = 4 #Number of processing lines of product

# B Cold Storage
#Infor for cold storage die-off. 
Time_ColdStorage = 24 #Days
Temperature_ColdStorage = 4 #C 

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

    #Shaker Table
Tr_St_P =np.random.triangular(0.06,0.28,0.30)
Tr_P_St =np.random.triangular(0,0.0006,0.0038)
    #Centrifuge
Tr_C_P =np.random.triangular(0.23,0.27,0.31)
Tr_P_C =np.random.triangular(0,0.0035,0.0159)


    
# 7 Final Product
Pack_Weight_FP = 5 #Weight of each pack. 
N_Lots_FP = 1 #Lost of final product
sample_size_FP = 300 #g #Sample Size in grams
n_samples_FP = 1 #number of samples per lot final product
N_Packages_Samples = 60
if ScenCondz.FPS_Agg ==True:
    n_samples_FP = 10
    

#Packaging into Cases
Case_Weight = 20 #lb




# 8 Post Processing Storage
Time_PostPStorage = 24 #hr
Temperature_ColdStorage = 4 #C 

#9 Transportartion post processing
Trasnportation_Time = 63.57 #h from Ryser et al
Transportation_Temp = np.random.triangular(0,4,6) #C

#10 Customer Storage

Time_PostPCS = 24 #hr
Temperature_PostPCS = 4 #C 



