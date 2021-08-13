# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:11:53 2021

@author: gareyes3
"""

#Filtering out the rejected lots. 

if ScenCondz.PHS_Int ==1:
    if sum(LL_Rej_Lots_PH)>0:
        df_MeanT = df.iloc[[0]]
        df_MeanT['CFU'] = 0
    df = df[~df['Lot'].isin(LL_Rej_Lots_PH)] 
    if sum(LL_Rej_Lots_PH)>0:
        df= df_MeanT
    
else: 
    df = df[~df['Sublot'].isin(LL_Rej_Lots_PH)]
    
    
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
    
LL_Rej_Lots_PH = [1,6]
        
df_trial = F_Rejection_Rule(df = df, LL_Rej_Lots = LL_Rej_Lots_PH , Test_Unit = "Sublot")


df.loc[:, ['CFU']]=600
df.iloc[0,:]


List1 = [3,4,6]
List2 = [6,3,4,7]

set(List1) <= set(List2)




















import math
import random




























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



Test_Unit = "Lot"
N_Samp_Unit = 10
NoGrab = 60
Samp_Size = 300
Partition_Weight = 100


Unique_TestUnit = list(df[Test_Unit].unique())
for i in (Unique_TestUnit):
    for l in range (N_Samp_Unit):
        Sampled_Grabs =df[df[Test_Unit] == 1].sample(NoGrab, replace= True)
        Grab_Weight = Samp_Size/NoGrab
        Detected = []
        for j, row in  Sampled_Grabs.iterrows():
            CFU = Sampled_Grabs.at[j,"CFU"]
            CFU_grab = CFU*(Grab_Weight/(Partition_Weight*454))
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
        


#New Sampling Function
def F_Sampling_2 (df, Test_Unit, N_Samp_Unit, Samp_Size, Partition_Weight, NoGrab):
    Unique_TestUnit = list(df[Test_Unit].unique())
    Grab_Weight = Samp_Size/NoGrab
    for i in (Unique_TestUnit):
            for l in range (N_Samp_Unit):
                for j in range(NoGrab):
                    Sampled_Grab =df[df[Test_Unit] == i].sample(1, replace= True)
                    Index = Sampled_Grab.index
                    CFU = Sampled_Grab["CFU"]
                    CFU_grab = CFU*(Grab_Weight/(Partition_Weight*454))
                    P_Detection=1-math.exp(-CFU_grab)
                    if random.uniform(0,1)<P_Detection:
                        df.at[Index,"Accept"] = False
    return (df)
                
      
df2 = F_Sampling_2(df =df, 
                   Test_Unit = "Sublot",
                   N_Samp_Unit = 1, 
                   Samp_Size = 300,
                   Partition_Weight = 1000,
                   NoGrab = 60)
                
df2=F_Rejection_Rule(df = df, Test_Unit = "Lot")                

Rejection_Unit = "Sublot"

#New Rejection Function
def F_Rejection_Rule2 (df, Test_Unit):
    #Test_Unit = "Lot" or "Sublot"
    Positives = df[df["Accept"]==False]
    Unique_TestUnit=list(df[Test_Unit].unique())
    Unique_Positives = list(Positives[Test_Unit].unique())
    if set(Unique_TestUnit)<= set(Unique_Positives):
        df_Blank = df.iloc[[0]]
        df_Blank.loc[:, ['CFU']] = 0
        df_Blank.loc[:, ['Weight']] = 0
        df = df_Blank
    else:
        df = df[~df[Test_Unit].isin(Unique_Positives)]
    return df


df_Trial2 = F_Rejection_Rule(df=df, Test_Unit ="Lot")







def F_Growth(DF,Temperature, TimeD ):
    b = 0.023
    Tmin  = 1.335-5.766 *b
    DieoffRate = np.random.triangular(0.0035, 0.013,0.040)
    TotalGrowthRate = (b*(Temperature - Tmin))**(2)
    if Temperature >5:
        Growth  = 1
    else:
        Growth = 0
    if Growth == 1:
        TotalGrowth = (TotalGrowthRate*TimeD)/2.303
    else:
        TotalGrowth  = -DieoffRate * TimeD
    DF['CFU']=DF['CFU']*10**TotalGrowth #Final Growth change CFU/g
    return DF



Time = 5 #hr
Temperature = 10 #C
Lag_Consumed_Prev = 0


#Calculate Lag time at given temperature
def Growth_Function_Lag(DF, Temperature,Time,Lag_Consumed_Prev):
    if Temperature > 5:
        Lag_Time = 7544*(Temperature**-3.11)
        print(Lag_Time)
        Proportion_Lag_Consumed = Time/Lag_Time
        print(Proportion_Lag_Consumed)
        Cummulative_Lag_Consumed = Lag_Consumed_Prev + Proportion_Lag_Consumed
        print(Cummulative_Lag_Consumed)
        if Cummulative_Lag_Consumed < 1: 
            df2 = df
        if Cummulative_Lag_Consumed >1:
            #time not in lag phase
            if Lag_Consumed_Prev < 1:
                PropNotLag =(((Cummulative_Lag_Consumed - 1))/Cummulative_Lag_Consumed)
                print(PropNotLag)
                Growth_Time = Time*PropNotLag
                df2 = F_Growth(DF =df,Temperature = Temperature,TimeD = Growth_Time)
            elif Lag_Consumed_Prev >1:
                Growth_Time = Time
                df2=F_Growth(DF =df,Temperature = Temperature,TimeD = Growth_Time)
            print(Growth_Time)
        Lag_Consumed_Prev = Cummulative_Lag_Consumed
    elif Temperature <5:
        df2=F_Growth(DF =df, Temperature = Temperature, TimeD = Time)
    outputs = [df2,Lag_Consumed_Prev]
    return outputs

     
GrowthOuts = Growth_Function_Lag(DF =df, Temperature = 7, Time = 13, Lag_Consumed_Prev  = Lag_Consumed_Prev)

df2 = GrowthOuts[0]
Lag_Consumed_Prev = GrowthOuts[1]







