# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 13:14:43 2022

@author: gareyes3
"""

 #%%

Field_df.loc[list(range(3,200)), "CFU" ] = 1000
Field_df.loc[list(range(3,500)), "Location" ] = 2


def F_CrossContProLine_tom (df, Tr_P_S, Tr_S_P, Sanitation_Freq_lb = 0, StepEff = 0 , compliance = 0 ):
        df_field_1 =df.loc[df["Location"]==2].copy()
        rateweight = 0.54
        every_x_many = int(Sanitation_Freq_lb/rateweight)
        ContS=0
        vectorCFU = df_field_1["CFU"].copy()
        newvector=[]
        if every_x_many > 0:
            Cleaning_steps = np.arange(0, len(vectorCFU) , every_x_many )
        for i in list(vectorCFU.index):
            if random.uniform(0,1)<compliance:
                if every_x_many > 0:
                    if i in Cleaning_steps:
                        ContS = ContS*10**StepEff
                        print ("cleaned")
            ContP = vectorCFU[i] #Contamination product
            TotTr_P_S= rng.binomial(ContP,Tr_P_S) #Transfer from Product to Surfaces
            TotTr_S_P = rng.binomial(ContS,Tr_S_P) #Trasnfer from Surfaves to product
            ContPNew = ContP-TotTr_P_S+TotTr_S_P #New Contmination on Product
            ContS=ContS+TotTr_P_S-TotTr_S_P #Remiining Contamination in Surface for upcoming batches
            newvector.append(ContPNew)
        df_field_1.loc[:,"CFU"] = newvector
        df.update(df_field_1)
        return df
    
    
        
    
def Case_Packaging(df,Case_Weight,Tomato_Weight):
    
    df_field_1 =df.loc[df["Location"]==2].copy()
    
    Tomatoes_Case = math.ceil(Case_Weight/Tomato_Weight)
    Total_Packages = len(df_field_1.index)
    Total_Cases = math.ceil(Total_Packages/Tomatoes_Case)
    Case_Pattern = [i for i in range(1, int(Total_Cases)+1) for _ in range(Tomatoes_Case)]
    Crop_No = len(df_field_1.index)
    Case_Pattern=Case_Pattern[:Crop_No]
    print(Case_Pattern)
    df_field_1.loc[:,"Case_PH"] = Case_Pattern
    
    df.update(df_field_1)
    return df

df3 = Case_Packaging(df = Field_df,Case_Weight = 20,Tomato_Weight = 0.54)
#%%
#Experimenntal Plots
DC_Cont_Day_Melted = DC_Cont_Day.melt()
p=sns.pointplot(data=DC_Cont_Day_Melted, x="variable", y="value")
p.set_xlabel("Days in System", fontsize = 12)
p.set_ylabel("Total Adulterant Cells in System", fontsize = 12)

Contam_Bin = random.sample(list(range(1,Total_Bins+1)),1)[0]


DC_Cont_Day_Pick1_Melted = DC_Cont_Day_Pick1.melt()
DC_Cont_Day_Pick1_Melted["Pick_ID"] = 1
DC_Cont_Day_Pick2_Melted = DC_Cont_Day_Pick2.melt()
DC_Cont_Day_Pick2_Melted["Pick_ID"] = 2
DC_Cont_Day_Pick3_Melted = DC_Cont_Day_Pick3.melt()
DC_Cont_Day_Pick3_Melted["Pick_ID"] = 3

DC_Cont_Day_Combined=pd.concat([DC_Cont_Day_Pick1_Melted,DC_Cont_Day_Pick2_Melted,DC_Cont_Day_Pick3_Melted])
DC_Cont_Day_Combined=DC_Cont_Day_Combined.reset_index()

p=sns.lineplot(data=DC_Cont_Day_Combined, x="variable", y="value", hue = "Pick_ID")
p.set_xlabel("Days in System", fontsize = 12)
p.set_ylabel("Total Adulterant Cells in System", fontsize = 12)
plt.xticks(rotation=90)
plt.axvline(11, color='red', alpha = 0.5)
plt.axvline(25, color='red', alpha = 0.5)
plt.axvline(39, color='red', alpha = 0.5)


######### Summary_Exposure
#Power_PER_Pick


def Get_Power(df, Weight_After, Weight_Before, CFU_avail): 
  return  sum((df[Weight_After]-df[Weight_Before])>0 )/ (sum(df[ CFU_avail]>0))

Total_Exposure = sum(DC_Exp["Total CFU"])

Get_Power(df = DC_Exp, 
          Weight_After = "PHS 3 Weight Rejected Aft", 
          Weight_Before = "PHS 3 Weight Rejected Bef", 
          CFU_avail = "CFU_Avail Pick 3"
          )

########






Field_df.loc[(Field_df["Pick_ID"] ==1) & (Field_df["Harvester"] == 1 )]

Field_df =Bin_Cont_Function(df = Field_df,
                        Hazard_Level = 100_000, 
                        Pick_No =1  , 
                        Cont_Bin_No = Contam_Bin)

#### Function Change Location
def Update_Location(df, Previous, NewLoc):
    df_field_1 =df.loc[df["Location"]==Previous].copy()
    df_field_1.loc[:,"Location"] =NewLoc
    df.update(df_field_1)
    return df

Update_Location(df= Field_df, Previous = 2, NewLoc =3)


###

def F_Sampling_T (df, Pick_No, Location, NSamp_Unit, NoGrab):
    
    df_field_1 =df.loc[(df["Pick_ID"]==Pick_No) & (df["Location"]==Location)].copy()
    
    #Unique_TestUnit = list(df[Test_Unit].unique())
    #Grab_Weight = Partition_Weight #In lb
    #for i in (Unique_TestUnit): #From sublot 1 to sublot n (same for pallet,lot,case etc)
    for l in range (1, NSamp_Unit+1): #Number of samples per sublot or lot or pallet.
        for j in range(NoGrab):
            CFU_hh=df_field_1["CFU"]
            List_Random=CFU_hh.sample(n=1)
            CFU = List_Random
            Index = List_Random.index[0]
            CFU_grab = CFU#*(Grab_Weight/(Partition_Weight*454))
            P_Detection=1-math.exp(-CFU_grab)
            RandomUnif = random.uniform(0,1)
            if RandomUnif < P_Detection:
                df_field_1.at[Index, 'PositiveSamples'].append(l)
    df.update(df_field_1)
    return (df)


def F_Rejection_Rule_T (df, Pick_No, Av_Picks, Test_Unit, limit):
    #Unique_Test_Unit =list(df[Test_Unit].unique())
    df_field_1 =df.loc[(df["Pick_ID"].isin(Av_Picks))].copy()
    Reject = []
    #for  i in Unique_Test_Unit:
    df_Subset = df_field_1[df_field_1[Test_Unit] == Pick_No].copy()
    List_of_grabs = df_Subset['PositiveSamples'].tolist()
    flat_list = [item for sublist in  List_of_grabs for item in sublist]
    Unique_Positives =list(np.unique(flat_list))
    if len(Unique_Positives)>limit:
        Reject.append(i)
    df_field_1.PositiveSamples = [list() for x in range(len(df_field_1.index))] #this is in case everything gets rejected
    if len(Reject)>0:
     df_field_1.loc[:,"Rej_Acc"] = "REJ"
        #df_Blank = df.iloc[[0]]
        #df_Blank.loc[:, ['CFU']] = 0
        #df_Blank.loc[:, ['Weight']] = SCInputz.Partition_Weight
        #df_Blank.loc[:, ['Accept']] = "All Rej"
        #df = df_Blank
    #else:
        #df = df[~df[Test_Unit].isin(Reject)]
    df.update(df_field_1)
    return df

Field_df=pd.DataFrame({"Tomato_ID": Individual_Tomatoes,
                       "Plant_ID": Individual_Plants[0:Individual_Tomatoes.size],
                       "Pick_ID": Pick_Random[0:Individual_Tomatoes.size],
                       "Weight": Tomato_weight,
                       "Harvester" : 0,
                       "Bucket":0,
                       "Bin": 0,
                       "Case_PH": 0,
                       "CFU": 0,
                       "Location": 1,
                       'PositiveSamples':"",
                       "Rej_Acc" :"Acc"
                  })
Field_df.PositiveSamples = [list() for x in range(len(Field_df.index))]

Field_df.loc[1:2500:,"CFU"] =10

F_Sampling_T (df= Field_df, 
              Pick_No = 2, 
              Location = 1, 
              NSamp_Unit = 1, 
              NoGrab =80 )

F_Rejection_Rule_T (df = Field_df, 
                    Pick_No = 2, Av_Picks= [2,3], 
                    Test_Unit = "Pick_ID", 
                    limit = 0)

df_field_1 =Field_df.loc[(Field_df["Pick_ID"]==Pick_No) & (Field_df["Location"]==Location)].copy()

df_field_1.index[4]

CFU_hh.sample(n=1).index[0]

list(range(1,3+1))

Field_df.loc[(Field_df["Pick_ID"].isin([1,2]))]

aaaa= Field_df.loc[(Field_df['Pick_ID']==1) & (Field_df['Rej_Acc']== "Acc") ].copy()
aaaa["CFU"].sum()

len([])

P_Detection=1-math.exp(-2)
len(aaaa)
