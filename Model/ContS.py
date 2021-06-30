# -*- coding: utf-8 -*-
import pandas as pd 
import numpy as np
import itertools
import scipy.stats as stats
import math
import os
import random
import seaborn as sns
from matplotlib import pyplot as plt
import Funz

#%% Contamination Scenarios

def F_Background_C(df, Hazard_lvl, Partition_Units):
    Ci = Hazard_lvl/Partition_Units
    df.CFU =Ci
    return df

def F_Point_Source_C (df, Hazard_lvl, No_Cont_Clusters, Cluster_Size, Partition_Weight):
    No_Cont_ClustersUnits = int(Cluster_Size/Partition_Weight) #Cluster Units per Contaminatrion Cluster
    Hazard_lvl_C= Hazard_lvl/No_Cont_Clusters
    Ci = Hazard_lvl_C
    X_1= df.sample(No_Cont_Clusters)
    X_1 = list(X_1.ClusterID)
    df.loc[X_1,'CFU']= df['CFU'] + Ci
    return df
    
def F_systematic_C(df, Hazard_lvl,No_Cont_ClustersUnits,No_Cont_Clusters,Cluster_Size, Partition_Weight ):
    No_Cont_ClustersUnits = int(Cluster_Size/Partition_Weight)
    Hazard_lvl_C= Hazard_lvl/(No_Cont_ClustersUnits*No_Cont_Clusters)
    Ci = Hazard_lvl_C
    n = random.randint(0,len(df.index)- No_Cont_ClustersUnits)
    x_random_consecutive_rows = df[n:n + No_Cont_ClustersUnits]
    x_random_consecutive_rows = list(x_random_consecutive_rows['ClusterID'])
    df.loc[ x_random_consecutive_rows,'CFU']= df['CFU'] + Ci
    return df
        
