# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 08:31:43 2022

@author: gareyes3
"""

#Determining the effect of chlorine wash: 
    
#Random contmaination. No_Intervention.     

difference_wash = (Baseline_NI_Wash_1[1]["Bef Washing"] - Baseline_NI_Wash_1[1]["Bef Shaker Table"] )
difference_wash=difference_wash[difference_wash!=0] #removing 0 values
np.log10(difference_wash).describe()


difference_wash = (Baseline_AI_1[1]["Bef Washing"] - Baseline_AI_1[1]["Bef Shaker Table"] )
difference_wash=difference_wash[difference_wash!=0] #removing 0 values
np.log10(difference_wash).describe()


difference_wash = (Baseline_AI_1_5ppm[1]["Bef Washing"] - Baseline_AI_1_5ppm[1]["Bef Shaker Table"] )
difference_wash=difference_wash[difference_wash!=0] #removing 0 values
np.log10(difference_wash).describe()

difference_wash = (Baseline_AI_1_10ppm[1]["Bef Washing"] - Baseline_AI_1_10ppm[1]["Bef Shaker Table"] )
difference_wash=difference_wash[difference_wash!=0] #removing 0 values
np.log10(difference_wash).describe()


difference_wash = (Baseline_AI_1_20ppm[1]["Bef Washing"] - Baseline_AI_1_20ppm[1]["Bef Shaker Table"] )
difference_wash=difference_wash[difference_wash!=0] #removing 0 values
np.log10(difference_wash).describe()

difference_wash = (Baseline_AI_1_0ppm[1]["Bef Washing"] - Baseline_AI_1_0ppm[1]["Bef Shaker Table"] )
difference_wash=difference_wash[difference_wash!=0] #removing 0 values
np.log10(difference_wash).describe()

difference_wash = (Baseline_AI_1_False[1]["Bef Washing"] - Baseline_AI_1_False[1]["Bef Shaker Table"] )
difference_wash=difference_wash[difference_wash!=0] #removing 0 values
np.log10(difference_wash).describe()


Changes_1=np.log10(Baseline_NI_Wash_1[1]["Bef Washing"]/Baseline_NI_Wash_1[1]["Bef Shaker Table"]).describe()

Baseline_NI_Wash_1[1]=Baseline_NI_Wash_1[1][Baseline_NI_Wash_1[1]["Bef Washing"]!=0]
Baseline_NI_Wash_1[1]["Bef Shaker Table"][Baseline_NI_Wash_1[1]["Bef Shaker Table"] == 0] = 0.001

(10**4.9) *(1-0.055)*(2.3/(3.2*10**6))
