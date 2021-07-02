# -*- coding: utf-8 -*-
"""
Created on Fri May 28 09:42:31 2021

@author: Gustavo Reyes
"""

#%%

import sys
sys.path
sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model')
#sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility\Model')

########################################Paths#################################################
#os.chdir('C:\\Users\Gustavo Reyes\Box\CPS Project- Farm to Facility\Python Model Files')
#os.chdir("C:\\Users\\reyes\\Box Sync\\CPS Project- Farm to Facility\\Python Model Files")
#os.chdir('C:\\Users\Gustavo Reyes')
#print(os.getcwd())
#%% 
#Libraries, Modules
import pandas as pd 
import numpy as np
import itertools
import scipy.stats as stats
import math
import os
import random
import seaborn as sns
from matplotlib import pyplot as plt
import Funz
import ContScen
import Listz 
import OutFunz
#from itertools import cycle


#%% 
Progression_DFS=[]

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
Background_C=1
Point_Source_C=0
Systematic_C=0

#Harvester Contamination
Crew_C = 0
Harvester_C = 0

#Processing equipment
PE_C = 0

Pack_C= 0



#Sampling Options

#Pre-Harvest
    #Pre-Harvest sampling must be on
PHS_4d= 1 #Scenario 1
PHS_4h = 0#Scenario 2
PHS_Int = 0 #Scenario 3

#Harvest: 
    #HArvest Sampling must be one
HS_Trad = 1 #Scenario 5
HS_Agg = 0 #Scenario 6

#Final Product Sampling
    #Final Product sampling must be on.
FPS_Trad =1 #Scenario 7
FPS_Agg = 0  #Scenario 8

#%%

List_Initial_CFU = []
                                                                    #List to collect outputs
#Total CFU Before_PH sampling 
List_BPHS_CFU=[]

#After_PH_sampling
Total_PA_PH = [] #Product Accepted
Total_PR_PH = [] #Product Rejected
Total_CR_PH = [] #Contamination Rejected
Total_CA_PH = [] #Contamination Accepted

#Before_H sampling
List_BHS_CFU=[]

#After H Sampling
Total_PR_H = []
Total_PA_H = []
Total_CR_H = []
Total_CA_H = []


#Before R Sampling
List_BRS_CFU=[]

#After R Sampling
Total_PR_R = []
Total_PA_R = []
Total_CR_R = []
Total_CA_R = []

#Between Washing and Value Addition
List_BtWVA_CFU =[]

List_AVA_CFU=[]

#Before FP Sampling
List_BFPS_CFU=[]

#After FP Sampling
Total_PR_FP = []
Total_PA_FP = []
Total_CR_FP = []
Total_CA_FP = []

List_TotalCFUg_FP = [] #Total

List_Cont_PercRej_PH = []
List_Cont_PercRej_H = []
List_Cont_PercRej_R = [] 
List_Cont_PercRej_FP=[]




#%%

for i in range(100):
       
                                                                    #Inputs for the Model, Initial Inputs
                                                                  
    # 0 Initial Inputs for Field Setup and Challenges
    
    Field_Weight= 100000 #total lb in field
    slot_weight = 10000
    Partition_Weight = 1000
    
    slot_number = int(Field_Weight/slot_weight)
    Partition_Units = int(Field_Weight/Partition_Weight)
    Cluster_Unit_weight = Field_Weight/Partition_Units
    
    #Challenge Related Information
    if Background_C ==1:
        Hazard_lvl = 50000  #CFU # background contamination
        Cluster_Size = 100000 #lb
        No_Cont_Clusters = 1
    
        
    if Point_Source_C ==1:
        Hazard_lvl = 50000  #CFU # background contamination
        Cluster_Size = 1000 #lb
        No_Cont_Clusters = 4
        
    if Systematic_C ==1: 
        Hazard_lvl = 50000  #CFU # background contamination
        Cluster_Size = 10000 #lb
        No_Cont_Clusters = 1

     

    if Crew_C == 1: 
        Hazard_lvl = 50000  #CFU # background contamination
        Cluster_Size = 5000 #lb
        No_Cont_Clusters = 4

    
    if Harvester_C==1:
        Hazard_lvl = 50000  #CFU # background contamination
        Cluster_Size = 50000 #lb
        No_Cont_Clusters = 1
        
    if PE_C == 1:
        Hazard_lvl = 50000  #CFU # background contamination
        Lines_Cont = 1
        
    if Pack_C == 1:
        Hazard_lvl = 50000  #CFU # background contamination
        Lines_ContPack = 1        
        
        
    
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
        Time_PHS_H = 0.166
    elif PHS_4d ==1:
        Time_PHS_H = 4
    else:
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
    Partition_Weight_FP = 10
    N_Lots_FP = 2
    sample_size_FP = 300 #g #Sample Size in grams
    n_samples_FP = 1

    

                                                            #Step 0: DF Creation and Setup based on scenarios. 
    #Creation of the Data Frame to Track: 
    data = {'Lot': 1,
            'Sublot':0,
            'PartitionID': list(range(1,Partition_Units+1)),
            'CFU':0,
            'Accept': True,
            'Weight': Field_Weight/Partition_Units}
    
    Sublot_Pattern = [i for i in range(1, slot_number+1) for _ in range(int(slot_number))]
    
    df = pd.DataFrame(data)
    df.Sublot = Sublot_Pattern
    df.index = range(1,Partition_Units+1)
    
    #Adding Contamination depending on challenge Background
    if Background_C == 1:
        df = ContScen.F_Background_C(df=df, Hazard_lvl = Hazard_lvl, 
                                     Partition_Units= Partition_Units)
        
    #Adding Contamination depending on challenge Point_Source
    if Point_Source_C == 1:
        df=ContScen.F_Point_Source_C(df=df, Hazard_lvl=Hazard_lvl,
                                     No_Cont_Clusters =No_Cont_Clusters, 
                                     Cluster_Size = Cluster_Size, 
                                     Partition_Weight = Partition_Weight)

        
    #Adding Contamination depending on challenge Systematic Sampling
    if Systematic_C == 1:
        df = ContScen.F_systematic_C(df=df, Hazard_lvl= Hazard_lvl,
                                     No_Cont_Clusters = No_Cont_Clusters,
                                     Cluster_Size= Cluster_Size,
                                     Partition_Weight = Partition_Weight)
        
    #Initial Contamination     
    Initial_CFU= sum(df.CFU)
    List_Initial_CFU.append(Initial_CFU)
    

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
        
    BPHS_CFU = sum(df.CFU) #Contamination before sampling
    List_BPHS_CFU.append(BPHS_CFU) #List of contamination before sampling
    
    #Filtering out the Rejected lots, Pre-Harvest
    if PHS_Int ==1:
        df = df[~df['Lot'].isin(Rej_Lots_PH)]   
    else: 
        df = df[~df['Sublot'].isin(Rej_Lots_PH)]
                       
    
    #Summary of Pre-Harvest Sampling
    Total_Accepted_PH = sum(df.Weight) #Lb
    Total_Rejected_PH = Field_Weight-Total_Accepted_PH #Lb
    Cont_Accepted_PH = sum(df.CFU) # Total CFU
    Cont_Rejected_PH = BPHS_CFU-Cont_Accepted_PH #Total CFU
    if Cont_Accepted_PH == 0:
        Cont_PercRej_PH = 1
    else:
        Cont_PercRej_PH = Cont_Rejected_PH/(Cont_Accepted_PH+Cont_Rejected_PH) #Percentage Rejected by H sampling
    
    
    #Outputs for Iterations
    Total_PA_PH.append(Total_Accepted_PH)
    Total_PR_PH.append(Total_Rejected_PH)
    Total_CA_PH.append(Cont_Accepted_PH)
    Total_CR_PH.append(Cont_Rejected_PH)
    List_Cont_PercRej_PH.append(Cont_PercRej_PH)
    

                                                                 #STEP 2: HARVEST
    
    #Pre-Harvest Sampling - Harvest Sampling Die off
    Time_Agg = Time_Agg + Time_PHS_H #Cummulative time so far in the process.
    Die_off_B = Funz.F_Simple_DieOff(Time_Agg)
    Die_Off_PHS_HS= Die_off_B-Die_Off_CE_PHS#Funz.F_DieOff_PHS_HS(Time_PHS_H, Time_Agg, Break_Point, Dieoff1, Dieoff2)
    print(Die_Off_PHS_HS)
    df['CFU'] = df['CFU']*(10**Die_Off_PHS_HS) #Updating Contmination to Show Total DieOff
    
    #Adding Contamination depending on challenge Systematic Sampling
    if Crew_C == 1:
        df = ContScen.F_Crew_C(df =df, Hazard_lvl =Hazard_lvl, 
                               No_Cont_Clusters = No_Cont_Clusters,
                               Cluster_Size =Cluster_Size, 
                               Partition_Weight = Partition_Weight)

    if Harvester_C == 1:
        df = ContScen.F_Harvester_C(df =df, Hazard_lvl =Hazard_lvl, 
                                    No_Cont_Clusters = No_Cont_Clusters, 
                                    Cluster_Size =Cluster_Size, 
                                    Partition_Weight = Partition_Weight)
    
    
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
        
    #Before pre harvest sampling
    BHS_CFU = sum(df.CFU) #Contamination before sampling
    List_BHS_CFU.append(BHS_CFU) #List of contaminations before sampling
    
    #Filtering out the Rejected lots, Pre-Harvest
    df = df[~df['Sublot'].isin(Rej_Lots_H)]
        
    
    #Summary of Harvest Sampling
    Total_Accepted_H = sum(df.Weight) #Total Accepted at HArvest
    Total_Rejected_H = Field_Weight-Total_Accepted_H
    Cont_Accepted_H = sum(df.CFU) #CFU
    Cont_Rejected_H =  BHS_CFU-Cont_Accepted_H #CFU
    if Cont_Accepted_PH == 0:
        Cont_PercRej_H = "NA"
    else:
        Cont_PercRej_H = Cont_Rejected_H/(Cont_Accepted_H+Cont_Rejected_H) #Percentage Rejected by H sampling
    
    #Outputs for Iterations
    Total_PA_H.append(Total_Accepted_H)
    Total_PR_H.append(Total_Rejected_H)
    Total_CA_H.append(Cont_Accepted_H)
    Total_CR_H.append(Cont_Rejected_H)
    List_Cont_PercRej_H.append(Cont_PercRej_H)
    
    
                                                               #STEP 3: RECEIVING
                                                               
    #Harvest Sampling - Receiving Harvest Sampling Die off
    Die_Off_HS_RS= Die_Off_HS_RS*Time_H_RS
    df['CFU'] = df['CFU']*(10**Die_Off_HS_RS) #Updating Contmination to Show Total DieOff
        
                                             
                                                               
    #Paletization
    
    Partitions_Per_Pallet =  int(Pallet_Weight/Partition_Weight)
    Pallet_Field = int(Field_Weight/Pallet_Weight)
    Pallet_Pattern = [i for i in range(1, Pallet_Field+1) for _ in range(int(Partitions_Per_Pallet))]
    Crop_No = len(df.index)
    Pallet_Pattern=Pallet_Pattern[:Crop_No]
    df['PalletNo'] = Pallet_Pattern
    df = df[['Lot', 'Sublot','PalletNo','PartitionID','CFU','Accept', 'Weight']]
    No_Pallets = df.PalletNo.nunique()
    
    


    Time_Agg = Time_Agg + Time_H_RS #Cummulative time so far in the process. 
    
    BRS_CFU = sum(df.CFU)
    List_BRS_CFU.append(BRS_CFU) #Contamination before receiving sampling
    
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
    
    
    #Outputs for of Receiving Sampling
    Total_Accepted_R = sum(df.Weight)
    Total_Rejected_R = Field_Weight-Total_Accepted_R
    Cont_Accepted_R = sum(df.CFU) #CFU
    Cont_Rejected_R = BRS_CFU-Cont_Accepted_R #CFU
    if Cont_Accepted_H == 0:
        Cont_PercRej_R = "NA"
    else:
        Cont_PercRej_R = Cont_Rejected_R/(Cont_Accepted_R+Cont_Rejected_R) #Percentage Rejected by H sampling
    
    Total_PA_R.append(Total_Accepted_R)
    Total_PR_R.append(Total_Rejected_R)
    Total_CA_R.append(Cont_Accepted_R)
    Total_CR_R.append(Cont_Rejected_R)
    List_Cont_PercRej_R.append(Cont_PercRej_R)
    
     
                                                                    #STEP 4: WASHING Reduction
    
    #Wash process reduction
    df=Funz.F_Washing(df, LogRedWash)
    
    #gathering contamination between washing and Value Addition
    BtWVA_CFU = sum(df.CFU)
    List_BtWVA_CFU.append (BtWVA_CFU)
    
        
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
    N_Lines = list(range(1,Processing_Lines+1))
    L_ProLine =list(itertools.chain(*(itertools.repeat(elem, n) for elem, n in zip(N_Lines, N_Divs))))
    df2["ProLine"] = L_ProLine
    
    #Dividing the pallets dataframe into different processing lines.  
    gb = df2.groupby('ProLine')#Creating Listby procesing line
    gb2 =[gb.get_group(x) for x in gb.groups] #Creating list of separate dataframe by processing lines

    #Value Addition Steps
    #Cross-Contamination Processing by batch, Assuming Every Pallet is a 4000k lb bath
    for j in gb2:
        ContS=0
        for i, row in j.iterrows():
            ContP = j.CFU[i] #Contamination product
            TotTr_P_S= ContP*(Tr_P_S/100) #Transfer from Product to Surfaces
            TotTr_S_P = ContS*(Tr_S_P/100) #Trasnfer from Surfaves to product
            ContPNew = ContP-TotTr_P_S+TotTr_S_P #New Contmination on Product
            ContS=ContS+TotTr_P_S-TotTr_S_P #Remiining Contamination in Surface for upcoming batches
            j.CFU[i]=ContPNew #Updating the Contamination in the Data Frame
            
    #Adding Contamination from Scenario to each lot
    if PE_C ==1:
        gb2 = ContScen.F_PEC_C(gb2=gb2,
                               Hazard_lvl = Hazard_lvl, 
                               Processing_Lines = Processing_Lines, 
                               Lines_Cont = Lines_Cont)
        
    
    #Joining Data Frames into one again, with contamination from lines. 
    df2=(pd.concat(gb2))
    
    AVA_CFU= sum(df2.CFU)
    List_AVA_CFU.append(AVA_CFU)
        
    df2['Lot'] =1#Updating the CFU/g column
        
    #Environmental Monitoring Program
    
    
    
                                               
                                                          #STEP 6: Finished Product Mixing and Sampling
    #Mixing products into one batch
    
    N_Partitions = int(Pallet_Weight/Partition_Weight_FP)
    
    df2 = Funz.F_Partitioning(DF=df2, NPartitions= N_Partitions)
    if N_Lots_FP==2:
        df2 =Funz.F_Lots_FP(df=df2, Nolots = 2)
    
    
    
    BFPS_CFU = sum(df2.CFU) #Total CFU before FP Sampling
    List_BFPS_CFU.append(BFPS_CFU) #Adding it to a List
    #df= Funz.F_Packaging(DF=df, Boxes_Pallet=Boxes_Pallet)
    
    #Dividing the pallets dataframe into different processing lines.  
    gbFP = df2.groupby('ProLine')#Creating Listby procesing line
    gbFP2 =[gbFP.get_group(x) for x in gbFP.groups] #Creating list of separate dataframe by processing lines
    
    if Pack_C ==1:
        gbFP2 = ContScen.F_PEC_C(gb2=gbFP2,
                        Hazard_lvl = Hazard_lvl, 
                        Processing_Lines = Processing_Lines, 
                        Lines_Cont = Lines_ContPack)
    
    df2=(pd.concat(gbFP2))
    
    #Sampling Step
    if FP_Sampling == 1:
        if FPS_Trad ==1:
            Rej_Lots_FP=Funz.F_SamplingFProd(df=df2, Test_Unit = 'PackNo', N_SampPacks = 60, Grab_Weight = 5 )
            print(Rej_Lots_FP)
        elif FPS_Agg ==1:
            Rej_Lots_H = Funz.F_Sampling(df =df2,Test_Unit ="Sublot", 
                                           NSamp_Unit = 10, 
                                           Samp_Size =sample_size_FP, 
                                           Clust_Weight =Partition_Weight_FP, 
                                           Limit =0, NoGrab =60 )
    else :
        Rej_Lots_FP = []
    

    #Filtering out the Rejected lots, Final product
    if FP_Sampling == 1:
        if FPS_Trad==1:
            df2 = df2[~df2['Lot'].isin(Rej_Lots_H)]
        elif FPS_Agg ==1:
            df2 = df2[~df2['Sublot'].isin(Rej_Lots_H)]
    
    Total_Accepted_FP = sum(df2.Weight) #Total Product Accepted
    Total_Rejected_FP = Field_Weight-Total_Accepted_FP #Total Product Rejected
    Cont_Accepted_FP = sum(df2.CFU) #CFU Accepted
    Cont_Rejected_FP =  BFPS_CFU-Cont_Accepted_FP #CFU Rejected from PH Sampling
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
    Total_PA_FP.append(Total_Accepted_FP)
    Total_PR_FP.append(Total_Rejected_FP)
    Total_CA_FP.append(Cont_Accepted_FP)
    Total_CR_FP.append(Cont_Rejected_FP)
    List_Cont_PercRej_FP.append(Cont_PercRej_FP)
    List_TotalCFUg_FP.append(Total_CFU_G_FP)
    
    #Total_Accepted = sum(df.Weight)
    #Total_Rejected = Field_Weight-Total_Accepted
    
#%%     

#Creation of Ouputs DF

#Progression Data
data_contprog = {"Initial":List_Initial_CFU,
                 "Before PHS": List_BPHS_CFU,
                 "After PHS": Total_CA_PH,
                 "Before HS":List_BHS_CFU,
                 "After HS": Total_CA_H,
                 "Before RS": List_BRS_CFU,
                 "After RS": Total_CA_R,
                 "Between W-VA": List_BtWVA_CFU,
                 "After VA": List_AVA_CFU,
                 "Before FPS": List_BFPS_CFU,
                 "FinalCont": Total_CA_FP
                 }

df_contprog = pd.DataFrame(data_contprog)


#Main Output Data
data_outputs={"Total_CFU_A":Total_CA_FP,
               "Total_CFU_Rej": Total_CR_FP,
               "Total_CFUg_A": List_TotalCFUg_FP,
              "Total_Weight_A":Total_PA_FP 
    }

df_outputs = pd.DataFrame(data_outputs)


                                                
                                                                    #Model Outputs per scenario. 
                                                                    
#Number and % of CFUs rejected due to actions taken on testing results, the primary benefit
                                                              
#Baseline No Sampling
if Baseline_Sampling==1:
    
    Out_BLSamp_PercRej = List_Cont_PercRej_FP #Percentage of CFU Rejected from total
    
    #Main Outputs, contamination and weight.
    BL_df_outputs = df_outputs
    BL_df_outputs2= OutFunz.F_Melting(df= BL_df_outputs, Scenario="Baseline")

    #Contamination Progression
    BL_df_contprog = df_contprog
    BL_df_contprog2= OutFunz.F_Melting(df= BL_df_contprog, Scenario="Baseline")
    Progression_DFS.append(BL_df_contprog2)

if PH_Sampling==1:
    #Sampling only in Pre-Harvers
    Out_PHSamp_PercRej = List_Cont_PercRej_PH #Percentage of CFU Rejected from total

    #Main Outputs, contamination and weight.
    PHS_df_outputs = df_outputs
    PHS_df_outputs2= OutFunz.F_Melting(df= PHS_df_outputs, Scenario="PHS")
    
    #Contamination Progression
    PHS_df_contprog = df_contprog
    PHS_df_contprog2= OutFunz.F_Melting(df= PHS_df_contprog, Scenario="PHS")
    Progression_DFS.append(PHS_df_contprog2)

#Sampling only in Harvest
if H_Sampling ==1:

    Out_HSamp_PercRej = List_Cont_PercRej_H #Percentage of CFU Rejected from total
    
    #Main Outputs, contamination and weight.
    HS_df_outputs = df_outputs
    HS_df_outputs2= OutFunz.F_Melting(df= HS_df_outputs, Scenario="HS")

    #Contamination Progression
    HS_df_contprog = df_contprog
    HS_df_contprog2= OutFunz.F_Melting(df= HS_df_contprog, Scenario="HS")
    Progression_DFS.append(HS_df_contprog2)

#Sampling in Receiving
if R_Sampling ==1:
    Out_RSamp_PercRej = List_Cont_PercRej_R #Percentage of CFU Rejected from total
    
    #Main Outputs, contamination and weight.
    RS_df_outputs = df_outputs
    RS_df_outputs2= OutFunz.F_Melting(df= RS_df_outputs, Scenario="RS")
    
    
    #Contamination Progression
    RS_df_contprog = df_contprog
    RS_df_contprog2= OutFunz.F_Melting(df= RS_df_contprog, Scenario="RS")
    Progression_DFS.append(RS_df_contprog2)

#Sampling at Final product
if FP_Sampling==1:
    
    Out_FPSamp_PercRej = List_Cont_PercRej_FP #Percentage of CFU Rejected from total
    
    #Main Outputs, contamination and weight.
    FP_df_outputs = df_outputs
    FP_df_outputs2= OutFunz.F_Melting(df= RS_df_outputs, Scenario="FP")
      
    
    #Contamination Progression
    FPS_df_contprog = df_contprog
    FPS_df_contprog2= OutFunz.F_Melting(df= FPS_df_contprog, Scenario="FPS")
    Progression_DFS.append(FPS_df_contprog2)



#Sampling Scenarios
                                                                        #Pre-Harvest

#Pre-Harvest 4 days
if (PH_Sampling ==1) and (PHS_4d==1):
    
    #Sampling only in Pre-Harvers
    Out_PH4d_PercRej = List_Cont_PercRej_PH #Percentage of CFU Rejected from total
    
    #Main Outputs, contamination and weight.
    PH4d_df_outputs = df_outputs
    PH4d_df_outputs2= OutFunz.F_Melting(df= PH4d_df_outputs, Scenario="PH4d")


#Pre-Harvest 4 hrous
if (PH_Sampling ==1) and (PHS_4h==1):
    #Sampling only in Pre-Harvers
    Out_PH4h_PercRej = List_Cont_PercRej_PH #Percentage of CFU Rejected from total
    
    #Main Outputs, contamination and weight.
    PH4h_df_outputs = df_outputs
    PH4h_df_outputs2= OutFunz.F_Melting(df= PH4h_df_outputs, Scenario="PH4h")

#Pre Harvest Intense Sampling
if (PH_Sampling ==1) and (PHS_Int ==1):
    
    #Sampling only in Pre-Harvers
    Out_PHIN_PercRej = List_Cont_PercRej_PH #Percentage of CFU Rejected from total
    
    #Main Outputs, contamination and weight.
    PHIN_df_outputs = df_outputs
    PHIN_df_outputs2= OutFunz.F_Melting(df= PHIN_df_outputs, Scenario="PHIN")

                                                                            #Harvest

if (H_Sampling ==1) and (HS_Trad==1):
        #Sampling only in Pre-Harvers
    Out_HTr_PercRej = List_Cont_PercRej_PH #Percentage of CFU Rejected from total
    
    #Main Outputs, contamination and weight.
    HTr_df_outputs = df_outputs
    HTr_df_outputs2= OutFunz.F_Melting(df= HTr_df_outputs, Scenario="HTr")

    
if (H_Sampling ==1) and (HS_Agg==1):
    #Sampling only in Pre-Harvers
    Out_HAgg_PercRej = List_Cont_PercRej_PH #Percentage of CFU Rejected from total
  
    #Main Outputs, contamination and weight.
    HAgg_df_outputs = df_outputs
    HAgg_df_outputs2= OutFunz.F_Melting(df= HAgg_df_outputs, Scenario="HAgg")

                                                                            #Finished Product

if (FP_Sampling ==1) and (FPS_Trad==1):
    
    #Sampling only in Pre-Harvers
    Out_FPTr_PercRej = List_Cont_PercRej_PH #Percentage of CFU Rejected from total
    
    #Main Outputs, contamination and weight.
    FPTr_df_outputs = df_outputs
    FPTr_df_outputs2= OutFunz.F_Melting(df= FPTr_df_outputs, Scenario="FPTr")

    
if (FP_Sampling ==1) and (FPS_Agg==1):
    #Sampling only in Pre-Harvers
    Out_FPAgg_PercRej = List_Cont_PercRej_PH #Percentage of CFU Rejected from total

    #Main Outputs, contamination and weight.
    FPAgg_df_outputs = df_outputs
    FPAgg_df_outputs2= OutFunz.F_Melting(df= FPAgg_df_outputs, Scenario="FPAgg")


#%% 
#Contamination Progression
ProgMelted = pd.concat(Progression_DFS)

Progplot =sns.catplot(x="variable", y="value", data=ProgMelted ,kind="bar",capsize=.2, hue = "Scenario", height=4, aspect=3 )
plt.xlabel("Process Step")
plt.ylabel("CFU in System")


#Boxplot Contamination Accepted CFU
data_scenarios = {'Baseline':  BL_df_outputs["Total_CFU_A"],
                'PHS':  PHS_df_outputs["Total_CFU_A"],
                'HS':  HS_df_outputs["Total_CFU_A"],
                'RS':  RS_df_outputs["Total_CFU_A"],
                'FP':  FP_df_outputs["Total_CFU_A"],
          }
df_data_scenarios = pd.DataFrame(data_scenarios)

df_data_scenarios_melted = pd.melt(df_data_scenarios)


Scenariosplot =sns.catplot(x="variable", y="value", data=df_data_scenarios_melted ,kind="bar",capsize=.2,  height=4, aspect=2 )
plt.xlabel("Process Step")
plt.ylabel("CFU in System")



#Boxplot Contamination Accepted CFU
datasampling = {'Baseline':  BL_df_outputs["Total_CFU_A"],
                'PH4d': Out_PH4d,
                'PH4h': Out_PH4h, 
                'PHIntense':Out_PHIN,
                'HTrad':Out_HTr,
                'HAgg':Out_HAgg,
                "Receiving":Out_RSamp,
                'FPTrad': Out_FPTr,
                "FPAgg": Out_FPAgg
          }




Samplingtypes = ['Baseline', 'PH4d','PH4h','PHIntense','HTrad','HAgg',"Receiving",'FPTrad',"FPAgg"]
MatchingAreas = ["Baseline","PreHarvest","PreHarvest","PreHarvest","Harvest", "Harvest","Receiving", 'FinalProduct', 'FinalProduct']

DataNames = {"variable" :Samplingtypes,
             "Areas" : MatchingAreas,
    }

DfDataNames = pd.DataFrame(DataNames)



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
dataCont = {'Baseline No Samp': Out_BLSampCont,
        'PreHarvest': Out_PHSampCont, 
          'Harvest':Out_HSampCont,
          'Receiving':Out_RSampCont, 
          'Final':Out_FPSampCont}
    
dfCont = pd.DataFrame(dataCont)

dfCont.boxplot()
plt.xlabel("Sampling at Stage")
plt.ylabel("Final Contamination in Product CFU/g")


#Boxplot Contamination Accepted CFU
dataTotCont = {'Baseline': Out_BLSampCA,
        'PreHarvest': Out_PHSamp, 
          'Harvest':Out_HSamp,
          'Receiving':Out_RSamp, 
          'Final':Out_FPSamp}
dfTotCont = pd.DataFrame(dataTotCont)

dfTotCont.boxplot()
plt.xlabel("Sampling at Stage")
plt.ylabel("Final Total Contamination Accepted CFU")

#Boxplot Contamination Rehjected CFU
dataTotContR = {'Baseline': Out_BLSampCR,
        'PreHarvest': Out_PHSampCR, 
          'Harvest':Out_HSampCR,
          'Receiving':Out_RSampCR, 
          'Final':Out_FPSampCR}
dfTotContR = pd.DataFrame(dataTotContR)

dfTotContR.boxplot()
plt.xlabel("Sampling at Stage")
plt.ylabel("Final Total Contamination Rejected CFU")


#Boxplot Total Product Accepted
dataProd = {'Baseline': Out_BLSampProd,
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



