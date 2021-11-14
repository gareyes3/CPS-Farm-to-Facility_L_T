# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 21:06:24 2021

@author: reyes
"""
import seaborn as sns
import pandas as pd


def Create_Boxplot(Data,Column):
    sns.set_theme(style="whitegrid")
    ax = sns.boxplot(x=Column, data=Data)
    ax = sns.swarmplot(x=Column, data=Data, color=".25")
    ax.set( ylabel='% CFU Rejected (Power)')
    
    return ax


def melting_type(df, typename):
    df_melt = pd.melt(df)
    df_melt["type"] = typename
    return df_melt
    
    