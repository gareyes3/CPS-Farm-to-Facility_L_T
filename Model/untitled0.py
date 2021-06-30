# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 09:03:40 2021

@author: Gustavo Reyes
"""

num, div = 25000, 6.5
print ([num // div + (1 if x < num % div else 0)  for x in range (div)])


    #Contamination Event
    Hazard_lvl = 50000  #CFU # background contamination
    No_Cont_Clusters = 4
    Hazard_lvl_clust = Hazard_lvl/No_Cont_Clusters
    TotalweightAv = sum(df2.Weight)
    ClusterSize = TotalweightAv/No_Cont_Clusters
    No_Cont_ClustersUnits = len(df2.index)
    Hazard_lvl_C= Hazard_lvl/(No_Cont_ClustersUnits*No_Cont_Clusters)
    x_2 =[]
    ClusterIDs = list(df['ClusterID'])
    for i in range(No_Cont_Clusters):
        TrimClusterIDS = ClusterIDs[:len(ClusterIDs)-No_Cont_ClustersUnits]
        n = random.sample(TrimClusterIDS,1)
        n  = n[0]
        x_random_consecutive_rows = ClusterIDs[n:n + No_Cont_ClustersUnits]
        x_2.append(x_random_consecutive_rows)
        ClusterIDs = [x for x in ClusterIDs if x not in x_random_consecutive_rows]
    x_2 =[j for i in x_2 for j in i]
    df.loc[ x_2,'CFU']= df['CFU'] + Ci