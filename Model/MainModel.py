# -*- coding: utf-8 -*-
"""
Created on Mon May 23 13:22:12 2022

@author: gareyes3
"""

#%%
import sys
sys.path
sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility_L_T\Model')
sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility_L_T\Model')

#%%
import numpy as np
import pandas as pd
import random 
import math
from numpy.random import Generator, PCG64
rng = Generator(PCG64())
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import reload 

import time
#Own Libraries
import Funz_T
import Inputz_T
import Scen_T
#import DepInputz
import T_Inputz
import Dictionariez_T


#%%

#%%

def Main_Loop(random_seed =1000):
    #Model
    #Creation of collection Data Frames.
    DC_Cont_Day = Dictionariez_T.Output_DF_Creation(Column_Names =Dictionariez_T.Col_Days, Niterations = Scen_T.Iteration_Number)
    DC_Prev_Day = Dictionariez_T.Output_DF_Creation(Column_Names =Dictionariez_T.Col_Days, Niterations = Scen_T.Iteration_Number)
    DC_Cont_Processing = Dictionariez_T.Output_DF_Creation(Column_Names =Dictionariez_T.Proc_Steps, Niterations = Scen_T.Iteration_Number)
    DC_Cont_Processing_Prev = Dictionariez_T.Output_DF_Creation(Column_Names =Dictionariez_T.Proc_Steps, Niterations = Scen_T.Iteration_Number)
    DC_Exp = Dictionariez_T.Output_DF_Creation(Column_Names =Dictionariez_T.Columns_Final_Outs, Niterations = Scen_T.Iteration_Number)

    #DC_Cont_Day_Pick1 = Dictionariez_T.Output_DF_Creation(Column_Names =Dictionariez_T.Col_Days, Niterations = Scen_T.Iteration_Number)
    #DC_Cont_Day_Pick2 = Dictionariez_T.Output_DF_Creation(Column_Names =Dictionariez_T.Col_Days, Niterations = Scen_T.Iteration_Number)
    #DC_Cont_Day_Pick3 = Dictionariez_T.Output_DF_Creation(Column_Names =Dictionariez_T.Col_Days, Niterations = Scen_T.Iteration_Number)

    Cont_Day_List = []
    #Simulating Days
    #reload(Inputz_T)
    
    #Contaminated Bin
    for k in range(0,Scen_T.Iteration_Number):
        print(k, "Iteration")
        random.seed(random_seed+k)
        np.random.seed(random_seed+k)
        reload(Inputz_T)
        print(Scen_T.Total_Hazard)
        
        #start_df = time.time()
        Field_df=pd.DataFrame({"Tomato_ID": Inputz_T.Individual_Tomatoes,
                               "Plant_ID": Inputz_T.Individual_Plants[0:Inputz_T.Individual_Tomatoes.size],
                               "Pick_ID": Inputz_T.Pick_Random[0:Inputz_T.Individual_Tomatoes.size],
                               "Weight": Inputz_T.Tomato_weight,
                               "Harvester" : 0,
                               "Bucket":0,
                               "Bin": 0,
                               "Case_PH": 0,
                               "CFU": 0,
                               "CFU_BRej":"",
                               "Location": 1,
                               'PositiveSamples':0,
                               "Rej_Acc" :"Acc"
                          })
        
        #Field_df.PositiveSamples = [list() for x in range(len(Field_df.index))]
        #print(time.time() - start_df, "df Creation")
        
        #Reseting to current pick
        Current_Pick = 1
        Current_Samp = 1
        
        ###Contamination Event Selection
        if Scen_T.Chosen_cont_day == 0:
            Cont_Day  = random.sample(list(Inputz_T.Days),1)
            print(Cont_Day[0])
        if Scen_T.Chosen_cont_day == 1:
            Cont_Day  = [Scen_T.Contamination_Day ]
            print(Cont_Day)
            
        Cont_Day_List.append(Cont_Day[0])    
    
        #Choosing the harvester that is contaminated
        Contaminated_Harvesters_Each = random.sample(list(range(1,Inputz_T.Total_Harvesters+1)),3)
        #Days_B_Pick1 = list(range(1,Inputz_T.Days_Between_Picks+1))
        #Days_B_Pick2 = list(range(Inputz_T.Days_Between_Picks+1,2*Inputz_T.Days_Between_Picks+1))
        #Days_B_Pick3 = list(range(2*Inputz_T.Days_Between_Picks+1,3*Inputz_T.Days_Between_Picks+1))
        
        #Cont_Event_1_Days = [random.sample(Days_B_Pick1,1)[0], random.sample(Days_B_Pick2,1)[0], random.sample(Days_B_Pick3,1)[0]]
        #Cont_Event_2_Days = [random.sample(Days_B_Pick1,1)[0], random.sample(Days_B_Pick2,1)[0], random.sample(Days_B_Pick3,1)[0]]
        
        
        
        
        for i in Inputz_T.Days:
            
            
            #100% widespread contamination
            if (Scen_T.Cont_Scenario == 1 and i in Cont_Day):
                #This function contaminated the field uniformly. 100% of the field cont. 
                Field_df = Funz_T.field_cont_percetage2(df = Field_df, 
                                                percent_cont = 100,
                                                Hazard_lvl = Scen_T.Total_Hazard, 
                                                No_Cont_Clusters = 1)

            
            #10% cluster contamination
            if (Scen_T.Cont_Scenario == 2 and i in Cont_Day): 
                #Contaminated field with 0.1% contamination, simulated bird droping. 
                Field_df = Funz_T.field_cont_percetage2(df = Field_df, 
                                                percent_cont = 10,
                                                Hazard_lvl =Scen_T.Total_Hazard, 
                                                No_Cont_Clusters = 1)
            
            #1% clustercontamination
            if (Scen_T.Cont_Scenario == 3 and i in Cont_Day): 
                #print("brid")
                #Contaminated field with 0.1% contamination, simulated bird droping. 
                Field_df = Funz_T.field_cont_percetage2(df = Field_df, 
                                                percent_cont = 1,
                                                Hazard_lvl = Scen_T.Total_Hazard, 
                                                No_Cont_Clusters = 1)
            #0.1% cluster contamination   
            if (Scen_T.Cont_Scenario == 4 and i in Cont_Day): 
                #Contaminated field with 0.1% contamination, simulated bird droping. 
                Field_df = Funz_T.field_cont_percetage2(df = Field_df, 
                                                percent_cont = 0.1,
                                                Hazard_lvl = Scen_T.Total_Hazard, 
                                                No_Cont_Clusters = 1)
            
            #Conduncting preharvest sampling.
            
            if Scen_T.Samp_Plan == 1: #plan 1 is preharvest
                #Collection of Outputs
                if i in Inputz_T.PHS_Days:

                    #collecting intermediate outputs
                    DC_Exp= Dictionariez_T.Output_Collection_Sampling(df = Field_df, 
                                                      outputDF=DC_Exp,
                                                      i = k, 
                                                      SampType = "PHS", 
                                                      PickNo = Current_Samp,
                                                      Bef_Aft = "Bef")

                    DC_Exp = Dictionariez_T.Output_Collection_Sampling_Weight_R(df = Field_df, 
                                                      outputDF=DC_Exp,
                                                      i = k, 
                                                      SampType = "PHS", 
                                                      PickNo = Current_Samp,
                                                      Bef_Aft = "Bef")

                    #whole tomatoes no mash
                    if Scen_T.Samp_Method == 1:

                        Field_df = Funz_T.F_Sampling_T (df= Field_df, 
                                                  Pick_No = Current_Pick, 
                                                  Location = 1, #Location is in field
                                                  NSamp_Unit = 1, 
                                                  NoGrab = Scen_T.Tomatoes_per_sample) 
                    #Method for the tomato Mash.
                    elif  Scen_T.Samp_Method == 2:
                        Field_df =  Funz_T.F_Sampling_T_Mash (df= Field_df, 
                                                              Pick_No= Current_Pick, 
                                                              Location =1,
                                                              NSamp_Unit =1, 
                                                              NoGrab= Scen_T.Tomatoes_per_sample, 
                                                              Subsample_Mass=25,
                                                              N_replicates = Scen_T.N_Replicates)
                    
                    #Rejection rules, reject current pick plus any upcoming picks

                    Field_df=Funz_T.F_Rejection_Rule_T (df = Field_df, 
                                        Pick_No = Current_Samp, 
                                        Av_Picks= list(range(Current_Pick,Inputz_T.N_Pick+1)), 
                                        Test_Unit = "Pick_ID", 
                                        limit = 0)

                    #Collecting sampling outputs
                    DC_Exp= Dictionariez_T.Output_Collection_Sampling(df = Field_df, 
                                      outputDF=DC_Exp,
                                      i = k, 
                                      SampType = "PHS", 
                                      PickNo = Current_Samp,
                                      Bef_Aft = "Aft")
                    
                    #Collecting total cells outputs
                    DC_Exp = Dictionariez_T.Output_Collection_Sampling_Weight_R(df = Field_df, 
                                                      outputDF=DC_Exp,
                                                      i = k, 
                                                      SampType = "PHS", 
                                                      PickNo = Current_Samp,
                                                      Bef_Aft = "Aft")
                    Current_Samp=Current_Samp+1
                
            
                
            
            #This is where processing starts, along with simulated harvest. 
            start_HD = time.time()
            if i in Inputz_T.Harvest_Days: #Harvest days. Go here.
                
                #Harvest Sampling
                if Scen_T.Samp_Plan == 2:
                    
                    #Collection of Outputs

                    DC_Exp= Dictionariez_T.Output_Collection_Sampling(df = Field_df, 
                                                      outputDF=DC_Exp,
                                                      i = k, 
                                                      SampType = "PHS", 
                                                      PickNo = Current_Samp,
                                                      Bef_Aft = "Bef")

                    DC_Exp = Dictionariez_T.Output_Collection_Sampling_Weight_R(df = Field_df, 
                                                      outputDF=DC_Exp,
                                                      i = k, 
                                                      SampType = "PHS", 
                                                      PickNo = Current_Samp,
                                                      Bef_Aft = "Bef")

    
                    if Scen_T.Samp_Method == 1:
                        Field_df = Funz_T.F_Sampling_T (df= Field_df, 
                                                  Pick_No = Current_Pick, 
                                                  Location = 1, #Location is in field
                                                  NSamp_Unit = 1, 
                                                  NoGrab = Scen_T.Tomatoes_per_sample) 
                    elif  Scen_T.Samp_Method == 2:
                        print("Mash Sampling 2")
                        Field_df =  Funz_T.F_Sampling_T_Mash (df= Field_df, 
                                                              Pick_No= Current_Pick, 
                                                              Location =1,
                                                              NSamp_Unit =1, 
                                                              NoGrab= Scen_T.Tomatoes_per_sample, 
                                                              Subsample_Mass=25,
                                                              N_replicates = Scen_T.N_Replicates)

                    
                    #Rejection rules, reject current pick plus any upcoming picks
                    Field_df=Funz_T.F_Rejection_Rule_T (df = Field_df, 
                                        Pick_No = Current_Samp, 
                                        Av_Picks= list(range(Current_Pick,Inputz_T.N_Pick+1)), 
                                        Test_Unit = "Pick_ID", 
                                        limit = 0)
                    
                    DC_Exp= Dictionariez_T.Output_Collection_Sampling(df = Field_df, 
                                      outputDF=DC_Exp,
                                      i = k, 
                                      SampType = "PHS", 
                                      PickNo = Current_Samp,
                                      Bef_Aft = "Aft")
                    
                    DC_Exp = Dictionariez_T.Output_Collection_Sampling_Weight_R(df = Field_df, 
                                                      outputDF=DC_Exp,
                                                      i = k, 
                                                      SampType = "PHS", 
                                                      PickNo = Current_Samp,
                                                      Bef_Aft = "Aft")
                    Current_Samp=Current_Samp+1
                
                
                
                #Location 2
                #Collection contmaination at processing stages. 
                DC_Cont_Processing= Dictionariez_T.Output_Collection_Prog(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing , 
                                                                          Step_Column = "Harvest_"+str(Current_Pick) ,
                                                                          i = k)
                
                DC_Cont_Processing_Prev= Dictionariez_T.Output_Collection_Prog_Prev(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing_Prev , 
                                                                          Step_Column = "Harvest_"+str(Current_Pick) ,
                                                                          i = k)
                
                Field_df = Funz_T.Harvesting_Function(df = Field_df, Total_Harvesters = Inputz_T.Total_Harvesters, 
                                              Tomatoes_Per_Bucket = Inputz_T.Tomatoes_Per_Bucket,
                                              Tomato_Sequence = Inputz_T.Tomato_Sequence, 
                                              Pick_No = Current_Pick,
                                              Tomatoes_per_Bin = Inputz_T.Tomatoes_per_Bin)

                
                #Harvester contmaination
                if (Scen_T.Cont_Scenario == 5):
                    #Picking the contaminated harvester at random
                    Contam_Harvester =Contaminated_Harvesters_Each [Current_Pick-1] 
                    #applying the contmainated harvester function to the Data. 
                    Field_df =Funz_T.Harvester_Cont_Function(df = Field_df,
                                            Hazard_Level = int(Scen_T.Total_Hazard/Inputz_T.N_Pick), #splitting contamination in 3 picks
                                            Pick_No =Current_Pick, 
                                            Cont_Harvester_No =Contam_Harvester )
                    
                #Bin Contmaination
                if (Scen_T.Cont_Scenario == 6):
                    #Picking the contaminated harvester at random
                    Contam_Bin = random.sample(list(range(1,Inputz_T.Total_Bins+1)),1)[0]
                    #applying the contmainated harvester function to the Data. 
                    Field_df =Funz_T.Bin_Cont_Function(df = Field_df,
                                            Hazard_Level = int(Scen_T.Total_Hazard/Inputz_T.N_Pick), #splitting contamination in 3 picks
                                            Pick_No =Current_Pick  , 
                                            Cont_Bin_No = Contam_Bin )
                
                
                
                #Transportation from the field to the shipping center
                #Here we need to caculate die-off for the tranportation of growth due to transportation. 
                Field_df = Funz_T.applying_survival_salmonella_cucum3(df = Field_df , 
                                                              Time = Inputz_T.Time_F_Sc,
                                                              RH = Inputz_T.RH_Florida,
                                                              Temp = Inputz_T.Temp_F_Sc,
                                                              Location = 2)

                
                #Updates location from Harvest to Shipping Center
                #Updating Cont
                DC_Cont_Processing= Dictionariez_T.Output_Collection_Prog(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing , 
                                                                          Step_Column = "Shipping Center_"+str(Current_Pick)
                                                                          ,i = k)
                
                DC_Cont_Processing_Prev= Dictionariez_T.Output_Collection_Prog_Prev(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing_Prev , 
                                                                          Step_Column = "Shipping Center_"+str(Current_Pick) ,
                                                                          i = k)
                
                #Updating location from 2 to 3
                Field_df=Funz_T.Update_Location2(df= Field_df, Previous = 2, NewLoc =3)
                
                
                #At Shipping center, temporary storage in open bins
                Field_df = Funz_T.applying_survival_salmonella_cucum3(df = Field_df , 
                                                              Time = Inputz_T.Time_Sc,
                                                              RH = Inputz_T.RH_Florida,
                                                              Temp = Inputz_T.Temp_Sc,
                                                              Location = 3)
                
                #From shipping center to packing facility.
                Field_df = Funz_T.applying_survival_salmonella_cucum3(df = Field_df , 
                                                              Time = Inputz_T.Time_Sc_Pack,
                                                              RH = Inputz_T.RH_Florida,
                                                              Temp = Inputz_T.Temp_Sc_Pack,
                                                              Location = 3)
                
                #Updates location from Shipping Center to Packing House
                Field_df=Funz_T.Update_Location2(df= Field_df, Previous = 3, NewLoc =4)
                
                DC_Cont_Processing= Dictionariez_T.Output_Collection_Prog(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing , 
                                                                          Step_Column = "Packinghouse_"+str(Current_Pick)
                                                                          ,i = k)
                
                DC_Cont_Processing_Prev= Dictionariez_T.Output_Collection_Prog_Prev(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing_Prev , 
                                                                          Step_Column = "Packinghouse_"+str(Current_Pick) ,
                                                                          i = k)
                
                #Receiving--------------------------------------------------------
                #### Sampling Plan at Receiving ----------------------------------
                if Scen_T.Samp_Plan == 3:
                    
                    #Collection of Outputs
                    DC_Exp= Dictionariez_T.Output_Collection_Sampling(df = Field_df, 
                                                      outputDF=DC_Exp,
                                                      i = k, 
                                                      SampType = "PHS", 
                                                      PickNo = Current_Samp,
                                                      Bef_Aft = "Bef")

                    DC_Exp = Dictionariez_T.Output_Collection_Sampling_Weight_R(df = Field_df, 
                                                      outputDF=DC_Exp,
                                                      i = k, 
                                                      SampType = "PHS", 
                                                      PickNo = Current_Samp,
                                                      Bef_Aft = "Bef")

                    if Scen_T.Samp_Method == 1:
                        Field_df = Funz_T.F_Sampling_T (df= Field_df, 
                                                  Pick_No = Current_Pick, 
                                                  Location = 4, #Location is in field
                                                  NSamp_Unit = 1, 
                                                  NoGrab = Scen_T.Tomatoes_per_sample) 
                    elif  Scen_T.Samp_Method == 2:
                        print("Mash Sampling R")
                        Field_df =  Funz_T.F_Sampling_T_Mash (df= Field_df, 
                                                              Pick_No= Current_Pick, 
                                                              Location =4,
                                                              NSamp_Unit =1, 
                                                              NoGrab= Scen_T.Tomatoes_per_sample, 
                                                              Subsample_Mass=25,
                                                              N_replicates = Scen_T.N_Replicates)

                    
                    #Rejection rules, reject current pick plus any upcoming picks

                    Field_df=Funz_T.F_Rejection_Rule_T (df = Field_df, 
                                        Pick_No = Current_Samp, 
                                        Av_Picks= list(range(Current_Pick,Inputz_T.N_Pick+1)), 
                                        Test_Unit = "Pick_ID", 
                                        limit = 0)

                    
                    DC_Exp= Dictionariez_T.Output_Collection_Sampling(df = Field_df, 
                                      outputDF=DC_Exp,
                                      i = k, 
                                      SampType = "PHS", 
                                      PickNo = Current_Samp,
                                      Bef_Aft = "Aft")
                    
                    DC_Exp = Dictionariez_T.Output_Collection_Sampling_Weight_R(df = Field_df, 
                                                      outputDF=DC_Exp,
                                                      i = k, 
                                                      SampType = "PHS", 
                                                      PickNo = Current_Samp,
                                                      Bef_Aft = "Aft")
                    Current_Samp=Current_Samp+1
                
                
                #Temporary Storage in Packing Facility
                Field_df = Funz_T.applying_survival_salmonella_cucum3(df = Field_df , 
                                                              Time = Inputz_T.Time_Pack,
                                                              RH = Inputz_T.RH_Florida,
                                                              Temp = Inputz_T.Temp_Pack,
                                                              Location = 4)
                
                #Processing
                #Wasing. 
                #Updates location from  Packing House to Washing --------------
                Field_df=Funz_T.Update_Location2(df= Field_df, Previous = 4, NewLoc =5)
                

                
                DC_Cont_Processing= Dictionariez_T.Output_Collection_Prog(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing , 
                                                                          Step_Column = "Washing_"+str(Current_Pick)
                                                                          ,i = k)
                
                DC_Cont_Processing_Prev= Dictionariez_T.Output_Collection_Prog_Prev(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing_Prev , 
                                                                          Step_Column = "Washing_"+str(Current_Pick) ,
                                                                          i = k)
                
                Field_df=Funz_T.Tomato_Wash(df = Field_df, Location  = 5, FC_lvl=Inputz_T.FC_lvl, i = random_seed+k)

                
                #Cross Contamination Conveyor Belt
                #Updates location from  Washing to Sorting---------------------
                Field_df=Funz_T.Update_Location2(df= Field_df, Previous = 5, NewLoc =6)
                
                DC_Cont_Processing= Dictionariez_T.Output_Collection_Prog(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing , 
                                                                          Step_Column = "CB1_"+str(Current_Pick)
                                                                          ,i = k)
                
                DC_Cont_Processing_Prev= Dictionariez_T.Output_Collection_Prog_Prev(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing_Prev , 
                                                                          Step_Column = "CB1_"+str(Current_Pick) ,
                                                                          i = k)

                Field_df=Funz_T.F_CrossContProLine_tom (df = Field_df, 
                                                 Tr_P_S = Inputz_T.Tr_P_CB, 
                                                 Tr_S_P = Inputz_T.Tr_CB_P,
                                                 Location = 6)
                


                
                #Drying Cross Contmination -----------------------------------
                #Updates location from  Conveyor Belt to Drying
                Field_df=Funz_T.Update_Location2(df= Field_df, Previous = 6, NewLoc =7)
                
                DC_Cont_Processing= Dictionariez_T.Output_Collection_Prog(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing , 
                                                                          Step_Column = "Drying_"+str(Current_Pick)
                                                                          ,i = k)
                
                DC_Cont_Processing_Prev= Dictionariez_T.Output_Collection_Prog_Prev(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing_Prev , 
                                                                          Step_Column = "Drying_"+str(Current_Pick) ,
                                                                          i = k)
                
                
                Field_df=Funz_T.F_CrossContProLine_tom (df = Field_df, 
                                                 Tr_P_S = Inputz_T.Tr_P_Dr, 
                                                 Tr_S_P = Inputz_T.Tr_Dr_P,
                                                 Location = 7 )
                
                #Sorting2 cross contmaination----------------------------------
                #Updates location from  Drying to Sorting
                Field_df=Funz_T.Update_Location2(df= Field_df, Previous = 7, NewLoc =8)
                
                DC_Cont_Processing= Dictionariez_T.Output_Collection_Prog(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing , 
                                                                          Step_Column = "Sorting_"+str(Current_Pick)
                                                                          ,i = k)
                
                DC_Cont_Processing_Prev= Dictionariez_T.Output_Collection_Prog_Prev(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing_Prev , 
                                                                          Step_Column = "Sorting_"+str(Current_Pick) ,
                                                                          i = k)
                
                Field_df=Funz_T.F_CrossContProLine_tom(df = Field_df, 
                                                 Tr_P_S = Inputz_T.Tr_P_SRT, 
                                                 Tr_S_P = Inputz_T.Tr_SRT_P,
                                                 Location = 8 )
                
                #Packing product into the cases at the Packing house.----------- 
                #Updates location from  Sorting to Packing
                Field_df=Funz_T.Update_Location2(df= Field_df, Previous = 8, NewLoc = 9)

                Field_df=Funz_T.Case_Packaging(df = Field_df,Case_Weight = 20,Tomato_Weight = 0.54, Location = 9)

                
                DC_Cont_Processing= Dictionariez_T.Output_Collection_Prog(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing , 
                                                                          Step_Column = "Packing_"+str(Current_Pick)
                                                                          ,i = k)
                
                DC_Cont_Processing_Prev= Dictionariez_T.Output_Collection_Prog_Prev(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing_Prev , 
                                                                          Step_Column = "Packing_"+str(Current_Pick) ,
                                                                          i = k)
                
                #Packed product sampling---------------------------------------
                if Scen_T.Samp_Plan == 4:
                    
                    #Collection of Outputs
                    DC_Exp= Dictionariez_T.Output_Collection_Sampling(df = Field_df, 
                                                      outputDF=DC_Exp,
                                                      i = k, 
                                                      SampType = "PHS", 
                                                      PickNo = Current_Samp,
                                                      Bef_Aft = "Bef")

                    DC_Exp = Dictionariez_T.Output_Collection_Sampling_Weight_R(df = Field_df, 
                                                      outputDF=DC_Exp,
                                                      i = k, 
                                                      SampType = "PHS", 
                                                      PickNo = Current_Samp,
                                                      Bef_Aft = "Bef")
                    #Whole tomato
                    if Scen_T.Samp_Method == 1:
                        Field_df = Funz_T.F_Sampling_T (df= Field_df, 
                                                  Pick_No = Current_Pick, 
                                                  Location = 9, #Location is in field
                                                  NSamp_Unit = 1, 
                                                  NoGrab = Scen_T.Tomatoes_per_sample) 
                    #Mashed Tomatoes
                    elif  Scen_T.Samp_Method == 2:
                        Field_df =  Funz_T.F_Sampling_T_Mash (df= Field_df, 
                                                              Pick_No= Current_Pick, 
                                                              Location =9,
                                                              NSamp_Unit =1, 
                                                              NoGrab= Scen_T.Tomatoes_per_sample, 
                                                              Subsample_Mass=25,
                                                              N_replicates = Scen_T.N_Replicates)

                    
                    #Rejection rules, reject current pick plus any upcoming picks
                    Field_df=Funz_T.F_Rejection_Rule_T (df = Field_df, 
                                        Pick_No = Current_Samp, 
                                        Av_Picks= list(range(Current_Pick,Inputz_T.N_Pick+1)), 
                                        Test_Unit = "Pick_ID", 
                                        limit = 0)

                    #updating output df
                    DC_Exp= Dictionariez_T.Output_Collection_Sampling(df = Field_df, 
                                      outputDF=DC_Exp,
                                      i = k, 
                                      SampType = "PHS", 
                                      PickNo = Current_Samp,
                                      Bef_Aft = "Aft")
                    #updating cells df
                    DC_Exp = Dictionariez_T.Output_Collection_Sampling_Weight_R(df = Field_df, 
                                                      outputDF=DC_Exp,
                                                      i = k, 
                                                      SampType = "PHS", 
                                                      PickNo = Current_Samp,
                                                      Bef_Aft = "Aft")
                    Current_Samp=Current_Samp+1
                
                
                #Post Packaging Storage ---------------------------------------
                Field_df = Funz_T.applying_survival_salmonella_cucum3(df = Field_df , 
                                                              Time = Inputz_T.Time_Post_Pack,
                                                              RH = Inputz_T.RH_Florida,
                                                              Temp = Inputz_T.Temp_Post_Pack,
                                                              Location = 9)
                #Ripening: 
                Field_df=Funz_T.Update_Location2(df= Field_df, Previous = 9, NewLoc = 10)
                
                DC_Cont_Processing= Dictionariez_T.Output_Collection_Prog(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing , 
                                                                          Step_Column = "PP_"+str(Current_Pick)
                                                                          ,i = k)
                
                DC_Cont_Processing_Prev= Dictionariez_T.Output_Collection_Prog_Prev(df = Field_df, 
                                                                          outputDF =DC_Cont_Processing_Prev , 
                                                                          Step_Column = "PP_"+str(Current_Pick) ,
                                                                          i = k)
                #Establishing which pick we are in
                Current_Pick = Current_Pick+1
                print(time.time() - start_HD, "HD Total Time") #Total time to run processinf
                
                
            #Adding Contmination to Every Day
            

            DC_Cont_Day=Dictionariez_T.Output_Collection_Prog(df = Field_df , outputDF =DC_Cont_Day , Step_Column = i,i = k)
            DC_Prev_Day=Dictionariez_T.Output_Collection_Prog_Prev(df = Field_df , outputDF =DC_Prev_Day, Step_Column = i,i = k)
    
                

            #Dieoff for Items that stayed in the Field. 
            Field_df = Funz_T.applying_survival_salmonella_cucum3(df = Field_df , 
                                                          Time = 24, #hr
                                                          RH = Inputz_T.RH_Florida,
                                                          Temp = Inputz_T.Temp_In_Field,
                                                          Location = 1)

            
        #Total Consumer Exposure dataframe updating..
        DC_Exp= Dictionariez_T.Output_Collection_Exp(df = Field_df, outputDF =DC_Exp ,i = k)
    return [DC_Exp,DC_Cont_Day,DC_Cont_Processing,DC_Cont_Processing_Prev,DC_Prev_Day, Cont_Day_List]    
        
