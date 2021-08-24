# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 10:30:57 2021

@author: Gustavo Reyes
"""

import pandas as pd

def F_InDF (Partition_Units,Field_Weight,slot_number ):
    #Parition_Units = Partition Units, 
    #Field_Weight = Weight of Field
    #Slot_number = Number of Sublots
    data = {'Lot': 1, #Field
            'Sublot':0, #Sublots
            'PartitionID': list(range(1,Partition_Units+1)), #Paritition
            'CFU':0, #CFU Pathogen
            'Grabs':"",
            "Positives":"",
            'Accept': True, #Accepted of Rejected
            'Weight': Field_Weight/Partition_Units} #Weight per Partition
    
    Sublot_Pattern = [i for i in range(1, slot_number+1) for _ in range(int(Partition_Units/slot_number))] #Pattern of Sublots
    df = pd.DataFrame(data)
    df.Sublot = Sublot_Pattern
    df.index = range(1,Partition_Units+1)
    df.Grabs = [list() for x in range(len(df.index))]
    return df






