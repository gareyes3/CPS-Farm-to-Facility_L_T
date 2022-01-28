import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import lognorm
import math
import random
import itertools
import ScenCondz
import matplotlib as plt
import SCInputz



#Function Source File
#%% Utility Functions
#Normal Truncated function
def Func_NormalTrunc(Min,Max, Mean, SD):
     X= stats.truncnorm((Min - Mean) / SD, (Max - Mean) / SD, loc=Mean, scale=SD)
     Y=(np.float(X.rvs(1)))
     return Y
 
def pert(a, b, c, *, size=1, lamb=4):
    r = c - a
    alpha = 1 + lamb * (b - a) / r
    beta = 1 + lamb * (c - b) / r
    return a + np.random.beta(alpha, beta, size=size) * r


#%% Die off functions    

#Die-off model

def F_DieOff1():
    Die_off_rate1=Func_NormalTrunc(-16.52,-0.47, -7.07,3.41)
    return Die_off_rate1

def F_DieOff2():
    Die_off_rate2=Func_NormalTrunc(-1.94,3.04, -0.24,0.70)
    return Die_off_rate2

#Die -off from Irrigation to Pre-Harvest
def F_DieOff_IR_PH(Time, Break_Point,Dieoff1, Dieoff2):
    TimeD = Time
    if TimeD < Break_Point: 
        T_Die_off= Dieoff1*TimeD
    elif TimeD >= Break_Point:
        Seg1T = TimeD-Break_Point
        T_Die_off1=Dieoff1*Seg1T
        Seg2T = TimeD - Seg1T
        T_Die_off2= Dieoff2*Seg2T
        T_Die_off = T_Die_off1+T_Die_off2
    return T_Die_off

#Die-off from Pre-Harvest Sampling to Harvest sampling
def F_DieOff_PHS_HS(Time,Time_Agg,Break_Point ,Dieoff1, Dieoff2 ):
    if Time_Agg < Break_Point: 
        TimeLeft = Break_Point-Time_Agg
        if Time < TimeLeft:
            T_Die_off = Dieoff1*Time
        elif Time >=TimeLeft:
            Seg1T = Time-TimeLeft
            T_Die_off1=Dieoff1*Seg1T
            Seg2T = Time-Seg1T
            T_Die_off2=Dieoff2*Seg2T
            T_Die_off = T_Die_off1+T_Die_off2
    elif Time_Agg>=Break_Point:
        T_Die_off=Dieoff2*Time
    return T_Die_off


def F_Simple_DieOff (Time): 
    #Reduction = -((Time/(2.45/24))**0.3)
    dieoff= Func_NormalTrunc(-1.04,-0.33, -0.77,0.21) #Belias linear die-off. 
    Reduction  = dieoff*Time
    return Reduction

def Applying_dieoff (df,Dieoff):
    df["CFU"] =  df["CFU"]*(10**Dieoff) #Applying Die off through DFs
    return df

def F_Simple_Reduction(df, Reduction):
    df["CFU"] =  df["CFU"]*(10**-Reduction) 
    return df

#%% Growth  or Reduction Models
#Cold Storage growth Model


def F_Growth(DF,Temperature, TimeD ):
    Parition_Weight_g = 50*454
    CFUs = DF["CFU"]
    b = 0.023
    Tmin  = 1.335-5.766 *b
    New_CFUs=[]
    for i in CFUs:
        CFUs_g = i/Parition_Weight_g #CFU/g
        if CFUs_g < (10**7): #7 log max density
            DieoffRate = np.random.triangular(0.0035, 0.013,0.040)/2.303 #log CFU /g h
            TotalGrowthRate = (b*(Temperature - Tmin))**(2)/(2.303) #log CFU /g h
            if Temperature >5:
                Growth  = 1
            else:
                Growth = 0
            if Growth == 1:
                TotalGrowth = (TotalGrowthRate*TimeD)
            else:
                TotalGrowth  = -DieoffRate * TimeD
            Updated_CFUs=(CFUs_g*10**TotalGrowth)*Parition_Weight_g #Final Growth change CFU/g
        else:
            Updated_CFUs = CFUs_g*Parition_Weight_g
        New_CFUs.append(Updated_CFUs)
    DF["CFU"] =New_CFUs 
    return DF



#Calculate Lag time at given temperature
def Growth_Function_Lag(DF, Temperature,Time,Lag_Consumed_Prev):
    if Temperature > 5:
        Lag_Time = 7544*(Temperature**-3.11) #laf frmula
        Proportion_Lag_Consumed = Time/Lag_Time
        Cummulative_Lag_Consumed = Lag_Consumed_Prev + Proportion_Lag_Consumed
        if Cummulative_Lag_Consumed < 1: 
            df2 = DF
        if Cummulative_Lag_Consumed >1:
            #time not in lag phase
            if Lag_Consumed_Prev < 1:
                PropNotLag =(((Cummulative_Lag_Consumed - 1))/Cummulative_Lag_Consumed)
                Growth_Time = Time*PropNotLag
                df2 = F_Growth(DF = DF,Temperature = Temperature,TimeD = Growth_Time)
            elif Lag_Consumed_Prev >1:
                Growth_Time = Time
                df2=F_Growth(DF =DF,Temperature = Temperature,TimeD = Growth_Time)
        Lag_Consumed_Prev = Cummulative_Lag_Consumed
    elif Temperature <=5:
        df2= F_Growth(DF =DF, Temperature = Temperature, TimeD = Time)
    outputs = [df2,Lag_Consumed_Prev]
    return outputs



#Washing
'''
def F_Washing (DF, LogRedWash):
    DF.CFU=DF.CFU*10**-LogRedWash 
    return DF
'''
#%% Contamination Functions

#Calculation of E.coli in Water
def F_Ecoli_Water():   
    Cw = random.uniform(1,235)
    X = stats.truncnorm((-5 - -1.9) / 0.6, (0 - -1.9) / 0.6, loc=-1.9, scale=0.6)
    Rw_1=(np.float(X.rvs(1)))
    Rw = 10**Rw_1
    Y = stats.truncnorm((0 - 0.108) / 0.019, (5 - 0.108) / 0.019, loc=0.108, scale=0.019)
    W=np.float(Y.rvs(1))
    Ci = (Cw/100)*Rw*W
    return Ci

def F_HarvestingCont ():
    Cs = 10**Func_NormalTrunc(Min=0, Max=3.67, Mean = 0.928, SD=1.11) #Soil, E.coli conc
    Rs = 10**Func_NormalTrunc(Min=-5, Max=0, Mean = -1.9, SD=0.6) #prob
    M = 10.22 #g soil in blades
    Nb = Cs *Rs*M #E coli cells in Blade CFU
    Rt1 = 0.0013 #Trasnfer Rate from soil to Lettuce
    Nh1 = Nb*Rt1 #Total E coli from harvesting blades to lettuce
    return Nh1

def F_InitialCont():
    #Using base pert distribution
    #Calculation of total CFUs
    Cont_CFU_g = float(pert(0,0,634))
    g_field = SCInputz.Field_Weight*454 #454 g in 1 lb. 
    Final_Cont = int(Cont_CFU_g*g_field)
    return Final_Cont
    
#%% Sampling Functions

#New Sampling Function
'''
#Outdates, Replaced with more efficient way to do the grabs iteration.
def F_Sampling_2 (df, Test_Unit, NSamp_Unit, Samp_Size, Partition_Weight, NoGrab):
    Unique_TestUnit = list(df[Test_Unit].unique())
    Grab_Weight = Samp_Size/NoGrab
    for i in (Unique_TestUnit): #From sublot 1 to sublot n (same for pallet,lot,case etc)
        for l in range (1, NSamp_Unit+1): #Number of samples per sublot or lot or pallet.
            for j in range(NoGrab):
                Sampled_Grab =df[df[Test_Unit] == i].sample(1, replace= True)
                Index = Sampled_Grab.index
                Index = Index[0]
                CFU = Sampled_Grab["CFU"]
                CFU_grab = CFU*(Grab_Weight/(Partition_Weight*454))
                P_Detection=1-math.exp(-CFU_grab)
                RandomUnif = random.uniform(0,1)
                if RandomUnif < P_Detection:
                    df.at[Index, 'PositiveSamples']. append(l)
    return (df)
'''

def F_Sampling_2 (df, Test_Unit, NSamp_Unit, Samp_Size, Partition_Weight, NoGrab):
    Unique_TestUnit = list(df[Test_Unit].unique())
    Grab_Weight = Samp_Size/NoGrab
    for i in (Unique_TestUnit): #From sublot 1 to sublot n (same for pallet,lot,case etc)
        for l in range (1, NSamp_Unit+1): #Number of samples per sublot or lot or pallet.
            for j in range(NoGrab):
                CFU_hh=np.array(df["CFU"])
                List_Random=random.choice(list(enumerate(CFU_hh)))
                CFU = List_Random[1]
                Index = List_Random[0]
                CFU_grab = CFU*(Grab_Weight/(Partition_Weight*454))
                P_Detection=1-math.exp(-CFU_grab)
                RandomUnif = random.uniform(0,1)
                if RandomUnif < P_Detection:
                    df.at[Index, 'PositiveSamples'].append(l)
    return (df)



#New Rejection Function
def F_Rejection_Rule2 (df, Test_Unit, limit):
    #Test_Unit = "Lot" or "Sublot"
    Listpositive = []
    for i, row in df.iterrows():
        Positives = len(set(df.at[i, "PositiveSamples"]))
        Listpositive.append(Positives)
    df.Positives =Listpositive
    Positives = df[df["Positives"]> limit]
    Unique_TestUnit=list(df[Test_Unit].unique())
    Unique_Positives = list(Positives[Test_Unit].unique())
    df.Positives = ""
    df.PositiveSamples = [list() for x in range(len(df.index))]
    if set(Unique_TestUnit)<= set(Unique_Positives):
        df_Blank = df.iloc[[0]]
        df_Blank.loc[:, ['CFU']] = 0
        df_Blank.loc[:, ['Weight']] = 1000
        df_Blank.loc[:, ['Accept']] = "All Rej"
        df = df_Blank
    else:
        df = df[~df[Test_Unit].isin(Unique_Positives)]
    return df


def F_Rejection_Rule3 (df, Test_Unit, limit):
    Unique_Test_Unit =list(df[Test_Unit].unique())
    Reject = []
    for  i in Unique_Test_Unit:
        df_Subset = df[df[Test_Unit] == i]
        List_of_grabs = df_Subset['PositiveSamples'].tolist()
        flat_list = [item for sublist in  List_of_grabs for item in sublist]
        Unique_Positives =list(np.unique(flat_list))
        if len(Unique_Positives)>limit:
            Reject.append(i)
    df.PositiveSamples = [list() for x in range(len(df.index))] #this is in case everything gets rejected
    if set(Unique_Test_Unit)<= set(Reject):
        df_Blank = df.iloc[[0]]
        df_Blank.loc[:, ['CFU']] = 0
        df_Blank.loc[:, ['Weight']] = SCInputz.Partition_Weight
        df_Blank.loc[:, ['Accept']] = "All Rej"
        df = df_Blank
    else:
        df = df[~df[Test_Unit].isin(Reject)]
    return df
        


#Sampling Sublots
#df =dateframe,
#NoSampleLot = Number of samples per lot
#Sample_size = Composite sample weight
#Cluster_Unit_weight 
#Limit= Limit CFU
#Grabs = Total grabs per sublot
def F_Sampling(df,Test_Unit, NSamp_Unit, Samp_Size, Partition_Weight, Limit, NoGrab ):
    #Df where contaminations are located
    #Test_Unit: Testing lot, as a whole, or sublots
    #N Samples/ Units: How many samples are taken per Test_Unit
    #Samp_Size: Sample Size Composite sample size
    #Partition_Weight: Weight of the partition
    #Limit : m maximum level of positive samples
    #No Grab: N60, grabs. 
    Results=[]
    Unique_TestUnit=list(df[Test_Unit].unique())
    for i in (Unique_TestUnit):
        Reject_Lis=[]
        for l in range (NSamp_Unit):
            Sampled_Grabs =df[df[Test_Unit] == i].sample(NoGrab, replace= True)
            Sampled_Grabs =list(Sampled_Grabs.CFU)
            Grab_Weight = Samp_Size/NoGrab
            Detected = []
            for j in Sampled_Grabs: 
                CFU_grab = j*(Grab_Weight/(Partition_Weight*454))
                P_Detection=1-math.exp(-CFU_grab)
                if random.uniform(0,1)<P_Detection:
                    Reject_YN=1
                else:
                    Reject_YN=0
                Detected.append(Reject_YN)
                if sum(Detected)>0:
                    Detected_YN = 1
                elif sum(Detected) ==0:
                    Detected_YN =0
            Reject_Lis.append(Detected_YN)
        a=sum(Reject_Lis)
        if a > Limit:
            AR= False
        else:
            AR= True
        Results.append(AR)
    data1 =  {Test_Unit: Unique_TestUnit,
           'Accept_Reject': Results}
    dT = pd.DataFrame(data1)
    dT= dT.loc[dT['Accept_Reject'] == False]
    ListR= list(dT[Test_Unit])
    return(ListR)

def F_SamplingFProd (df, Test_Unit, N_SampPacks, Grab_Weight):
    Results=[]
    Clust_Weight = int(df.loc[1,"Weight"]*454)
    Sampled_Packs = list(df[Test_Unit].sample(N_SampPacks))
    for i in Sampled_Packs:
        CFU = df.loc[df['PackNo'] == i, 'CFU'].values[0]
        CFU_grab = CFU*(Grab_Weight/(Clust_Weight*454))
        P_Detection=1-math.exp(-CFU_grab)
        if random.uniform(0,1)<P_Detection:
            Reject_YN=1
        else:
            Reject_YN=0
        Results.append(Reject_YN)
    return Results


def F_Rejection_Rule (df, LL_Rej_Lots, Test_Unit):
    #Test_Unit = "Lot" or "Sublot"
    Unique_TestUnit=list(df[Test_Unit].unique())
    if set(Unique_TestUnit)<= set(LL_Rej_Lots):
        df_Blank = df.iloc[[0]]
        df_Blank.loc[:, ['CFU']] = 0
        df_Blank.loc[:, ['Weight']] = 0
        df = df_Blank
    else:
        df = df[~df[Test_Unit].isin(LL_Rej_Lots)]
    return df

#%% Partitioning and Mixing Functions
def F_Palletization (df, Field_Weight,Pallet_Weight, Partition_Weight):
    Partitions_Per_Pallet =  int(Pallet_Weight/Partition_Weight)
    Pallet_Field = int(Field_Weight/Pallet_Weight)
    Pallet_Pattern = [i for i in range(1, Pallet_Field+1) for _ in range(int(Partitions_Per_Pallet))]
    Crop_No = len(df.index)
    Pallet_Pattern=Pallet_Pattern[:Crop_No]
    df['PalletNo'] = Pallet_Pattern
    df = df[['Lot', 'Sublot','PalletNo','PartitionID','CFU','PositiveSamples','Accept', 'Weight']]
    return df



def F_ProLineSplitting(df, Processing_Lines,): #
    df2=df.groupby(['PalletNo'], as_index =False)[["CFU", "Weight"]].sum()
    #Splitting Pallets into processing lines. Faccept
    N_Pallets = len(df2.index)
    num, div = N_Pallets, Processing_Lines #Getting list of pallets per line
    N_Divs =  ([num // div + (1 if x < num % div else 0)  for x in range (div)])
    N_Lines = list(range(1,Processing_Lines+1))
    L_ProLine =list(itertools.chain(*(itertools.repeat(elem, n) for elem, n in zip(N_Lines, N_Divs))))
    df2["ProLine"] = L_ProLine
    #Dividing the pallets dataframe into different processing lines.  
    gb = df2.groupby('ProLine')#Creating Listby procesing line
    gb2 =[gb.get_group(x) for x in gb.groups] #Creating list of separate dataframe by processing lines
    return gb2

def F_CrossContProLine (gb2, Tr_P_S, Tr_S_P):
    ContS_L=[]
    for j in gb2:
        ContS=0
        for row in j.itertuples():
            i  = row[0]
            ContP = j.CFU[i] #Contamination product
            TotTr_P_S= np.random.binomial(ContP,Tr_P_S) #Transfer from Product to Surfaces
            TotTr_S_P = np.random.binomial(ContS,Tr_S_P) #Trasnfer from Surfaves to product
            ContPNew = ContP-TotTr_P_S+TotTr_S_P #New Contmination on Product
            ContS=ContS+TotTr_P_S-TotTr_S_P #Remiining Contamination in Surface for upcoming batches
            j.at[i,("CFU")]=ContPNew #Updating the Contamination in the Data Frame
        ContS_L.append(ContS)
    Outputs = [gb2,ContS_L]
    return Outputs


def F_CrossContProLine2 (gb2, Tr_P_S, Tr_S_P):
    ContS_L=[]
    for j in gb2:
        ContS=0
        vectorCFU = j.CFU
        newvector=[]
        for i in vectorCFU:
            ContP = i #Contamination product
            TotTr_P_S= np.random.binomial(ContP,Tr_P_S) #Transfer from Product to Surfaces
            TotTr_S_P = np.random.binomial(ContS,Tr_S_P) #Trasnfer from Surfaves to product
            ContPNew = ContP-TotTr_P_S+TotTr_S_P #New Contmination on Product
            ContS=ContS+TotTr_P_S-TotTr_S_P #Remiining Contamination in Surface for upcoming batches
            i=ContPNew #Updating the Contamination in the Data Frame
            newvector.append(i)
        j["CFU"] = newvector
        ContS_L.append(ContS)
    Outputs = [gb2,ContS_L]
    return Outputs



#Paritioning Function
def F_Partitioning(DF,NPartitions):
    if ScenCondz.Field_Pack==False:
        AllParts_Cont = []
        for row in DF.itertuples():
            i = row[0]
            Cont = DF.at[i,'CFU']
            PartCont=np.random.multinomial(Cont,[1/NPartitions]*NPartitions,size=1)
            PartCont = PartCont[0]
            AllParts_Cont.append(PartCont)
        b_flat = [j for i in AllParts_Cont for j in i]
        newdf = pd.concat([DF]*NPartitions,axis=0)
        newdf=newdf.sort_values(by=['PalletNo'])
        #Pallet_List=(list(range(1,NPartitions+1)))
        newdf["PackNo"] =list(range(1,len(newdf.index)+1))#np.tile(Pallet_List, len(newdf)//NPartitions)
        newdf = newdf.reset_index(drop=True)  
        newdf.Weight=newdf.Weight/NPartitions
        newdf.CFU = b_flat
        newdf["Sublot"] = 1
        newdf = newdf[['PalletNo','PackNo','CFU', 'Weight', 'Sublot','ProLine','Lot']]
    elif ScenCondz.Field_Pack == True:
        AllParts_Cont = []
        for row in DF.itertuples():
            i = row[0]
            PartCont=np.random.multinomial(Cont,[1/NPartitions]*NPartitions,size=1)
            PartCont = PartCont[0]
            AllParts_Cont.append(PartCont)
        b_flat = [j for i in AllParts_Cont for j in i]
        newdf = pd.concat([DF]*NPartitions,axis=0)
        #Pallet_List=(list(range(1,NPartitions+1)))
        newdf["CaseNo"] =list(range(1,len(newdf.index)+1))#np.tile(Pallet_List, len(newdf)//NPartitions)
        newdf = newdf.reset_index(drop=True)  
        newdf.Weight=newdf.Weight/NPartitions
        newdf.CFU = b_flat
        newdf["Sublot"] = 1
        newdf = newdf[['CaseNo','CFU', 'Weight', 'Sublot','Lot']]
    return newdf

def F_Field_Packing(DF, Case_Weight, PartWeight):
    NPartitions = int(PartWeight/Case_Weight) 
    AllParts_Cont = []
    for row in DF.itertuples():
        i = row[0]
        Cont = DF.at[i,'CFU']
        PartCont=np.random.multinomial(Cont,[1/NPartitions]*NPartitions,size=1)
        PartCont = PartCont[0]
        AllParts_Cont.append(PartCont)
    b_flat = [j for i in AllParts_Cont for j in i]
    newdf = pd.concat([DF]*NPartitions,axis=0)
    newdf=newdf.sort_values(by=['Sublot'])
    #Pallet_List=(list(range(1,NPartitions+1)))
    newdf["CaseNo"] =list(range(1,len(newdf.index)+1))#np.tile(Pallet_List, len(newdf)//NPartitions)
    newdf = newdf.reset_index(drop=True)  
    newdf.Weight=newdf.Weight/NPartitions
    newdf.CFU = b_flat
    newdf = newdf[['CaseNo','CFU', 'Weight', 'Sublot','Lot']]
    return newdf
    

def F_Lots_FP(df, Nolots):
    l = len(df.index) // Nolots 
    df.loc[:l - 1, "Sublot"] = Nolots-1
    df.loc[l:, "Sublot"] = Nolots
    return df

def F_Mixing(DF):
    CFU_Summation = sum(DF.CFU)
    gram_Summation = sum(DF.Weight)*454
    Cont = CFU_Summation/gram_Summation
    ArrayUnique= pd.unique(DF['Sublot'])
    data1 = {'Sublot': [ArrayUnique],
       'Lot': 1,
       'Cont':Cont,
       'CFU':CFU_Summation,
       'Accept': True,
       'Weight': sum(DF.Weight)}
    df1 = pd.DataFrame(data1)  
    return df1


def parts(a, b):
    q, r = divmod(a, b)
    return [q + 1] * r + [q] * (b - r)


def F_Partitioning2(DF, Partition_Weight):
    LWeights = []
    LXX_2 = []
    for row in DF.itertuples():
        i = row[0]
        Weight= int(DF.at[i,'Weight'])
        xx_2=int(Weight//Partition_Weight)
        LXX_2.append(xx_2)
        Weight2 = parts(Weight,xx_2)
        LWeights.append(Weight2)  
    LWeightsFlat = [item for sublist in  LWeights for item in sublist]
    newDF= DF.loc[DF.index.repeat(LXX_2)]
    newDF["Weight"] = LWeightsFlat
    AllParts_Cont = []
    b_flat=[]
    DF['Parts'] =LXX_2
    for row in DF.itertuples():
        i = row[0]
        Cont = DF.at[i,'CFU']
        Parts = int(DF.at[i,'Parts'])
        PartCont=np.random.multinomial(Cont,[1/Parts]*Parts, size =1)
        PartCont = PartCont[0]
        AllParts_Cont.append(PartCont)
    b_flat = [j for i in AllParts_Cont for j in i]
    newDF.CFU = b_flat
    return newDF


#%%
def F_Partitioning_W(DF,NPartitions):
    AllParts_Cont = []
    for row in DF.itertuples():
        i = row[0]
        Cont = DF.at[i,'CFU']
        PartCont=np.random.multinomial(Cont,[1/NPartitions]*NPartitions,size=1)
        PartCont = PartCont[0]
        AllParts_Cont.append(PartCont)
    b_flat = [j for i in AllParts_Cont for j in i]
    newdf = pd.concat([DF]*NPartitions,axis=0)
    newdf=newdf.sort_values(by=['PalletNo'])
    #Pallet_List=(list(range(1,NPartitions+1)))
    newdf["Part"] =list(range(1,len(newdf.index)+1))#np.tile(Pallet_List, len(newdf)//NPartitions)
    newdf = newdf.reset_index(drop=True)  
    newdf.Weight=newdf.Weight/NPartitions
    newdf.CFU = b_flat
    return newdf



#Washing Chloride: 
def F_Chloride_lvl (Time_Wash):
    #Function Inputs. 
    #Changing times to 0.1 increments.
    Times = np.arange(0, Time_Wash+0.1, 0.1).tolist()
    Times = [round(num, 1) for num in Times]
    #Addition Rates
    r1= 12.75 #(mg/(ml/min**2))
    r2 = 7.47 #(mg/(ml/min**2))
    r3 = 5.56 #(mg/(ml/min**2))
    #Dose
    Ro = 12 #Chlorine dosing period, ever7 12 minutes
    Ro0 = 2 #Minutes duration of dose
    #Time
    Pre_runningT = 0 #Runing time variable
    K0 = 32.3 # free chrolirine demand per min 
    C= 0 # initial #(mg/L) #Concentration of Free Chrloride available
    O = 0  # Initial Oxygen demand
    #Other parameters
    SigC = 1.70*(10**-3) #Natural decay of FC
    BC = 5.38*(10**-4) #Depletion rate of FC in water. 
    A_Per =0
    List_Time_Ints = list(range(Ro,500,Ro))
    List_C=[]
    for i in Times: 
        Running_Time = i
        if(Running_Time in List_Time_Ints):
            A_Per=A_Per+1
        Time_Interval = Running_Time-(Pre_runningT)
        if 0<= Running_Time <= (0+Ro0) :
            Rate = r1
            X = 1
        elif Ro <= Running_Time <= (Ro+Ro0) :
            Rate = r2
            X = 1
        elif 2*Ro <= Running_Time <= (2*Ro+Ro0) : 
            Rate = r3
            X = 1
        elif (A_Per*Ro) <= Running_Time <= (A_Per*Ro+Ro0) : 
            Rate = r3
            X = 1
        else: 
            X = 0
        dO = K0*Time_Interval #Demand per time interval
        O = O+dO # Current oxygen demand
        decay = ((-SigC*Time_Interval)*C) - ((BC*Time_Interval)*O*C)  #Decay due to demand of chlorine
        Increase = (Rate*X*Time_Interval) #increase due to dosing period. 
        dC = decay + Increase #Total chanfe in Free Chlorine
        C = C+dC #FRee Chlorine after set time.
        if C < 0:
            C = 0 
        Pre_runningT = i #Running Time.
        List_C.append(C)
    Cdf = pd.DataFrame(
    {'Time': Times,
     'C': List_C,
    })
    return Cdf


#CFU_Non = (TR(decimal)*(CFU non inoculatred + CFU wash Water))
def Washing_Batch(df, New_water_every_xpacks):
    Contamination_Vector = df['CFU']
    Rangeofiterations = list(range(0,len(Contamination_Vector)))
    if New_water_every_xpacks == 0:
         every_so = []
    else:
        every_so = Rangeofiterations[::New_water_every_xpacks]
    Log_Red_WashW = np.random.uniform(1.87,2.23)
    TrRatetoNI = (1*10**np.random.normal(0.0,0.3))/100 #check this fit
    Cont_Water =0
    for i in range(len(Contamination_Vector)):
        if i in every_so:
            Cont_Water = 0
        print(i)
        Cont =  Contamination_Vector[i]
        if Cont>0:
            New_Cont = Cont*10**-Log_Red_WashW
            Cont_Water = Cont - New_Cont
            Contamination_Vector[i] = New_Cont
        elif Cont ==0:
            Transfer_W_NI = Cont_Water*TrRatetoNI
            New_Cont = Transfer_W_NI
            Cont_Water = Cont_Water -Transfer_W_NI 
            Contamination_Vector[i] = New_Cont
    df["CFU"] = Contamination_Vector
    return df

#Washing

def F_Partitioning_ProcLines(gb3 , NPartitions):
    List_GB3 = []
    for j in gb3:
        if len(j) != 1:
            j = F_Partitioning_W(DF= j,NPartitions= NPartitions) 
            List_GB3.append(j)
        elif len(j) == 1:
            List_GB3.append(j)
    return List_GB3

def F_DF_Clvl(Time):
    List_Wash = []
    Times = list(range(0,Time+1))
    for i in Times:
     C = F_Chloride_lvl (i)
     List_Wash.append(C)
     
    dataTime = {
        "Time": Times,
        "Clvl":List_Wash }
    df_Clvl = pd.DataFrame(dataTime)
    return (df_Clvl)

#F_Chloride_lvl(200)


def F_Washing_ProcLines (List_GB3, Wash_Rate, Cdf):
    for j in List_GB3:
        WashT = len(j.index)
        #DF_Clvl = F_DF_Clvl(WashT)
        
        Times_W = np.arange(0, WashT, 1).tolist()
        Times_W = [round(num, 1) for num in Times_W]
        
        Blw = 0.38 #ml/g min: is the pathogen binding rate to pieces of shredded lettuce heads
        alpha = 0.75#Inactivation rate of pathogen via FC L/mgmin
        V = (3200 *1000) #L #From Luo et al 2012. 
        Rate = Wash_Rate/2.2  #45.45 #kg/min #From Luo et al 2012. 
        Wash_Time = 2.3 #min 
        c1 = 1/Wash_Time #Reciprocal of average time. 
        L = (Rate*1000)/(c1) #g of lettuce in the tak at the same time
        Xl = 0
        Xw =0  #pathogen in process water MPN/ml
        
        L_Xw = []
        L_Xl = []
        for i in Times_W:
            #Defining Initial Contamination
            Time = i
            AvCont = j.at[i,"CFU"] /(j.at[i,"Weight"]*454)
            AvContAfter = AvCont*10**-0.8
            C =   float(Cdf.loc[Cdf['Time'] == Time, 'C'])
            #C= F_Chloride_lvl(Time_Wash= Time)
            Bws = ((AvCont- AvContAfter)*Rate)/V
            CXw = Bws - (Blw*Xw*(L/V)) - (alpha*Xw*C)
            Xw = Xw+CXw
            if Xw<0:
                Xw = 0
            L_Xw.append(Xw)
            Xl = AvCont
            CXl = (Blw*Xw) - (alpha*Xl*C) - (c1*Xl)
            Xl =Xl +CXl
            if Xl < 0:
                Xl = 0
            L_Xl.append(Xl)
            AvCont = Xl
            CFU_2 = AvCont*((j.at[i,"Weight"]*454))
            j.at[i,"CFU"] =  CFU_2
    return (List_GB3) 


#Final Product Case

def Case_Packaging(df,Case_Weight, Pack_Weight):

    Packages_Case = Case_Weight/Pack_Weight
    Total_Packages = len(df.index)
    Total_Cases = Total_Packages/Packages_Case
    Case_Pattern = [i for i in range(1, int(Total_Cases)+1) for _ in range(int(Packages_Case))]
    Crop_No = len(df.index)
    Case_Pattern=Case_Pattern[:Crop_No]
    df.insert(1,"Case",Case_Pattern)
    return df


#OTher Functions

def F_SummingGB2Cont(gb2):
    List_x_Sum=[]  
    for i in gb2:
        x_Sum=i.CFU.sum()
        List_x_Sum.append(x_Sum)
    Out =sum(List_x_Sum)
    return Out


