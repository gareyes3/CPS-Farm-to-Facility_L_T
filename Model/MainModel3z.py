

#%%
import sys
sys.path
#sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model')
sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility\Model')

#%%
Progression_DFS = []

#%% 
#Libraries, Modules
import pandas as pd 
import seaborn as sns
from matplotlib import pyplot as plt
import Funz
import ContScen
import Listz 
import InFunz
import ScenCondz
import ContCondz
import Inputz
from importlib import reload  
reload(Listz)
#reload(Inputz)

#%%

def F_MainLoop():

    for  i in range(Inputz.N_Iterations):
        print(i)
        
        #Adding Background Contamination
        
    
        #STEP 0 CONTAMINATION SCENARIOS  ----------------------------------------------------------------------------------------------------
    
        #Creation of the Data Frame to Track: 
        df= InFunz.F_InDF(Partition_Units = Inputz.Partition_Units,
                          Field_Weight = Inputz.Field_Weight, 
                          slot_number = Inputz.slot_number)
        
        #Adding Contamination depending on challenge Background
        if ContCondz.Background_C == 1:
            df = ContScen.F_Background_C(df=df, 
                                         Hazard_lvl = Inputz.Hazard_lvl, 
                                         Partition_Units= Inputz.Partition_Units)
            
        #Adding Contamination depending on challenge Point_Source
        if ContCondz.Point_Source_C == 1:
            df=ContScen.F_Point_Source_C(df=df, 
                                         Hazard_lvl=Inputz.Hazard_lvl,
                                         No_Cont_Clusters =Inputz.No_Cont_Clusters, 
                                         Cluster_Size = Inputz.Cluster_Size, 
                                         Partition_Weight = Inputz.Partition_Weight)
    
            
        #Adding Contamination depending on challenge Systematic Sampling
        if ContCondz.Systematic_C == 1:
            df = ContScen.F_systematic_C(df=df, Hazard_lvl= Inputz.Hazard_lvl,
                                         No_Cont_Clusters =Inputz.No_Cont_Clusters,
                                         Cluster_Size= Inputz.Cluster_Size,
                                         Partition_Weight = Inputz.Partition_Weight)
            
        # Outputs: Initial Contamination     
        LV_Initial_CFU= sum(df.CFU)
        Listz.List_Initial_CFU.append(LV_Initial_CFU)
        
    
        #STEP 1 PREHARVEST ------------------------------------------------------------------------------------------------------------------
        
        #Die-off From Contamination Event to Pre-Havrvest
        #Die_Off_CE_PHS =Funz.F_DieOff_IR_PH(Time_CE_PHS,Break_Point, Dieoff1, Dieoff2) #Die off rate from Irrigation to pre harvest sampling
        
        LV_Die_Off_CE_PHS = Funz.F_Simple_DieOff(Inputz.Time_CE_PHS) #
        df["CFU"] =  df["CFU"]*(10**LV_Die_Off_CE_PHS) #Applying Die off through DFs
        LV_Time_Agg = 0 + Inputz.Time_CE_PHS #Cummulative time so far in the process.
            
        #Sampling at Pre-Harvest
        if ScenCondz.PH_Sampling ==1: #If function to turn off Pre-Harvest Sampling
            if ScenCondz.PHS_Int ==1:
                df = Funz.F_Sampling_2(df =df,Test_Unit ="Lot", 
                                              NSamp_Unit = Inputz.n_samples_lot_PH, 
                                              Samp_Size =Inputz.sample_size_PH, 
                                              Partition_Weight =Inputz.Partition_Weight, 
                                              NoGrab =Inputz.No_Grabs_PH )
            else:
            #Pre-Harvest Sampling, 
                 df = Funz.F_Sampling_2(df =df,Test_Unit ="Sublot", 
                                           NSamp_Unit = Inputz.n_samples_slot_PH, 
                                           Samp_Size =Inputz.sample_size_PH, 
                                           Partition_Weight =Inputz.Partition_Weight, 
                                           NoGrab =Inputz.No_Grabs_PH )
            
            
        LO_Cont_B_PH = sum(df.CFU) #Contamination before rejection sampling
        Listz.List_BPHS_CFU.append( LO_Cont_B_PH) #List of contamination before sampling
        
        #Filtering out the Rejected lots, Pre-Harvest
        if ScenCondz.PHS_Int ==1:
           df= Funz.F_Rejection_Rule2(df =df, Test_Unit = "Lot", limit = 0)  
        else: 
            df=Funz.F_Rejection_Rule2(df =df, Test_Unit = "Sublot", limit = 0) 
                           
        
        #Outputs from Pre-Harvest Sampling
        LO_WeightAcc_PH = sum(df.Weight) #Lb
        LO_WeightRej_PH = Inputz.Field_Weight-LO_WeightAcc_PH #Lb
        LO_ContAcc_PH = sum(df.CFU) # Total CFU
        LO_ContRej_PH =  LO_Cont_B_PH-LO_ContAcc_PH #Total CFU
        if LO_ContAcc_PH == 0:
            LO_ContRej_P_PH = 1
        else:
            LO_ContRej_P_PH = LO_ContRej_PH/(LO_ContAcc_PH+LO_ContRej_PH) #Percentage Rejected by H sampling
        
        #Outputs for Iterations
        Listz.Total_PA_PH.append(LO_WeightAcc_PH)
        Listz.Total_PR_PH.append(LO_WeightRej_PH)
        Listz.Total_CA_PH.append(LO_ContAcc_PH)
        Listz.Total_CR_PH.append(LO_ContRej_PH)
        Listz.List_Cont_PercRej_PH.append(LO_ContRej_P_PH)
        
        #STEP 2 HARVEST ---------------------------------------------------------------------------------------------------------------------
        
        #Pre-Harvest Sampling - Harvest Sampling Die off
        LV_Time_Agg = LV_Time_Agg + Inputz.Time_PHS_H #Cummulative time so far in the process.
        LV_Die_off_B = Funz.F_Simple_DieOff(LV_Time_Agg)
        LV_Die_Off_PHS_HS= LV_Die_off_B-LV_Die_Off_CE_PHS#Funz.F_DieOff_PHS_HS(Time_PHS_H, Time_Agg, Break_Point, Dieoff1, Dieoff2)
        df['CFU'] = df['CFU']*(10**LV_Die_Off_PHS_HS) #Updating Contmination to Show Total DieOff
        
        #Adding Contamination depending on challenge at harvest
        if ContCondz.Crew_C == 1:
            df = ContScen.F_Crew_C(df =df, 
                                   Hazard_lvl =Inputz.Hazard_lvl, 
                                   No_Cont_Clusters = Inputz.No_Cont_Clusters,
                                   Cluster_Size =Inputz.Cluster_Size, 
                                   Partition_Weight = Inputz.Partition_Weight)
    
        if ContCondz.Harvester_C == 1:
            df = ContScen.F_Harvester_C(df =df, 
                                        Hazard_lvl =Inputz.Hazard_lvl, 
                                        No_Cont_Clusters = Inputz.No_Cont_Clusters, 
                                        Cluster_Size =Inputz.Cluster_Size, 
                                        Partition_Weight = Inputz.Partition_Weight)
        
        
        #Harvest Sampling
        if ScenCondz.H_Sampling == 1:
            if ScenCondz.HS_Trad==1:
                df = Funz.F_Sampling_2(df =df,
                                             Test_Unit ="Sublot", 
                                             NSamp_Unit = Inputz.n_samples_slot_H, 
                                             Samp_Size =Inputz.sample_size_H, 
                                             Partition_Weight =Inputz.Partition_Weight, 
                                             NoGrab =Inputz.No_Grabs_H )
            elif ScenCondz.HS_Agg==1:
               df = Funz.F_Sampling_2(df =df,Test_Unit ="Sublot", 
                                               NSamp_Unit = 10, 
                                               Samp_Size =Inputz.sample_size_H, 
                                               Partition_Weight =Inputz.Partition_Weight, 
                                               NoGrab =Inputz.No_Grabs_H )

            
        #Before pre harvest sampling
        LO_Cont_B_H = sum(df.CFU) #Contamination before sampling
        Listz.List_BHS_CFU.append(LO_Cont_B_H) #List of contaminations before sampling
        
        #Filtering out the Rejected lots, Harvest Sampling
        df = Funz.F_Rejection_Rule2 (df =df, Test_Unit = "Sublot",limit = 0) 
            
        
        #Outputs from Pre-Harvest Sampling
        LO_WeightAcc_H = sum(df.Weight) #Lb
        LO_WeightRej_H = Inputz.Field_Weight-LO_WeightAcc_H #Lb
        LO_ContAcc_H = sum(df.CFU) # Total CFU
        LO_ContRej_H =  LO_Cont_B_H-LO_ContAcc_H #Total CFU
        if LO_ContAcc_H == 0:
            LO_ContRej_P_H = 1
        else:
            LO_ContRej_P_H = LO_ContRej_H/(LO_ContAcc_H+LO_ContRej_H) #Percentage Rejected by H sampling
        
        #Outputs for Iterations
        Listz.Total_PA_H.append(LO_WeightAcc_H)
        Listz.Total_PR_H.append(LO_WeightRej_H)
        Listz.Total_CA_H.append(LO_ContAcc_H)
        Listz.Total_CR_H.append(LO_ContRej_H)
        Listz.List_Cont_PercRej_H.append(LO_ContRej_P_H)
        
        #STEP 3 RECEIVING ---------------------------------------------------------------------------------------------------------------------
        '''  
        #Pre-Cooling of Lettuce
        LV_Time_Agg = LV_Time_Agg + Inputz.Time_R_PC #Time from Receiving to Pre-Cooling
        # Process Pending, Reduction? 
        
        #Cold Storage:
        df = Funz.F_Growth(DF=df, 
                           Temperature=Inputz.Temperature_ColdStorage, 
                           TimeD= Inputz.Time_ColdStorage)#Growth during cold storage
        
        LV_Time_Agg = LV_Time_Agg + Inputz.Time_ColdStorage #Time between Pre-Cooling and Cold Storage. 
        '''
                                                             
        #Harvest Sampling - Receiving Harvest Sampling Die off
        #Transportation from havest to faility
        GrowthOutsHF = Funz.Growth_Function_Lag(DF =df, 
                                                Temperature = Inputz.Temperature_H_RS, 
                                                Time = Inputz.Time_H_RS, 
                                                Lag_Consumed_Prev  = Inputz.Lag_Consumed_Prev)
        
        df = GrowthOutsHF[0]
        Inputz.Lag_Consumed_Prev = GrowthOutsHF[1]
        
        #Hydrocooling
        GrowthOutsHF = Funz.Growth_Function_Lag(DF =df, 
                                        Temperature = Inputz.Temperature_H_RS, 
                                        Time = Inputz.Time_H_RS, 
                                        Lag_Consumed_Prev  = Inputz.Lag_Consumed_Prev)
        
        
        #Paletization
        
        df = Funz.F_Palletization(df=df,
                                  Field_Weight=Inputz.Field_Weight,
                                  Pallet_Weight=Inputz.Pallet_Weight,
                                  Partition_Weight = Inputz.Partition_Weight,
                                  )
        
    
        LV_Time_Agg = LV_Time_Agg + Inputz.Time_H_RS #Cummulative time so far in the process. 
        
        LO_Cont_B_R = sum(df.CFU)
        Listz.List_BRS_CFU.append(LO_Cont_B_R) #Contamination before receiving sampling
        
        if ScenCondz.R_Sampling == 1:
            #Sampling at Reception
            df = Funz.F_Sampling_2(df =df,Test_Unit ="PalletNo", 
                                           NSamp_Unit = Inputz.n_samples_pallet, 
                                           Samp_Size =Inputz.sample_size_R, 
                                           Partition_Weight =Inputz.Partition_Weight, 
                                           NoGrab =Inputz.No_Grabs_R )
        
        #Rejecting Inidividual pallets if 1 positive
        df = Funz.F_Rejection_Rule2 (df =df, Test_Unit = "PalletNo", limit = 0) 
        
        
        #Outputs from Pre-Harvest Sampling
        LO_WeightAcc_R = sum(df.Weight) #Lb
        LO_WeightRej_R = Inputz.Field_Weight-LO_WeightAcc_R #Lb
        LO_ContAcc_R = sum(df.CFU) # Total CFU
        LO_ContRej_R =  LO_Cont_B_R-LO_ContAcc_R #Total CFU
        if LO_ContAcc_R == 0:
            LO_ContRej_P_R = 1
        else:
            LO_ContRej_P_R = LO_ContRej_R/(LO_ContAcc_R+LO_ContRej_R) #Percentage Rejected by H sampling
        
        #Outputs for Iterations
        Listz.Total_PA_R.append(LO_WeightAcc_R)
        Listz.Total_PR_R.append(LO_WeightRej_R)
        Listz.Total_CA_R.append(LO_ContAcc_R)
        Listz.Total_CR_R.append(LO_ContRej_R)
        Listz.List_Cont_PercRej_R.append(LO_ContRej_P_R)
        
    
            
        #STEP 4 Value Addition ---------------------------------------------------------------------------------------------------------------------
    
        #Splitting pallets into processing lines. 
        gb2 = Funz.F_ProLineSplitting(df =df, Processing_Lines = Inputz.Processing_Lines)
        
        #Splitting Processing Lines into Mini Batches
        gb2 = Funz.F_Partitioning_ProcLines(gb3 = gb2 , NPartitions = int(Inputz.Pallet_Weight/Inputz.Wash_Rate))
        
        #Value Addition Steps
    
        
        #Cross-Contamination Processing by processing line between 100 lb. batches 
        #1 Shredder
        LO_Cont_B_Shredder = Funz.F_SummingGB2Cont(gb2 =gb2) #Contamination before Shrdder
        Listz.Cont_B_Shredder.append( LO_Cont_B_Shredder)
        if ContCondz.PE_C ==1 and ContCondz.PE_Cont_Loc ==1:
            gb2 = ContScen.F_PEC_C(gb2= gb2,
                                   Hazard_lvl = Inputz.Hazard_lvl, 
                                   Processing_Lines = Inputz.Processing_Lines, 
                                   Lines_Cont = Inputz.Lines_Cont)
            
        ShredderOuts = Funz.F_CrossContProLine(gb2 =gb2, Tr_P_S = Inputz.Tr_P_Sh, Tr_S_P= Inputz.Tr_Sh_P)
        gb2 = ShredderOuts[0]
        ShredCont = ShredderOuts[1]   
        #2 Conveyor Belt
        LO_Cont_B_Belt = Funz.F_SummingGB2Cont(gb2 =gb2) #Contamination before BElt
        Listz.Cont_B_Belt.append( LO_Cont_B_Belt)
        if ContCondz.PE_C ==1 and ContCondz.PE_Cont_Loc ==2:
            gb2 = ContScen.F_PEC_C(gb2= gb2,
                                   Hazard_lvl = Inputz.Hazard_lvl, 
                                   Processing_Lines = Inputz.Processing_Lines, 
                                   Lines_Cont = Inputz.Lines_Cont)
            
        CVOuts = Funz.F_CrossContProLine(gb2 = gb2, Tr_P_S = Inputz.Tr_P_Cv, Tr_S_P = Inputz.Tr_Cv_P)
        gb2 = CVOuts[0]
        CvCont = CVOuts[1]
        
        
        #3Washing:
        LO_Cont_B_Washing = Funz.F_SummingGB2Cont(gb2 =gb2) #Contamination before Washing
        Listz.Cont_B_Washing.append( LO_Cont_B_Washing)
        if ContCondz.PE_C ==1 and ContCondz.PE_Cont_Loc ==3:
            gb2 = ContScen.F_PEC_C(gb2= gb2,
                                   Hazard_lvl = Inputz.Hazard_lvl, 
                                   Processing_Lines = Inputz.Processing_Lines, 
                                   Lines_Cont = Inputz.Lines_Cont)
            
        DF_Chlevels = Funz.F_Chloride_lvl(300) #Simlating Chlorine levels after time.
        gb2 = Funz.F_Washing_ProcLines(List_GB3 =gb2, Wash_Rate = Inputz.Wash_Rate, Cdf =  DF_Chlevels)
        
        #4 Shaker Table
        LO_Cont_B_Shaker = Funz.F_SummingGB2Cont(gb2 =gb2) #Contamination before Shaker Table
        Listz.Cont_B_Shaker.append( LO_Cont_B_Shaker)
        if ContCondz.PE_C ==1 and ContCondz.PE_Cont_Loc ==4:
            gb2 = ContScen.F_PEC_C(gb2= gb2,
                                   Hazard_lvl = Inputz.Hazard_lvl, 
                                   Processing_Lines = Inputz.Processing_Lines, 
                                   Lines_Cont = Inputz.Lines_Cont)
            
        StOuts = Funz.F_CrossContProLine(gb2 =gb2, Tr_P_S = Inputz.Tr_P_St, Tr_S_P= Inputz.Tr_St_P)
        gb2 = StOuts[0]
        StCont = StOuts[1]
        
        #5 Centrifuge
        LO_Cont_B_Centrifuge = Funz.F_SummingGB2Cont(gb2 =gb2) #Contamination before Centrigure
        Listz.Cont_B_Centrifuge.append( LO_Cont_B_Centrifuge)
    
        if ContCondz.PE_C ==1 and ContCondz.PE_Cont_Loc ==5:
            gb2 = ContScen.F_PEC_C(gb2= gb2,
                                   Hazard_lvl = Inputz.Hazard_lvl, 
                                   Processing_Lines = Inputz.Processing_Lines, 
                                   Lines_Cont = Inputz.Lines_Cont)
            
        CentrifugeOuts = Funz.F_CrossContProLine(gb2 =gb2, Tr_P_S = Inputz.Tr_P_C, Tr_S_P= Inputz.Tr_C_P)
        gb2 = CentrifugeOuts[0]
        CentrifugeCont = CentrifugeOuts[1]
            
        #Adding Contamination from Scenario to each lot
        if ContCondz.PE_C ==1:
            gb2 = ContScen.F_PEC_C(gb2= gb2,
                                   Hazard_lvl = Inputz.Hazard_lvl, 
                                   Processing_Lines = Inputz.Processing_Lines, 
                                   Lines_Cont = Inputz.Lines_Cont)
            
        
        #Joining Data Frames into one again, with contamination from lines. 
        df=(pd.concat(gb2))
        #Outputs after value addition.
        LO_Cont_A_VA= sum(df.CFU)
        Listz.List_AVA_CFU.append(LO_Cont_A_VA)
        
    
            
        df['Lot'] =1#Updating the CFU/g column
 
            
        #Environmental Monitoring Program
        
        
        #STEP 5 PACKING AND MIXING ---------------------------------------------------------------------------------------------------------------------
        
        #Mixing products into one batch
        df = df.reset_index(drop=True) 
        LV_NewPart_Weight  = df.at[1,"Weight"]
        LV_N_Partitions = int(LV_NewPart_Weight/Inputz.Pack_Weight_FP) 
        df = Funz.F_Partitioning(DF=df,
                                 NPartitions= LV_N_Partitions)
        
        if Inputz.N_Lots_FP==2:
            df =Funz.F_Lots_FP(df=df, 
                               Nolots = 2)
            
            #Dividing the pallets dataframe into different processing lines.  
        gb2 = df.groupby('ProLine')#Creating Listby procesing line
        gb2 =[gb2.get_group(x) for x in gb2.groups] #Creating list of separate dataframe by processing lines
        
        if ContCondz.Pack_C ==1:
            gb2 = ContScen.F_PEC_C(gb2=gb2,
                            Hazard_lvl = Inputz.Hazard_lvl, 
                            Processing_Lines = Inputz.Processing_Lines, 
                            Lines_Cont = Inputz.Lines_ContPack)
        
        df=(pd.concat(gb2))
        df["Accept"] = True
        df['Grabs'] = [list() for x in range(len(df.index))]
        df["Positives"] = ""
        
        
        LO_Cont_B_FP = sum(df.CFU) #Total CFU before FP Sampling
        Listz.List_BFPS_CFU.append(LO_Cont_B_FP) #Adding it to a List
        #df= Funz.F_Packaging(DF=df, Boxes_Pallet=Boxes_Pallet)
        
    
        
        #Sampling Step
        if ScenCondz.FP_Sampling == 1:
            if ScenCondz.FPS_Trad ==1:
                df =Funz.F_Sampling_2(df =df,Test_Unit ="Lot", 
                                           NSamp_Unit = Inputz.n_samples_FP, 
                                           Samp_Size =Inputz.sample_size_FP, 
                                           Partition_Weight =Inputz.Pack_Weight_FP, 
                                           NoGrab = Inputz.N_Packages_Samples)
                
            elif ScenCondz.FPS_Agg ==1:
                df =Funz.F_Sampling_2(df =df,Test_Unit ="Lot", 
                                           NSamp_Unit = Inputz.n_samples_FP, 
                                           Samp_Size =Inputz.sample_size_FP, 
                                           Partition_Weight =Inputz.Pack_Weight_FP, 
                                           NoGrab = Inputz.N_Packages_Samples)
        
    
        #Filtering out the Rejected lots, Final product
        #Rejecting Inidividual pallets if 1 positive
        df = Funz.F_Rejection_Rule2 (df =df, Test_Unit = "Lot",limit = 0) 
        
        LO_WeightAcc_FP = sum(df.Weight) #Lb
        LO_WeightRej_Total = Inputz.Field_Weight - LO_WeightAcc_FP #Lb
        LO_PerRej_Total =  LO_WeightRej_Total/Inputz.Field_Weight
        LO_ContAcc_FP = sum(df.CFU) # Total CFU
        LO_ContRej_FP =  LO_Cont_B_FP-LO_ContAcc_FP #Total CFU
        if LO_ContAcc_FP == 0:
            LO_ContRej_P_FP = 1
        else:
            LO_ContRej_P_FP = LO_ContAcc_FP/(LO_ContAcc_FP+LO_ContRej_FP) #Percentage Rejected by H sampling
            
        if LO_WeightAcc_FP == 0:
            Total_CFU_G_FP = 0 #Total CFU per gram of final product
        else:
            Total_CFU_G_FP = LO_ContAcc_FP/( LO_WeightAcc_FP*454) #Total CFU per gram of final product
            
            #Outputs for Iterations
        Listz.Total_PA_FP.append(LO_WeightAcc_FP)
        Listz.Total_PR_Final.append(LO_WeightRej_Total)
        Listz.Total_PerRej_Weight.append(LO_PerRej_Total)
        Listz.Total_CA_FP.append(LO_ContAcc_FP)
        Listz.Total_CR_FP.append(LO_ContRej_FP)
        Listz.List_Cont_PercRej_FP.append(LO_ContRej_P_FP)
        Listz.List_TotalCFUg_FP.append(Total_CFU_G_FP)
    
        #STEP 6 POST PROCESS STEPS ---------------------------------------------------------------------------------------------------------------------
        #Steps after Final Product
        if(ScenCondz.Customer_Added_Steps ==1):
            #Growth or Die-off during storage post processing
            df = Funz.F_Growth(DF=df, 
                               Temperature=Inputz.Temperature_ColdStorage, 
                               TimeD= Inputz.Time_PostPStorage) #Growth during cold storage
            '''
            Case_Weight= 20 
            #Adding Shipping Pallets and Cases. 
            Packages_Case = Case_Weight/Inputz.Pack_Weight_FP
            Total_Packages = len(df.index)
            Total_Cases = Total_Packages/Case_Weight
            print(Total_Cases)
            Case_Pattern = [i for i in range(1, int(Total_Cases)+1) for _ in range(int(Packages_Case))]
            Crop_No = len(df.index)
            Pallet_Pattern=Pallet_Pattern[:Crop_No]
            Sequence Pallets
            '''
            #Transportation through trucks.
            df = Funz.F_Growth(DF=df,
                               Temperature= Inputz.Transportation_Temp, 
                               TimeD= Inputz.Trasnportation_Time)
            
            #Storage at customer: 
            df = Funz.F_Growth(DF=df,
                       Temperature= Inputz.Transportation_Temp, 
                       TimeD= Inputz.Trasnportation_Time)
            
    #Simplest Output
    Final_ContPlot =sns.boxplot(y=Listz.Total_CA_FP)
    plt.ylabel("Total CFU Remaining in System")
    
    #Progression Data
    data_contprog = {"Initial":Listz.List_Initial_CFU,
                 "Bef Pre-Harvest Samp": Listz.List_BPHS_CFU,
                 "Aft Pre-Harvest Samp": Listz.Total_CA_PH,
                 "Bef Harvest Samp":Listz.List_BHS_CFU,
                 "Aft Harvest Samp": Listz.Total_CA_H,
                 "Bef Receiving Samp": Listz.List_BRS_CFU,
                 "After Receiving Samp": Listz.Total_CA_R,
                 "Bef Shredding":Listz.Cont_B_Shredder,
                 "Bef Conveyor Belt":Listz.Cont_B_Belt,
                 "Bef Washing":Listz.Cont_B_Washing,
                 "Bef Shaker Table":Listz.Cont_B_Shaker,
                 "Bef Centrifuge":Listz.Cont_B_Centrifuge,
                 "Aft Value Addition": Listz.List_AVA_CFU,
                 "Bef Final Prod S": Listz.List_BFPS_CFU,
                 "Final Product": Listz.Total_CA_FP
                 }

    df_contprog = pd.DataFrame(data_contprog)

    #Main Output Data
    data_outputs={"Total_CFU_A":Listz.Total_CA_FP,
                   "Total_CFU_Rej": Listz.Total_CR_FP,
                   "Total_CFUg_A": Listz.List_TotalCFUg_FP,
                  "Total_Weight_A":Listz.Total_PA_FP,
                  "Total_Weight_R": Listz.Total_PR_Final,
                  "PerRejectedWeight": Listz.Total_PerRej_Weight,
                  "PerRejected at PH":Listz.List_Cont_PercRej_PH,
                  "PerRejected at H":Listz.List_Cont_PercRej_H,
                  "PerRejected at R":Listz.List_Cont_PercRej_R,
                  "PerRejected at FP":Listz.List_Cont_PercRej_FP,
        }

    df_outputs = pd.DataFrame(data_outputs)
    
    outputs = [df_contprog, df_outputs]
    return outputs
    


