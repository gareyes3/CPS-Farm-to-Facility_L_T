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
Unique_TestUnit = list(df[Test_Unit].unique())
for i in (Unique_TestUnit):
        for l in range (N_Samp_Unit):
            for j in range(NoGrab):
                Sampled_Grab =df[df[Test_Unit] == i].sample(1, replace= True)
                Index = Sampled_Grab.index
                CFU = Sampled_Grab["CFU"]
                CFU_grab = CFU*(Grab_Weight/(Partition_Weight*454))
                P_Detection=1-math.exp(-CFU_grab)
                if random.uniform(0,1)<P_Detection:
                    Reject_YN=1
                    df.at[Index,"Accept"] = False
                    print(Index)
                
                
                
                

Rejection_Unit = "Sublot"


def F_Rejection_Rule (df, Test_Unit):
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


df_Trial2 = F_Rejection_Rule(df=df, Test_Unit ="Sublot")


