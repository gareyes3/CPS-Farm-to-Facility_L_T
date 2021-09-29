# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 11:31:26 2021

@author: gareyes3
"""
import math
import pandas as pd

Niteration = 20
i = 3

data_contprog = {"Initial":[""]*Niteration,
             "Bef Pre-Harvest Samp": [""]*Niteration,
             "Aft Pre-Harvest Samp": [""]*Niteration,
             "Bef Harvest Samp":[""]*Niteration,
             }

df_contprog = pd.DataFrame(data_contprog)

df_contprog.at[i,"Initial"]  =3

[""]*Niteration



Column_Names_Outs = ["Step_CFU_Acc",
                    "Step_CFU_Rej",
                    "Step_CFU_PerR",
                    "Step_Wei_Acc",
                    "Step_Wei_Rej",
                    "Step_Wei_PerR",
                    ]


Column_Names_Progression = ["Initial",
                            "Bef Pre-Harvest Samp",
                            "Aft Pre-Harvest Samp",
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



def Output_DF_Creation(Column_Names, Niterations):
    Outputs_Df =pd.DataFrame("", index= range(Niteration), columns =Column_Names)
    return Outputs_Df



def Output_Collection_Prog(df, outputDF, Step_column,i):
    #df= main model df
    #outputDF = contprogdataframe
    #Step_column = column for the step we are at
    Total_CFU = sum(df.CFU)
    outputDF.at[i,Step_column] = Total_CFU
    return outputDF




def Output_Collection_Final(df, outputDF, Step, Cont_Before, Weight_Before, i):
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
    
    outputDF.columns = outputDF.columns.str.replace("Step", Step) #Updating Head of Columns
    
    return outputDF



df_trial = Output_DF_Creation(Column_Names_Progression, 20)



 
