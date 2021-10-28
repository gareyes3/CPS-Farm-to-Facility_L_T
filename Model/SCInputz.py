# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 10:56:37 2021

@author: gareyes3
"""
import ScenCondz
import ContCondz
import Funz
import numpy as np    



#Initial Inputs for Field Setup and Challenges

N_Iterations= 5

Field_Weight= 100000 #total lb in field
slot_weight = 10000 #weight of the sublot in field.
Partition_Weight = 50 #Partition weight for contamination Events, Partition to have better definition of field. 

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
    SysNo_Cont_Clusters = 1 #Number of contaminated clusters

 
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


#Sampling Inputs. 

#Pre_Harvest   

sample_size_PH = 375 # (Input) g #Sample Size in grams for Pre Harvest
n_samples_slot_PH = 1 # (Input) Samples per sublot of product
No_Grabs_PH = 60 
Limit_PH = 0
RR_PH_Trad = "Sublot" #Reject by Sublot
#Intesne pre-harvest sampling
if ScenCondz.PHS_Int ==True:
    n_samples_lot_PH = 10 # (Input) Samples per lot of product'
    RR_PH_Int = "Lot"

#Harvest Inputs: 
sample_size_H = 375 #g #Sample Size in grams
n_samples_slot_H = 1 # Samples per lot of product
No_Grabs_H = 60 
Limit_H = 0
RR_H_Trad  = "Sublot"
#aggregative_prehavest sampling
if ScenCondz.HS_Agg ==True:
    n_samples_slot_H = 10 # (Input) Samples per lot of product'
    RR_H_Agg  = "Sublot"


#Receiving sampling:
n_samples_pallet = 1 #samples taken per pallet
sample_size_R = 125 #375 #g #Sample Size in grams Receiving
No_Grabs_R = 20
Limit_R =0
RR_R_Trad= "PalletNo"


#Finished Product Sampling: 
sample_size_FP = 375 #g #Sample Size in grams
n_samples_FP = 1 #number of samples per lot final product
N_Packages_Samples = 60
RR_FP_Trad = "Lot"
if ScenCondz.FPS_Agg ==True:
    n_samples_FP = 10
Limit_FP =0
RR_FP_Agg= "Lot"

#Receiving Sampling Field Pack/Also Final Product Sampling. 
n_samples_R_FP = 1
sample_size_R_FP = 375
No_GRabs_R_FP = 60
Limit_R_FP = 0
RR_R_FP_Trad  = "Lot"


