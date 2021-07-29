# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 09:31:30 2021

@author: Gustavo Reyes
"""


                                                       #Inputs for the Model, Initial Inputs
import ScenCondz
import Funz
import numpy as np                                                    
                                                              
# 0 Initial Inputs for Field Setup and Challenges



Field_Weight= 100000 #total lb in field
slot_weight = 10000 #weight of the sublot in field.
Partition_Weight = 1000 #Partition weight for contamination Events, Partition to have better definition of field. 

slot_number = int(Field_Weight/slot_weight) #Number of sublots per field
Partition_Units = int(Field_Weight/Partition_Weight) #Number of partition units per field


# Contamination Challenge Related Information
if ScenCondz.Background_C ==1:
    Hazard_lvl = 50000  #CFU # background contamination
    Cluster_Size = 100000 #lb
    No_Cont_Clusters = 1 #Number of contamination clusters here one uniform cluster, field size.
    #BackGround Contamination. 

if ScenCondz.Point_Source_C ==1:
    Hazard_lvl = 50000  #CFU # background contamination
    Cluster_Size = 1000 #lb
    No_Cont_Clusters = 4 #4 1000k lb clusters. 
    
if ScenCondz.Systematic_C ==1: 
    Hazard_lvl = 50000  #CFU # background contamination
    Cluster_Size = 10000 #lb
    No_Cont_Clusters = 1 #Number of contaminated clusters

 

if ScenCondz.Crew_C == 1: 
    Hazard_lvl = 50000  #CFU # background contamination
    Cluster_Size = 5000 #lb
    No_Cont_Clusters = 4 #Number of contaminated clusters


if ScenCondz.Harvester_C==1:
    Hazard_lvl = 50000  #CFU # background contamination
    Cluster_Size = 50000 #lb
    No_Cont_Clusters = 1 #Number of contaminated clusters
    
if ScenCondz.PE_C == 1:
    Hazard_lvl = 50000  #CFU # background contamination
    Lines_Cont = 1
    
if ScenCondz.Pack_C == 1:
    Hazard_lvl = 50000  #CFU # background contamination
    Lines_ContPack = 1        
    
    

# 0 Die-off in Field for first 3 contamination Events
Break_Point=Funz.Func_NormalTrunc(0.11,3.71,0.68,0.98) #Breaking point for Die Off from Belias et al. 
Dieoff1 = Funz.F_DieOff1() #from Belias et al. 
Dieoff2 = Funz.F_DieOff2() #from Belias et al. 


# 1 Pre-Harvest Inputs

sample_size_PH = 300 # (Input) g #Sample Size in grams for Pre Harvest
n_samples_slot_PH = 1 # (Input) Samples per sublot of product
No_Grabs_PH = 60 
Limit_PH = 0
if ScenCondz.PHS_Int ==1:
    n_samples_lot_PH = 5 # (Input) Samples per lot of product'


# 2 Harvest Inputs

#Options for the Sampling Scenarios 1,2,3
if ScenCondz.PHS_Int == 1:
    Time_PHS_H = 0 #Days #time from pre harvest sampling to harvest Sampling
elif ScenCondz.PHS_4h ==1:
    Time_PHS_H = 0.166 # 4Hours before harvest
elif ScenCondz.PHS_4d ==1:
    Time_PHS_H = 4 #4 days before harvest
else:
    Time_PHS_H = 4 #if not, baseline is always 4 hours

#Time between Contamination Event and Harvest Sampling
Time_CE_H = 6 #days
#Here because of math
Time_CE_PHS= int(Time_CE_H-Time_PHS_H) #Days Time from Contamination Event (Irrigation) to Pre-Harvest Sampling
sample_size_H = 300 #g #Sample Size in grams
n_samples_slot_H = 1 # Samples per lot of product
No_Grabs_H = 60 


# 3 Receiving
#Growth rate or die off from harvest to receiving
Time_H_RS = 1 # 1 hr. Days,Time from Harvest Sampling to Receiving Sampling,
Temperature_H_RS = 25 #C  
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
N_Lots_FP = 2 #Lost of final product
sample_size_FP = 300 #g #Sample Size in grams
n_samples_FP = 1 #number of samples final product
if ScenCondz.FPS_Trad ==1:
    N_Packages_Samples = 60
    Grab_Weight = 5 #g
    


# 8 Post Processing Storage
Time_PostPStorage = 24 #hr
Temperature_ColdStorage = 4 #C 

#9 Transportartion post processing
Trasnportation_Time = 63.57 #h from Ryzer et al
Transportation_Temp = 4 #C


