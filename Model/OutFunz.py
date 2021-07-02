# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 09:46:17 2021

@author: Gustavo Reyes
"""

import pandas as pd

def F_Melting(df, Scenario):
    X_df_contprog2= pd.melt(df)
    X_df_contprog2["Scenario"] = Scenario
    return X_df_contprog2