# -*- coding: utf-8 -*-
#Function Bench



#Adding Contamination to Data Frame
def F_FeedCont(DF,Total_Cont, x_1):
    DF.loc[x_1,'Cont']= Total_Cont
    DF.CFU = (DF.Cont*(DF.Weight*454))
    return (DF)  
                            
 
def F_Sampling(DF, NoSampleLot, sample_size, Limit):
    Results=[]
    for j, row in DF.iterrows():
            Reject_Lis=[]
            for i in range(NoSampleLot):
                Contam = DF.at[j,'ContClus']
                P_Detection=1-math.exp(-Contam*sample_size)
                if random.uniform(0,1)<P_Detection:
                    Reject_YN=1
                else:
                    Reject_YN=0
                Reject_Lis.append(Reject_YN)
            a=sum( Reject_Lis)
            if a > Limit:
                AR= False
            else:
                AR= True
            Results.append(AR)
    return(Results)


#Function to sample whole batch units

def F_Reject_Pallets(DF):
    gg = DF[DF['Accept'] == False]
    List_rejected_lots = gg['SubLotNo'].to_list()    
    DF = (DF[~DF.LotNo.isin(List_rejected_lots)])
    return (DF)


#Palletization Function
def F_Palletization(DF, Pallet_No):
    newdf = pd.concat([DF]*10,axis=0)
    newdf=newdf.sort_values(by=['SubLotNo'])
    Pallet_List=(list(range(1,Pallet_No+1)))
    newdf["PalletNo"] =np.tile(Pallet_List, len(newdf)//Pallet_No)
    newdf = newdf.reset_index(drop=True)  
    newdf.Weight=newdf.Weight/Pallet_No
    newdf.CFU=newdf.CFU/Pallet_No
    newdf = newdf[['Lot', 'SubLotNo','PalletNo','Cont','CFU','Accept', 'Weight']]
    return(newdf)


def F_Packaging(DF, Boxes_Pallet):
    newdf = pd.concat([DF]*10,axis=0)
    newdf=newdf.sort_values(by=['PalletNo','SubLotNo'])
    Pallet_List=(list(range(1,Boxes_Pallet+1)))
    newdf["PackNo"] =np.tile(Pallet_List, len(newdf)//Boxes_Pallet)
    newdf = newdf.reset_index(drop=True)  
    newdf.Weight= newdf.Weight/Boxes_Pallet
    newdf.CFU=newdf.CFU/Boxes_Pallet
    newdf = newdf[['Lot', 'SubLotNo','PalletNo','PackNo','Cont','CFU','Accept', 'Weight']]
    newdf=newdf.sort_values(by=['SubLotNo','PalletNo','PackNo'])
    return(newdf)


def F_SamplingSlots(df, NoSampleLot, sample_size, Cluster_Unit_weight, Limit, Grabs ):
    Results=[]
    Uniquesublots =list(df.Sublot.unique())
    for i in (Uniquesublots):
        Reject_Lis=[]
        for l in range (NoSampleLot):
            Sampled_Grabs =df[df.Sublot == i].sample(Grabs, replace= True)
            Sampled_Grabs =list(Sampled_Grabs.CFU)
            Grab_Weight = sample_size/Grabs
            Detected = []
            for j in Sampled_Grabs: 
                CFU_grab = j*(Grab_Weight/(Cluster_Unit_weight*454))
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
        print(Reject_Lis)
        a=sum(Reject_Lis)
        if a > Limit:
            AR= False
        else:
            AR= True
        Results.append(AR)
        print("Results",Results)
    data1 =  {'slot_number': Uniquesublots,
           'Accept_Reject': Results}
    dT = pd.DataFrame(data1)
    dT= dT.loc[dT['Accept_Reject'] == False]
    ListR= list(dT.slot_number)
    return(ListR)

def F_SamplingPallets (df,NoSamplePallet,sample_size, Cluster_Unit_weight, Limit, Grabs ):
    Results=[]
    UniquePallets=list(df.PalletNo.unique())
    for i in (UniquePallets):
        Reject_Lis=[]
        for l in range (NoSamplePallet):
            Sampled_Grabs =df[df.PalletNo == i].sample(Grabs, replace= True)
            Sampled_Grabs =list(Sampled_Grabs.CFU)
            Grab_Weight = sample_size/Grabs
            Detected = []
            for j in Sampled_Grabs: 
                CFU_grab = j*(Grab_Weight/(Cluster_Unit_weight*454))
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
        print(Reject_Lis)
        a=sum(Reject_Lis)
        if a > Limit:
            AR= False
        else:
            AR= True
        Results.append(AR)
        print("Results",Results)
    data1 =  {'Pallet_No': UniquePallets,
           'Accept_Reject': Results}
    dT = pd.DataFrame(data1)
    dT= dT.loc[dT['Accept_Reject'] == False]
    ListR= list(dT.Pallet_No)
    return(ListR)