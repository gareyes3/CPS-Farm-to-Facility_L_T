# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 11:31:26 2021

@author: gareyes3
"""
import math
import pandas as pd
import numpy as np


Column_Names_Outs = ["Step_CFU_Acc",
                    "Step_CFU_Rej",
                    "Step_CFU_PerR",
                    "Step_Wei_Acc",
                    "Step_Wei_Rej",
                    "Step_Wei_PerR",
                    ]


Column_Names_Progression = ["Contam Event Before PHS",
                            "Bef Pre-Harvest Samp",
                            "Aft Pre-Harvest Samp",
                            "Contam Event After PHS",
                            "Bef Harvest Samp",
                            "Aft Harvest Samp",
                            "Bef Receiving Samp",
                            "After Receiving Samp",
                            "Bef Shredding",
                            "Bef Conveyor Belt",
                            "Bef Washing",
                            "Bef Shaker Table",
                            "Bef Centrifuge",
                            "Aft Value Addition",
                            "Bef Final Prod S",
                            "Final Product Facility"
                            ]

Column_Per_Contaminated = ["PropCont_CE_B_PHS",
                            "PropCont_B_PHS",
                            "PropCont_A_PHS",
                            "PropCont_CE_A_PHS",
                            "PropCont_B_HS",
                            "PropCont_A_PHS",
                            "PropCont_B_RS",
                            "PropCont_A_RS",
                            "PropCont_B_Shredding",
                            "PropCont_B_CBelt",
                            "PropCont_B_Washing",
                            "PropCont_B_ST",
                            "PropCont_B_Cent",
                            "PropCont_A_VA",
                            "PropCont_B_FPS",
                            "PropCont_B_FP"
    ]



def Output_DF_Creation(Column_Names, Niterations):
    Outputs_Df =pd.DataFrame(np.NaN, index= range(Niterations), columns =Column_Names)
    return Outputs_Df



def Output_Collection_Prog(df, outputDF, Step_Column,i):
    #df= main model df
    #outputDF = contprogdataframe
    #Step_column = column for the step we are at
    Total_CFU = sum(df.CFU)
    outputDF.at[i,Step_Column] = Total_CFU
    return outputDF

def Pop_Output_Colection(df, outputDF, Step_Column, i):
    Pop  = df[df.CFU>0]
    TotalPop = len(Pop)
    Total_whole = len(df.CFU)
    Pop_Final = TotalPop /Total_whole
    outputDF.at[i,Step_Column] =  Pop_Final
    return outputDF

#df.CFU=np.random.uniform(0,1,2000)
#df.CFU[1] = 0

def Output_Collection_Final(df, outputDF, Step, Cont_Before, Weight_Before, i, Niterations):
    #Contaminations
    Cont_Acc = sum(df.CFU)
    Cont_Rej = Cont_Before-Cont_Acc
    if Cont_Acc == 0:
        Cont_PerR = 1
    else:
        Cont_PerR = Cont_Rej/(Cont_Acc+Cont_Rej) #Percentage Rejected by Finished product sampling
    #Weight
    Wei_Acc = sum(df.Weight)
    Wei_Rej = Weight_Before-Wei_Acc
    Wei_PerR =  Wei_Rej/(Wei_Rej+Wei_Acc)
    
    outputDF.at[i,"Step_CFU_Acc"] = Cont_Acc
    outputDF.at[i,"Step_CFU_Rej"] = Cont_Rej
    outputDF.at[i,"Step_CFU_PerR"] = Cont_PerR
    outputDF.at[i,"Step_Wei_Acc"] = Wei_Acc
    outputDF.at[i,"Step_Wei_Rej"] = Wei_Rej
    outputDF.at[i,"Step_Wei_PerR"] = Wei_PerR
    if i == Niterations -1:
        outputDF.columns = outputDF.columns.str.replace("Step", Step) #Updating Head of Columns Change column end iteration.
    
    return outputDF




'''
df_prog = Output_DF_Creation(Column_Names =Column_Names_Progression, Niterations =20)
df_outs = Output_DF_Creation(Column_Names =Column_Names_Outs, Niterations =20)


df_prog = Output_Collection_Prog(df = df,
                                outputDF = df_prog,
                                Step_Column = "Bef Pre-Harvest Samp", 
                                i =11 )


ContBEf = 10000
weightBEf = 100000
df_outs = Output_Collection_Final(df = df, 
                                outputDF = df_outs, 
                                Step = "PH", 
                                Cont_Before = 10000, 
                                Weight_Before =1000000, 
                                i = 10, 
                                Niterations = 20)

'''