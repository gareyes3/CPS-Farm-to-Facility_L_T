# -*- coding: utf-8 -*-
"""
Created on Fri May 28 09:42:31 2021

@author: Gustavo Reyes
"""

#%%

import sys
sys.path
#sys.path.append('C:\\Users\Gustavo Reyes\Box\CPS Project- Farm to Facility\Python Model Files')
sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model')
#sys.path.append("C:\\Users\\reyes\\Box Sync\\CPS Project- Farm to Facility\\Python Model Files")

########################################Paths#################################################
#os.chdir('C:\\Users\Gustavo Reyes\Box\CPS Project- Farm to Facility\Python Model Files')
#os.chdir("C:\\Users\\reyes\\Box Sync\\CPS Project- Farm to Facility\\Python Model Files")
#os.chdir('C:\\Users\Gustavo Reyes')
#print(os.getcwd())
#%% 
#Libraries, Modules
import pandas as pd 
import numpy as np
import scipy.stats as stats
import math
import os
import random
import seaborn as sns
from matplotlib import pyplot as plt
import Funz
#from itertools import cycle
#%%
                                                                #Scenarios and Conditions
#Sampling Conditions, Baseline all conditions are off
Baseline_Sampling= 0 #all others must be 0if this one is 1
PH_Sampling = 0
H_Sampling = 0
R_Sampling = 0
FP_Sampling =1

#Additional Sampling Conditions. Env and 
Water_SamplingProc = 0
Env_SamplingProc =0
Env_SamplingCust = 0
Water_SamplingCust = 0

#Contamination Challenges
#In Field
Background_C=0
Point_Source_C=0
Systematic_C=1

#Harvester Contamination
Crew_C = 0
Harvester_C = 0 

#Processing equipment
PE_C = 0



#Sampling Options

#Pre-Harvest
    #Pre-Harvest sampling must be on
PHS_4d= 0 #Scenario 1
PHS_4h = 0#Scenario 2
PHS_Int = 0 #Scenario 3

#Harvest: 
    #HArvest Sampling must be one
HS_Trad = 0
HS_Agg = 0

#Final Product Sampling
    #Final Product sampling must be on.
FPS_Trad =0
FPS_Agg = 1 


#%%
                                                                    #List to collect outputs
#Before_PH sampling 
LBPH_Total_CFU=[]

#After_PH_sampling
Total_PA_PH = []
Total_PR_PH = []
Total_CR_PH = []
Total_CA_PH = []
LTotal_CFU_g_PH = []

#Before_H sampling
LBH_Total_CFU=[]

#After H Sampling
Total_PR_H = []
Total_PA_H = []
Total_CR_H = []
Total_CA_H = []

#Before R Sampling
LBR_Total_CFU=[]

#After R Sampling
Total_PR_R = []
Total_PA_R = []
Total_CR_R = []
Total_CA_R = []

#Before FP Sampling
LBFP_Total_CFU=[]

#After FP Sampling
Total_PR_FP = []
Total_PA_FP = []
Total_CR_FP = []
Total_CA_FP = []

LTotal_CFU_g_FP = []

LCont_PercRej_PH = []
LCont_PercRej_H = []
LCont_PercRej_R = [] 
LCont_PercRej_FP=[]


#%%

for i in range(100):
       
                                                                    #Inputs for the Model, Initial Inputs
                                                                  
    # 0 Initial Inputs for Field Setup and Challenges
    
    Field_Weight= 100000 #total lb in field
    slot_weight = 10000
    Cluster_Weight = 1000
    
    slot_number = int(Field_Weight/slot_weight)
    Cluster_Units = int(Field_Weight/Cluster_Weight)
    Cluster_Unit_weight = Field_Weight/Cluster_Units
    
    #Challenge Related Information
    if Background_C ==1:
        Hazard_lvl = 50000  #CFU # background contamination
        Cluster_Size = 100000 #lb
        No_Cont_Clusters = 1
    
        
    if Point_Source_C ==1:
        Hazard_lvl = 50000  #CFU # background contamination
        Cluster_Size = 1000 #lb
        No_Cont_Clusters = 4
        No_Cont_ClustersUnits = int(Cluster_Size/Cluster_Weight) #Cluster Units per Contaminatrion Cluster
    
        
    if Systematic_C ==1: 
        Hazard_lvl = 50000  #CFU # background contamination
        Cluster_Size = 10000 #lb
        No_Cont_Clusters = 1
        No_Cont_ClustersUnits = int(Cluster_Size/Cluster_Weight)
     

    if Crew_C == 1: 
        Hazard_lvl = 50000  #CFU # background contamination
        Cluster_Size = 5000 #lb
        No_Cont_Clusters = 4
        No_Cont_ClustersUnits = int(Cluster_Size/Cluster_Weight) #Cluster Units per Contaminatrion Cluster
    
    if Harvester_C==1:
        Hazard_lvl = 50000  #CFU # background contamination
        Cluster_Size = 50000 #lb
        No_Cont_Clusters = 1
        No_Cont_ClustersUnits = int(Cluster_Size/Cluster_Weight) #Cluster Units per Contaminatrion Cluster
    
    # 0 Die-off
    Break_Point=Funz.Func_NormalTrunc(0.11,3.71,0.68,0.98) #Breaking point for Die Off
    Dieoff1 = -0.5 #Funz.F_DieOff1()
    Dieoff2 = -0.5 #Funz.F_DieOff2()
    Time_Agg = 0
    
    
    # 1 Pre-Harvest Inputs

    sample_size_PH = 300 #g #Sample Size in grams
    n_samples_slot_PH = 1 # Samples per sublot of product
    if PHS_Int ==1:
        n_samples_lot_PH = 15 #Samples per lot of product
    
    # 2 Harvest Inputs
        #Options for the Sampling Scenarios 1,2,3
    if PHS_Int == 1:
        Time_PHS_H = 0 #Days #time from pre harvest sampling to harvest Sampling
    elif PHS_4h ==1:
        Time_PHS_H: 0.166
    elif PHS_4d ==1:
        Time_PHS_H = 4
    
    #Time between Contamination Event and HArvest Sampling
    Time_CE_H = 6 #days
    #Here because of math
    Time_CE_PHS= int(Time_CE_H-Time_PHS_H) #Days Time from Contamination Event (Irrigation) to Pre-Harvest 
    sample_size_H = 300 #g #Sample Size in grams
    n_samples_slot_H = 1 # Samples per lot of product
    
    # 3 Receiving
    Time_H_RS = 0.25 # Days,Time from Harvest Sampling to Receiving Sampling 
    Pallet_Weight = 4000   
    n_samples_pallet = 1 #samples taken per pallet
    sample_size_R = 300 #g #Sample Size in grams Receiving
    
    #Growth rate or die off from harvest to receiving
    Die_Off_HS_RS= 0 #Growth Rate , Die_off/growth from Harvest-Receiving CFU/g
    
    # 4 Processing -Cross Contamination Inputs
    # A Pre-Cooling
    Time_R_PC = 0.1 #Days
    Processing_Lines = 4
    
    # B Cold Storage
    Time_ColdStorage = 1 #Days
    Temperature_ColdStorage = 4 #C
    
    TR1 = np.random.triangular(0,0.01,0.02) #Transfer (%) from contaminated lettuce to flume
    TR2 = np.random.triangular(0,0.02,0.02) #Transfer (%) from contaminated lettuce to shredder
    TR3 = np.random.triangular(0,0.01,0.02) #Transfer (%) from contaminated lettuce to shaker
    TR4 = np.random.triangular(0.01,0.04,0.08) #Transfer (%) from contaminated lettuce to centrifuge
    TR5 = np.random.triangular(0,0.01,0.024) #Transfer (%) from contaminated lettuce to conveyor
    Tr_P_S = TR1+TR2+TR3+TR4+TR5
    Tr_S_P = np.random.triangular(9.9,15.33,18.83)
    ContS=0
    
    # 5 Washing input
    LogRedWash= np.random.normal(1.2, 0.3)
    
        
    # 7 Final Product
    Partition_Weight = 10
    N_Lots_FP = 2
    sample_size_FP = 300 #g #Sample Size in grams
    n_samples_FP = 1
    
    

                                                            #Step 0: DF Creation and Setup based on scenarios. 
    #Creation of the Data Frame to Track: 
    data = {'Lot': 1,
            'Sublot':0,
            'ClusterID': list(range(1,Cluster_Units+1)),
            'CFU':0,
            'Accept': True,
            'Weight': Field_Weight/Cluster_Units}
    
    Sublot_Pattern = [i for i in range(1, slot_number+1) for _ in range(int(slot_number))]
    
    df = pd.DataFrame(data)
    df.Sublot = Sublot_Pattern
    df.index = range(1,Cluster_Units+1)
    
    #Adding Contamination depending on challenge Background
    if Background_C == 1:
        Ci= Hazard_lvl/Cluster_Units
        df.CFU =Ci
        
    #Adding Contamination depending on challenge Point_Source
    if Point_Source_C == 1:
        Hazard_lvl_C= Hazard_lvl/No_Cont_Clusters
        Ci = Hazard_lvl_C
        X_1= df.sample(No_Cont_Clusters)
        X_1 = list(X_1.ClusterID)
        df.loc[X_1,'CFU']= df['CFU'] + Ci

        
    #Adding Contamination depending on challenge Systematic Sampling
    if Systematic_C == 1:
        Hazard_lvl_C= Hazard_lvl/(No_Cont_ClustersUnits*No_Cont_Clusters)
        Ci = Hazard_lvl_C
        n = random.randint(0,len(df.index)- No_Cont_ClustersUnits)
        x_random_consecutive_rows = df[n:n + No_Cont_ClustersUnits]
        x_random_consecutive_rows = list(x_random_consecutive_rows['ClusterID'])
        df.loc[ x_random_consecutive_rows,'CFU']= df['CFU'] + Ci

                                                                      #Step 1: PREHARVEST
    #Die-off From Contamination Event to Pre-Havrvest
   
    Die_Off_CE_PHS =Funz.F_Simple_DieOff(Time_CE_PHS) #Funz.F_DieOff_IR_PH(Time_CE_PHS,Break_Point, Dieoff1, Dieoff2) #Die off rate from Irrigation to pre harvest sampling
    print(Die_Off_CE_PHS)
    df["CFU"] =  df["CFU"]*(10**Die_Off_CE_PHS)
    Time_Agg = Time_Agg + Time_CE_PHS #Cummulative time so far in the process.
        
    
    if PH_Sampling ==1: #If function to turn off Pre-Harvest Sampling
        if PHS_Int ==1:
            Rej_Lots_PH = Funz.F_Sampling(df =df,Test_Unit ="Lot", 
                                          NSamp_Unit = 15, 
                                          Samp_Size =sample_size_PH, 
                                          Clust_Weight =Cluster_Unit_weight, 
                                          Limit =0, NoGrab =60 )
        else:
        #Pre-Harvest Sampling, 
             Rej_Lots_PH = Funz.F_Sampling(df =df,Test_Unit ="Sublot", 
                                       NSamp_Unit = n_samples_slot_PH, 
                                       Samp_Size =sample_size_PH, 
                                       Clust_Weight =Cluster_Unit_weight, 
                                       Limit =0, NoGrab =60 )
    else: #If no pre harvest sampling, none rejected
        Rej_Lots_PH= [] 
        
    BPH_Tot_CFU = sum(df.CFU) #Contamination before sampling
    LBPH_Total_CFU.append(BPH_Tot_CFU) #List of contamination before sampling
    
    #Filtering out the Rejected lots, Pre-Harvest
    if PHS_Int ==1:
        df = df[~df['Lot'].isin(Rej_Lots_PH)]   
    else: 
        df = df[~df['Sublot'].isin(Rej_Lots_PH)]
                       
    
    #Summary of Pre-Harvest Sampling
    Total_Accepted_PH = sum(df.Weight) #Lb
    Total_Rejected_PH = Field_Weight-Total_Accepted_PH #Lb
    Cont_Accepted_PH = sum(df.CFU) # Total CFU
    Cont_Rejected_PH = BPH_Tot_CFU-Cont_Accepted_PH #Total CFU
    if Cont_Accepted_PH == 0:
        Cont_PercRej_PH = 1
    else:
        Cont_PercRej_PH = Cont_Rejected_PH/(Cont_Accepted_PH+Cont_Rejected_PH) #Percentage Rejected by H sampling
    
    
    #Outputs for Iterations
    Total_PA_PH.append(Total_Accepted_PH)
    Total_PR_PH.append(Total_Rejected_PH)
    Total_CA_PH.append(Cont_Accepted_PH)
    Total_CR_PH.append(Cont_Rejected_PH)
    LCont_PercRej_PH.append(Cont_PercRej_PH)
    

                                                                 #STEP 2: HARVEST
    
    #Pre-Harvest Sampling - Harvest Sampling Die off
    Time_Agg = Time_Agg + Time_PHS_H #Cummulative time so far in the process.
    Die_off_B = Funz.F_Simple_DieOff(Time_Agg)
    Die_Off_PHS_HS= Die_off_B-Die_Off_CE_PHS#Funz.F_DieOff_PHS_HS(Time_PHS_H, Time_Agg, Break_Point, Dieoff1, Dieoff2)
    print(Die_Off_PHS_HS)
    df['CFU'] = df['CFU']*(10**Die_Off_PHS_HS) #Updating Contmination to Show Total DieOff
    
    
    #Adding Contamination depending on challenge Systematic Sampling
    if Crew_C == 1:
        No_Cont_ClustersUnits = len(df.index)
        Hazard_lvl_C= Hazard_lvl/(No_Cont_ClustersUnits*No_Cont_Clusters)
        Ci = Hazard_lvl_C
        x_2 =[]
        ClusterIDs = list(df['ClusterID'])
        for i in range(No_Cont_Clusters):
            TrimClusterIDS = ClusterIDs[:len(ClusterIDs)-No_Cont_ClustersUnits]
            n = random.sample(TrimClusterIDS,1)
            n  = n[0]
            x_random_consecutive_rows = ClusterIDs[n:n + No_Cont_ClustersUnits]
            x_2.append(x_random_consecutive_rows)
            ClusterIDs = [x for x in ClusterIDs if x not in x_random_consecutive_rows]
        x_2 =[j for i in x_2 for j in i]
        df.loc[ x_2,'CFU']= df['CFU'] + Ci

    if Harvester_C == 1:
        No_Cont_ClustersUnits = len(df.index)
        Hazard_lvl_C= Hazard_lvl/(No_Cont_ClustersUnits*No_Cont_Clusters)
        Ci = Hazard_lvl_C
        x_2 =[]
        ClusterIDs = list(df['ClusterID'])
        for i in range(No_Cont_Clusters):
            TrimClusterIDS = ClusterIDs[:len(ClusterIDs)-No_Cont_ClustersUnits]
            n = random.sample(TrimClusterIDS,1)
            n  = n[0]
            x_random_consecutive_rows = ClusterIDs[n:n + No_Cont_ClustersUnits]
            x_2.append(x_random_consecutive_rows)
            ClusterIDs = [x for x in ClusterIDs if x not in x_random_consecutive_rows]
        x_2 =[j for i in x_2 for j in i]
        df.loc[ x_2,'CFU']= df['CFU'] + Ci
    
    
    #Harvest Sampling
    if H_Sampling == 1:
        if HS_Trad==1:
            Rej_Lots_H = Funz.F_Sampling(df =df,Test_Unit ="Sublot", 
                                           NSamp_Unit = n_samples_slot_H, 
                                           Samp_Size =sample_size_H, 
                                           Clust_Weight =Cluster_Unit_weight, 
                                           Limit =0, NoGrab =60 )
        elif HS_Agg==1:
            Rej_Lots_H = Funz.F_Sampling(df =df,Test_Unit ="Sublot", 
                                           NSamp_Unit = 10, 
                                           Samp_Size =sample_size_H, 
                                           Clust_Weight =Cluster_Unit_weight, 
                                           Limit =0, NoGrab =60 )
    else:
        Rej_Lots_H=[]
        
    BH_Tot_CFU = sum(df.CFU) #Contamination before sampling
    LBH_Total_CFU.append(BH_Tot_CFU) #List of contaminations before sampling
    
    #Filtering out the Rejected lots, Pre-Harvest
    df = df[~df['Sublot'].isin(Rej_Lots_H)]
        
    
    #Summary of Harvest Sampling
    Total_Accepted_H = sum(df.Weight) #Total Accepted at HArvest
    Total_Rejected_H = Field_Weight-Total_Accepted_H
    Cont_Accepted_H = sum(df.CFU) #CFU
    Cont_Rejected_H =  BH_Tot_CFU-Cont_Accepted_H #CFU
    if Cont_Accepted_PH == 0:
        Cont_PercRej_H = "NA"
    else:
        Cont_PercRej_H = Cont_Rejected_H/(Cont_Accepted_H+Cont_Rejected_H) #Percentage Rejected by H sampling
    
    #Outputs for Iterations
    Total_PA_H.append(Total_Accepted_H)
    Total_PR_H.append(Total_Rejected_H)
    Total_CA_H.append(Cont_Accepted_H)
    Total_CR_H.append(Cont_Rejected_H)
    LCont_PercRej_H.append(Cont_PercRej_H)
    
    
                                                               #STEP 3: RECEIVING
    #Paletization
    
    Cluster_Pallet =  int(Pallet_Weight/Cluster_Weight)
    Pallet_Field = int(Field_Weight/Pallet_Weight)
    Pallet_Pattern = [i for i in range(1, Pallet_Field+1) for _ in range(int(Cluster_Pallet))]
    Crop_No = len(df.index)
    Pallet_Pattern=Pallet_Pattern[:Crop_No]
    df['PalletNo'] = Pallet_Pattern
    df = df[['Lot', 'Sublot','PalletNo','ClusterID','CFU','Accept', 'Weight']]
    No_Pallets = df.PalletNo.nunique()
    
    
    #Harvest Sampling - Receiving Harvest Sampling Die off
    Die_Off_HS_RS= Die_Off_HS_RS*Time_H_RS
    df['CFU'] = df['CFU']*(10**Die_Off_HS_RS) #Updating Contmination to Show Total DieOff

    Time_Agg = Time_Agg + Time_H_RS #Cummulative time so far in the process. 
    
    BR_Tot_CFU = sum(df.CFU)
    LBR_Total_CFU.append(BR_Tot_CFU)
    if R_Sampling == 1:
        #Sampling at Reception
        Rej_Pallets_R = Funz.F_Sampling(df =df,Test_Unit ="PalletNo", 
                                       NSamp_Unit = n_samples_pallet, 
                                       Samp_Size =sample_size_R, 
                                       Clust_Weight =Cluster_Unit_weight, 
                                       Limit =0, NoGrab =3 )
    else:
        Rej_Pallets_R = []
    #Rejecting Inidividual pallets if 1 positive
    df = df[~df['PalletNo'].isin(Rej_Pallets_R)]
    
    #Summary of Receiving Sampling
    Total_Accepted_R = sum(df.Weight)
    Total_Rejected_R = Field_Weight-Total_Accepted_R
    Cont_Accepted_R = sum(df.CFU) #CFU
    Cont_Rejected_R = BR_Tot_CFU-Cont_Accepted_R #CFU
    if Cont_Accepted_H == 0:
        Cont_PercRej_R = "NA"
    else:
        Cont_PercRej_R = Cont_Rejected_R/(Cont_Accepted_R+Cont_Rejected_R) #Percentage Rejected by H sampling
    
    Total_PA_R.append(Total_Accepted_R)
    Total_PR_R.append(Total_Rejected_R)
    Total_CA_R.append(Cont_Accepted_R)
    Total_CR_R.append(Cont_Rejected_R)
    LCont_PercRej_R.append(Cont_PercRej_R)
    
     
                                                                    #STEP 4: WASHING Reduction
    
    #Wash process reduction
    df=Funz.F_Washing(df, LogRedWash)
    
        
                                                             #STEP 4: VALUE ADDITION/ PROCESSING Includes Washing
    #Pre-Cooling of Lettuce
    Time_Agg = Time_Agg + Time_R_PC #Time from Receiving to Pre-Cooling
    # Process Pending, Reduction? 
    
    #Cold Storage:
    df = Funz.F_Growth(DF=df, Temperature=Temperature_ColdStorage, TimeD= Time_ColdStorage)#Growth during cold storage
    Time_Agg = Time_Agg + Time_ColdStorage #Time between Pre-Cooling and Cold Storage. 

    
    df2=df.groupby(['PalletNo'], as_index =False)[["CFU", "Weight"]].sum()
    
    #Splitting Pallets into processing lines. 
    N_Pallets = len(df2.index)
    num, div = N_Pallets, Processing_Lines #Getting list of pallets per line
    N_Divs =  ([num // div + (1 if x < num % div else 0)  for x in range (div)])
    
    
    #Value Addition Steps
    #Cross-Contamination Processing by batch, Assuming Every Pallet is a 1000k lb bath
    for i, row in df2.iterrows():
        ContP = df2.CFU[i] #Contamination product
        TotTr_P_S= ContP*(Tr_P_S/100) #Transfer from Product to Surfaces
        TotTr_S_P = ContS*(Tr_S_P/100) #Trasnfer from Surfaves to product
        ContPNew = ContP-TotTr_P_S+TotTr_S_P #New Contmination on Product
        ContS=ContS+TotTr_P_S-TotTr_S_P #Remiining Contamination in Surface for upcoming batches
        df2.CFU[i]=ContPNew #Updating the Contamination in the Data Frame
        
    df2['Lot'] =1#Updating the CFU/g column
        
    #Environmental Monitoring Program
    
    
    
                                               
                                                          #STEP 6: Finished Product Mixing and Sampling
    #Mixing products into one batch
    
    N_Partitions = int(Pallet_Weight/Partition_Weight)
    
    df2 = Funz.F_Partitioning(DF=df2, NPartitions= N_Partitions)
    if N_Lots_FP==2:
        df2 =Funz.F_Lots_FP(df=df2, Nolots = 2)
    
    
    
    BFP_Tot_CFU = sum(df2.CFU) #Total CFU before FP Sampling
    LBFP_Total_CFU.append(BFP_Tot_CFU) #Adding it to a List
    #df= Funz.F_Packaging(DF=df, Boxes_Pallet=Boxes_Pallet)
    
    #Sampling Step
    if FP_Sampling == 1:
        if FPS_Trad ==1:
            Rej_Lots_FP=Funz.F_SamplingFProd(df=df2, Test_Unit = 'PackNo', N_SampPacks = 60, Grab_Weight = 5 )
            print(Rej_Lots_FP)
        elif FPS_Agg ==1:
            Rej_Lots_H = Funz.F_Sampling(df =df2,Test_Unit ="Sublot", 
                                           NSamp_Unit = 10, 
                                           Samp_Size =sample_size_FP, 
                                           Clust_Weight =Partition_Weight, 
                                           Limit =0, NoGrab =60 )
    else :
        Rej_Lots_FP = []
    

    #Filtering out the Rejected lots, Pre-Harvest
    if FP_Sampling == 1:
        df2 = df2[~df2['Lot'].isin(Rej_Lots_H)]
    elif FPS_Agg ==1:
        df2 = df2[~df2['Sublot'].isin(Rej_Lots_H)]
    
    Total_Accepted_FP = sum(df2.Weight) #Total Product Accepted
    Total_Rejected_FP = Field_Weight-Total_Accepted_FP #Total Product Rejected
    Cont_Accepted_FP = sum(df2.CFU) #CFU Accepted
    Cont_Rejected_FP =  BFP_Tot_CFU-Cont_Accepted_FP #CFU Rejected from PH Sampling
    if Cont_Accepted_R == 0:
        Cont_PercRej_FP = "NA"
    else:
        Cont_PercRej_FP = Cont_Rejected_FP/(Cont_Accepted_FP+Cont_Rejected_FP) #Percentage Rejected by H sampling
        
    if Total_Accepted_FP == 0:
        Total_CFU_G_FP = 0 #Total CFU per gram of final product
    else:
        Total_CFU_G_FP = Cont_Accepted_FP/( Total_Accepted_FP*454) #Total CFU per gram of final product
    
                                                            #STEP 7 Collection of outputs
    #Collection of Outputs 
    Total_PA_FP.append( Total_Accepted_FP)
    Total_PR_FP.append( Total_Rejected_FP)
    Total_CA_FP.append( Cont_Accepted_FP)
    Total_CR_FP.append( Cont_Rejected_FP)
    LCont_PercRej_FP.append(Cont_PercRej_FP)
    LTotal_CFU_g_FP.append(Total_CFU_G_FP)
    
    #Total_Accepted = sum(df.Weight)
    #Total_Rejected = Field_Weight-Total_Accepted
    
#%%                                                      #STEP 7: Finished Product Packing

    


                                                                    #Model Outputs per scenario. 
                                                                    
#Number and % of CFUs rejected due to actions taken on testing results, the primary benefit                                                                  
                                                                                                                                                                                            
                                                                    
#Baseline No Sampling
if Baseline_Sampling==1:
    Out_NoSampCA = Total_CA_FP #Total CFU Accepted
    Out_NoSampCR = Total_CR_FP #Totqal CFU Rejected
    Out_NoSamp_PercRej = LCont_PercRej_FP #Percentage of CFU Rejected from total
    
    Out_NoSampCont = LTotal_CFU_g_FP #Total CFU/g Accepted
    Out_NoSampProd = Total_PA_FP #Total Weight of product accepted

if PH_Sampling==1:
    #Sampling only in Pre-Harvers
    Out_PHSamp = Total_CA_FP
    Out_PHSampCR = Total_CR_FP #Totqal CFU Rejected
    Out_PHSampCont =  LTotal_CFU_g_FP
    Out_PHSamp_PercRej = LCont_PercRej_PH #Percentage of CFU Rejected from total
    
    Out_PHSampProd = Total_PA_FP

#Sampling only in Harvest
if H_Sampling ==1:
    Out_HSamp = Total_CA_FP
    Out_HSampCR = Total_CR_FP #Totqal CFU Rejected
    Out_HSampCont =  LTotal_CFU_g_FP
    Out_HSamp_PercRej = LCont_PercRej_H #Percentage of CFU Rejected from total
    
    Out_HSampProd = Total_PA_FP

#Sampling in Receiving
if R_Sampling ==1:
    Out_RSamp = Total_CA_FP
    Out_RSampCR = Total_CR_FP #Totqal CFU Rejected
    Out_RSampCont =  LTotal_CFU_g_FP
    Out_RSamp_PercRej = LCont_PercRej_R #Percentage of CFU Rejected from total
    
    Out_RSampProd = Total_PA_FP

#Sampling at Final product
if FP_Sampling==1:
    Out_FPSamp = Total_CA_FP
    Out_FPSampCR = Total_CR_FP #Totqal CFU Rejected
    Out_FPSampCont =  LTotal_CFU_g_FP
    Out_FPSamp_PercRej = LCont_PercRej_FP #Percentage of CFU Rejected from total
    
    Out_FPSampProd = Total_PA_FP

 


#Sampling Scenarios
                                                                        #Pre-Harvest

#Pre-Harvest 4 days
if (PH_Sampling ==1) and (PHS_4d==1):
        #Sampling only in Pre-Harvers
    Out_PH4dSamp = Total_CA_FP
    Out_PH4dSampCR = Total_CR_FP #Totqal CFU Rejected
    Out_PH4dSampCont =  LTotal_CFU_g_FP
    Out_PH4dSamp_PercRej = LCont_PercRej_PH #Percentage of CFU Rejected from total
    Out_PH4dSampProd = Total_PA_FP

#Pre-Harvest 4 hrous
if (PH_Sampling ==1) and (PHS_4h==1):
        #Sampling only in Pre-Harvers
    Out_PH4hSamp = Total_CA_FP
    Out_PH4hSampCR = Total_CR_FP #Totqal CFU Rejected
    Out_PH4hSampCont =  LTotal_CFU_g_FP
    Out_PH4hSamp_PercRej = LCont_PercRej_PH #Percentage of CFU Rejected from total
    Out_PH4hSampProd = Total_PA_FP

#Pre Harvest Intense Sampling
if (PH_Sampling ==1) and (PHS_Int ==1):
        #Sampling only in Pre-Harvers
    Out_PHINSamp = Total_CA_FP
    Out_PHINSampCR = Total_CR_FP #Totqal CFU Rejected
    Out_PHINSampCont =  LTotal_CFU_g_FP
    Out_PHINSamp_PercRej = LCont_PercRej_PH #Percentage of CFU Rejected from total
    Out_PHINSampProd = Total_PA_FP

                                                                            #Harvest

if (H_Sampling ==1) and (HS_Trad==1):
        #Sampling only in Pre-Harvers
    Out_HTrSamp = Total_CA_FP
    Out_HTrSampCR = Total_CR_FP #Totqal CFU Rejected
    Out_HTrSampCont =  LTotal_CFU_g_FP
    Out_HTrSamp_PercRej = LCont_PercRej_PH #Percentage of CFU Rejected from total
    Out_HTrSampProd = Total_PA_FP
    
if (H_Sampling ==1) and (HS_Agg==1):
        #Sampling only in Pre-Harvers
    Out_HAggSamp = Total_CA_FP
    Out_HAggSampCR = Total_CR_FP #Totqal CFU Rejected
    Out_HAggSampCont =  LTotal_CFU_g_FP
    Out_HAggSamp_PercRej = LCont_PercRej_PH #Percentage of CFU Rejected from total
    Out_HAggSampProd = Total_PA_FP

                                                                            #Finished Product

if (FP_Sampling ==1) and (FPS_Trad==1):
        #Sampling only in Pre-Harvers
    Out_FPTrSamp = Total_CA_FP
    Out_FPTrSampCR = Total_CR_FP #Totqal CFU Rejected
    Out_FPTrSampCont =  LTotal_CFU_g_FP
    Out_FPTrSamp_PercRej = LCont_PercRej_PH #Percentage of CFU Rejected from total
    Out_FPTrSampProd = Total_PA_FP
    
if (FP_Sampling ==1) and (FPS_Agg==1):
        #Sampling only in Pre-Harvers
    Out_FPAggSamp = Total_CA_FP
    Out_FPAggSampCR = Total_CR_FP #Totqal CFU Rejected
    Out_FPAggSampCont =  LTotal_CFU_g_FP
    Out_FPAggSamp_PercRej = LCont_PercRej_PH #Percentage of CFU Rejected from total
    Out_FPAggSampProd = Total_PA_FP

#%% 
Samplingtypes = ['Baseline', 'PH4d','PH4h','PHIntense','HTrad','HAgg',"Receiving",'FPTrad',"FPAgg"]
MatchingAreas = ["Baseline","PreHarvest","PreHarvest","PreHarvest","Harvest", "Harvest","Receiving", 'FinalProduct', 'FinalProduct']

DataNames = {"variable" :Samplingtypes,
             "Areas" : MatchingAreas,
    }

DfDataNames = pd.DataFrame(DataNames)


#Boxplot Contamination Accepted CFU
datasampling = {'Baseline':  Out_NoSampCA,
                'PH4d': Out_PH4dSamp,
                'PH4h': Out_PH4hSamp, 
                'PHIntense':Out_PHINSamp,
                'HTrad':Out_HTrSamp,
                'HAgg':Out_HAggSamp,
                "Receiving":Out_RSamp,
                'FPTrad': Out_FPTrSamp,
                "FPAgg": Out_FPAggSamp
          }
dfTotCont = pd.DataFrame(datasampling)

data8 = data=pd.melt(dfTotCont)
data8 =data8.merge(DfDataNames, how = 'right')
sns.boxplot(x= 'variable' , y="value", data=data8 , hue = "Areas", dodge =False)

sns.set(rc={'figure.figsize':(10,8.27)})
#dfTotCont.boxplot()
plt.xlabel("Sampling Strategy")
plt.ylabel("Final Total Contamination Accepted CFU")





df10 = pd.DataFrame({'Group':['A','A','A','B','C','B','B','C','A','C'],\
                  'Apple':np.random.rand(10),'Orange':np.random.rand(10)})
df10 = df[['Group','Apple','Orange']]
df11=pd.melt(df10,id_vars=['Group'],value_vars=['Apple','Orange'],var_name='fruits', dodge =False)





#Boxplot Contamination Accepted CFU/g
dataCont = {'Baseline No Samp': Out_NoSampCont,
        'PreHarvest': Out_PHSampCont, 
          'Harvest':Out_HSampCont,
          'Receiving':Out_RSampCont, 
          'Final':Out_FPSampCont}
    
dfCont = pd.DataFrame(dataCont)

dfCont.boxplot()
plt.xlabel("Sampling at Stage")
plt.ylabel("Final Contamination in Product CFU/g")


#Boxplot Contamination Accepted CFU
dataTotCont = {'Baseline': Out_NoSampCA,
        'PreHarvest': Out_PHSamp, 
          'Harvest':Out_HSamp,
          'Receiving':Out_RSamp, 
          'Final':Out_FPSamp}
dfTotCont = pd.DataFrame(dataTotCont)

dfTotCont.boxplot()
plt.xlabel("Sampling at Stage")
plt.ylabel("Final Total Contamination Accepted CFU")

#Boxplot Contamination Rehjected CFU
dataTotContR = {'Baseline': Out_NoSampCR,
        'PreHarvest': Out_PHSampCR, 
          'Harvest':Out_HSampCR,
          'Receiving':Out_RSampCR, 
          'Final':Out_FPSampCR}
dfTotContR = pd.DataFrame(dataTotContR)

dfTotContR.boxplot()
plt.xlabel("Sampling at Stage")
plt.ylabel("Final Total Contamination Rejected CFU")


#Boxplot Total Product Accepted
dataProd = {'Baseline': Out_NoSampProd,
        'PreHarvest': Out_PHSampProd, 
          'Harvest':Out_HSampProd,
          'Receiving':Out_RSampProd, 
          'Final':Out_FPSampProd}
dfProd = pd.DataFrame(dataProd)

dfProd.boxplot()
plt.xlabel("Sampling at Stage")
plt.ylabel("Total Product Accepted")



#Percentage of total contaminated Rejected

dataContPercRej = {'PreHarvest': Out_PHSamp_PercRej, 
          'Harvest':Out_HSamp_PercRej,
          'Receiving':Out_RSamp_PercRej, 
          'Final':Out_FPSamp_PercRej}
    
dataContPercRej = pd.DataFrame(dataContPercRej)


sns.boxplot(x="variable", y="value", data=pd.melt(dataContPercRej))
plt.xlabel("Sampling at Stage Only")
plt.ylabel("Percentage of Contamination Rejected CFU")



