# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 13:15:08 2022

@author: gareyes3
"""
#%%
import sys
sys.path
sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility_L_T\Model')
sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility_L_T\Model')
#%%
import numpy as np
import pandas as pd
import random 
import math
from numpy.random import Generator, PCG64
rng = Generator(PCG64())
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import reload 

import time
#Own Libraries
import Funz_T
import Inputz_T
import Scen_T
import MainModel
import DepInputz

import Funz
import T_Inputz
import InFunz
import ContScen
import Dictionariez_T


#%% Contamination progression thruhgout system No Sampling

Inputz_T.Iteration_Number = 1000
Scen_T.Tomatoes_per_sample = 1
Scen_T.Samp_Plan = 0
reload(DepInputz)
Outs_S0 = MainModel.Main_Loop()


#%% Sampling Scenarios
 #Sampling Scenario
Inputz_T.Iteration_Number = 1000
Scen_T.Tomatoes_per_sample = 2
Scen_T.Samp_Plan = 1
reload(DepInputz)
Outs_S1_A = MainModel.Main_Loop()

Inputz_T.Iteration_Number = 1000
Scen_T.Tomatoes_per_sample = 6
Scen_T.Samp_Plan = 1
reload(DepInputz)
Outs_S1_B = MainModel.Main_Loop()

Inputz_T.Iteration_Number = 1000
Scen_T.Tomatoes_per_sample = 100
Scen_T.Samp_Plan = 1
reload(DepInputz)
Outs_S1_C = MainModel.Main_Loop()

#HS

Inputz_T.Iteration_Number = 1000
Scen_T.Tomatoes_per_sample = 2
Scen_T.Samp_Plan = 2
reload(DepInputz)
Outs_S2_A = MainModel.Main_Loop()


Inputz_T.Iteration_Number = 1000
Scen_T.Tomatoes_per_sample = 6
Scen_T.Samp_Plan = 2
reload(DepInputz)
Outs_S2_B = MainModel.Main_Loop()

Inputz_T.Iteration_Number = 1000
Scen_T.Tomatoes_per_sample = 100
Scen_T.Samp_Plan = 2
reload(DepInputz)
Outs_S2_C = MainModel.Main_Loop()

#RS

Inputz_T.Iteration_Number = 1000
Scen_T.Tomatoes_per_sample = 2
Scen_T.Samp_Plan = 3
reload(DepInputz)
Outs_S3_A = MainModel.Main_Loop()


Inputz_T.Iteration_Number = 1000
Scen_T.Tomatoes_per_sample = 6
Scen_T.Samp_Plan = 3
reload(DepInputz)
Outs_S3_B = MainModel.Main_Loop()

Inputz_T.Iteration_Number = 1000
Scen_T.Tomatoes_per_sample = 100
Scen_T.Samp_Plan = 3
reload(DepInputz)
Outs_S3_C = MainModel.Main_Loop()

#FPS

Inputz_T.Iteration_Number = 1000
Scen_T.Tomatoes_per_sample = 2
Scen_T.Samp_Plan = 4
reload(DepInputz)
Outs_S4_A = MainModel.Main_Loop()


Inputz_T.Iteration_Number = 1000
Scen_T.Tomatoes_per_sample = 6
Scen_T.Samp_Plan = 4
reload(DepInputz)
Outs_S4_B = MainModel.Main_Loop()

Inputz_T.Iteration_Number = 1000
Scen_T.Tomatoes_per_sample = 100
Scen_T.Samp_Plan = 4
reload(DepInputz)
Outs_S4_C = MainModel.Main_Loop()


### Bird Cont
Inputz_T.Iteration_Number = 500
Scen_T.Tomatoes_per_sample = 100
Scen_T.Samp_Plan = 1
Scen_T.Cont_Scenario = 2
reload(DepInputz)
Outs_S4_C = MainModel.Main_Loop()

#%%
#Saving Dfs
S0_0_MainOut = Outs_S0[0]

S1_A_MainOut = Outs_S1_A[0]
S1_B_MainOut = Outs_S1_B[0]
S1_C_MainOut = Outs_S1_C[0]

S2_A_MainOut = Outs_S2_A[0]
S2_B_MainOut = Outs_S2_B[0]
S2_C_MainOut = Outs_S2_C[0]

S3_A_MainOut = Outs_S3_A[0]
S3_B_MainOut = Outs_S3_B[0]
S3_C_MainOut = Outs_S3_C[0]

S4_A_MainOut = Outs_S4_A[0]
S4_B_MainOut = Outs_S4_B[0]
S4_C_MainOut = Outs_S4_C[0]

#Analysis
def Get_Power(df, Weight_After, Weight_Before, CFU_avail): 
    Total_Rej = sum((df[Weight_After]-df[Weight_Before])>0 )
    Total_Avail = (sum(df[ CFU_avail]>0))
    Power =  sum((df[Weight_After]-df[Weight_Before])>0 )/ (sum(df[ CFU_avail]>0))
    return [Total_Rej,Total_Avail,Power]


def get_powers_scenarios (df):
    A=Get_Power(df = df, 
              Weight_After = "PHS 1 Weight Rejected Aft", 
              Weight_Before = "PHS 1 Weight Rejected Bef", 
              CFU_avail = "CFU_Avail Pick 1"
              )

    B=Get_Power(df = df, 
              Weight_After = "PHS 2 Weight Rejected Aft", 
              Weight_Before = "PHS 2 Weight Rejected Bef", 
              CFU_avail = "CFU_Avail Pick 2"
              )

    C= Get_Power(df = df, 
              Weight_After = "PHS 3 Weight Rejected Aft", 
              Weight_Before = "PHS 3 Weight Rejected Bef", 
              CFU_avail = "CFU_Avail Pick 3"
              )
    return [A,B,C]




#Getting contmaination at sampling points ======================================
df_locations = pd.DataFrame({
    "Pick 1": S1_A_MainOut["CFU_Bef_Pick1PHS"],
    "Pick 2": S1_A_MainOut["CFU_Bef_Pick2PHS"],
    "Pick 3": S1_A_MainOut["CFU_Bef_Pick3PHS"],
    })

df_locations_melted=df_locations.melt()

p=sns.boxplot(data = df_locations_melted, 
            x = "variable",
            y = "value"
            )
p.set_xlabel("PHS per Pick")
p.set_ylabel("TAC available at sampling point")

df_powers = pd.DataFrame({
    "PHS Pick 1":[ 0.02894736842105263],
    "PHS Pick 2": [0.065439672801636],
    "PHS Pick 3": [0.07439824945295405],
    })

df_power_melted = df_powers.melt()


sns.barplot(data = df_power_melted, 
            x = "variable",
            y = "value")


#=================================

sns.boxplot(y=S1_A_MainOut["CFU_Bef_Pick3PHS"] ) 


Total_Exposure = sum(S1_A_MainOut["Total CFU"])

def get_powers_scenarios (df):
    A=Get_Power(df = df, 
              Weight_After = "PHS 1 Weight Rejected Aft", 
              Weight_Before = "PHS 1 Weight Rejected Bef", 
              CFU_avail = "CFU_Avail Pick 1"
              )

    B=Get_Power(df = df, 
              Weight_After = "PHS 2 Weight Rejected Aft", 
              Weight_Before = "PHS 2 Weight Rejected Bef", 
              CFU_avail = "CFU_Avail Pick 2"
              )

    C= Get_Power(df = df, 
              Weight_After = "PHS 3 Weight Rejected Aft", 
              Weight_Before = "PHS 3 Weight Rejected Bef", 
              CFU_avail = "CFU_Avail Pick 3"
              )
    return [A,B,C]

    

#Power For Scenario 1

get_powers_scenarios (df=S1_A_MainOut)
#Power For Scenario 2
get_powers_scenarios (df=S1_B_MainOut)

#Power For Scenario 3
get_powers_scenarios (df=S1_C_MainOut)

#Power For Scenario 4

get_powers_scenarios (df=S2_A_MainOut)

#Power For Scenario 5
get_powers_scenarios (df=S2_B_MainOut)

#Power For Scenario 6
get_powers_scenarios (df=S2_C_MainOut)

#Power For Scenario 7

get_powers_scenarios (df=S3_A_MainOut)

#Power For Scenario 8
get_powers_scenarios (df=S3_B_MainOut)

#Power For Scenario 9
get_powers_scenarios (df=S3_C_MainOut)

#Power For Scenario 10

get_powers_scenarios (df=S4_A_MainOut)

#Power For Scenario 11

get_powers_scenarios (df=S4_B_MainOut)

#Power For Scenario 12

get_powers_scenarios (df=S4_C_MainOut)


Powers_Summary_DF = pd

#%%
##Contamination at sampling points

def Get_Contam_Sampling(df, Type, Mass):
    A=pd.DataFrame({"Cont":df["CFU_Avail Pick 1"],
                  "Pick": 1,
                  "Type" : Type,
                  "Mass": Mass
                  })
    B=pd.DataFrame({"Cont":df["CFU_Avail Pick 2"],
                  "Pick": 2,
                  "Type" : Type,
                  "Mass": Mass
                  })
    C=pd.DataFrame({"Cont":df["CFU_Avail Pick 3"],
                  "Pick": 3,
                  "Type" : Type,
                  "Mass": Mass
                  })
    Dfout = pd.concat([A,B,C])
    return (Dfout)
    
S1_A_Contam=Get_Contam_Sampling(df = S1_A_MainOut, Type = "PH",Mass = "1 Tomato")
S1_B_Contam=Get_Contam_Sampling(df = S1_B_MainOut, Type = "PH",Mass = "5 Tomato")
S1_C_Contam=Get_Contam_Sampling(df = S1_C_MainOut, Type = "PH",Mass = "20 X 5 Tomato")

S2_A_Contam=Get_Contam_Sampling(df = S2_A_MainOut, Type = "HS",Mass = "1 Tomato")
S2_B_Contam=Get_Contam_Sampling(df = S2_B_MainOut, Type = "HS",Mass = "5 Tomato")
S2_C_Contam=Get_Contam_Sampling(df = S2_C_MainOut, Type = "HS",Mass = "20 X 5 Tomato")

S3_A_Contam=Get_Contam_Sampling(df = S3_A_MainOut, Type = "RS",Mass = "1 Tomato")
S3_B_Contam=Get_Contam_Sampling(df = S3_B_MainOut, Type = "RS",Mass = "5 Tomato")
S3_C_Contam=Get_Contam_Sampling(df = S3_C_MainOut, Type = "RS",Mass = "20 X 5 Tomato")


S4_A_Contam=Get_Contam_Sampling(df = S4_A_MainOut, Type = "PPS",Mass = "1 Tomato")
S4_B_Contam=Get_Contam_Sampling(df = S4_B_MainOut, Type = "PPS",Mass = "5 Tomato")
S4_C_Contam=Get_Contam_Sampling(df = S4_C_MainOut, Type = "PPS",Mass = "20 X 5 Tomato")


Cont_Samp_Point = pd.concat([S1_A_Contam,S1_B_Contam,S1_C_Contam,
                             S2_A_Contam,S2_B_Contam,S2_C_Contam,
                             S3_A_Contam,S3_B_Contam,S3_C_Contam,
                             S4_A_Contam,S4_B_Contam,S4_C_Contam])

Cont_Samp_Point.to_csv(path_or_buf = "C:\\Users\\Gustavo Reyes\\Documents\\GitHubFiles\\CPS-Farm-to-Facility_L_T\\Model\\Data_Tomato_Outputs\\Cont_Samp_Point.csv")

#%% Contamination Progression. 
Baseline_Melted_A = Outs_S0[1].melt()
Baseline_Melted_B = Outs_S0[1].melt()
Baseline_Melted_C = Outs_S0[1].melt()
Baseline_Melted_A["Plan"] = "Baseline No Sampling"
Baseline_Melted_A["Plan Mass"] = "A"
Baseline_Melted_B["Plan"] = "Baseline No Sampling"
Baseline_Melted_B["Plan Mass"] = "B"
Baseline_Melted_C["Plan"] = "Baseline No Sampling"
Baseline_Melted_C["Plan Mass"] = "C"


S1_A_Melted = Outs_S1_A[1].melt()
S1_B_Melted = Outs_S1_B[1].melt()
S1_C_Melted = Outs_S1_C[1].melt()

S1_A_Melted["Plan"] = "PH"
S1_A_Melted["Plan Mass"] = "A"
S1_B_Melted["Plan"] = "PH"
S1_B_Melted["Plan Mass"] = "B"
S1_C_Melted["Plan"] = "PH"
S1_C_Melted["Plan Mass"] = "C"
#----
S2_A_Melted = Outs_S2_A[1].melt()
S2_B_Melted = Outs_S2_B[1].melt()
S2_C_Melted = Outs_S2_C[1].melt()

S2_A_Melted["Plan"] = "HS"
S2_A_Melted["Plan Mass"] = "A"
S2_B_Melted["Plan"] = "HS"
S2_B_Melted["Plan Mass"] = "B"
S2_C_Melted["Plan"] = "HS"
S2_C_Melted["Plan Mass"] = "C"
#---

S3_A_Melted = Outs_S3_A[1].melt()
S3_B_Melted = Outs_S3_B[1].melt()
S3_C_Melted = Outs_S3_C[1].melt()

S3_A_Melted["Plan"] = "RS"
S3_A_Melted["Plan Mass"] = "A"
S3_B_Melted["Plan"] = "RS"
S3_B_Melted["Plan Mass"] = "B"
S3_C_Melted["Plan"] = "RS"
S3_C_Melted["Plan Mass"] = "C"
#---
S4_A_Melted = Outs_S4_A[1].melt()
S4_B_Melted = Outs_S4_B[1].melt()
S4_C_Melted = Outs_S4_C[1].melt()

S4_A_Melted["Plan"] = "PPS"
S4_A_Melted["Plan Mass"] = "A"
S4_B_Melted["Plan"] = "PPS"
S4_B_Melted["Plan Mass"] = "B"
S4_C_Melted["Plan"] = "PPS"
S4_C_Melted["Plan Mass"] = "C"


T100_Binded=pd.concat([
    Baseline_Melted_A,S1_A_Melted, S2_A_Melted,S3_A_Melted, S4_A_Melted,
    Baseline_Melted_B,S1_B_Melted, S2_B_Melted,S3_B_Melted, S4_B_Melted,
    Baseline_Melted_C,S1_C_Melted, S2_C_Melted,S3_C_Melted, S4_C_Melted])
#T100_Binded.to_csv(path_or_buf = "C:\\Users\\gareyes3\\Documents\\GitHub\\CPS-Farm-to-Facility_L_T\\Model\\Data_Tomato_Outputs\\Cont_Prog.csv")

T100_Binded.to_csv(path_or_buf = "C:\\Users\\Gustavo Reyes\\Documents\\GitHubFiles\\CPS-Farm-to-Facility_L_T\\Model\\Data_Tomato_Outputs\\Cont_Prog.csv")

sns.lineplot(data = Baseline_Melted_A , x = "variable", y = "value")
sns.lineplot(data = S1_C_Melted , x = "variable",y = "value")
sns.lineplot(data = S2_C_Melted , x = "variable",y = "value")
sns.lineplot(data = S3_C_Melted , x = "variable",y = "value")
sns.lineplot(data = S4_C_Melted , x = "variable",y = "value")


sns.lineplot(data = S1_A_Melted , x = "variable", y = "value")
sns.lineplot(data = S1_B_Melted , x = "variable", y = "value")
sns.lineplot(data = S1_C_Melted , x = "variable",y = "value")

sns.lineplot(data = S2_A_Melted , x = "variable", y = "value")
sns.lineplot(data = S2_B_Melted , x = "variable", y = "value")
sns.lineplot(data = S2_C_Melted , x = "variable",y = "value")

#%% Consumer Exposure

S0_0_Exp = sum(S0_0_MainOut["Total CFU"])

S1_A_Exp=sum(S1_A_MainOut["Total CFU"])
S1_B_Exp=sum(S1_B_MainOut["Total CFU"])
S1_C_Exp=sum(S1_C_MainOut["Total CFU"])

S2_A_Exp=sum(S2_A_MainOut["Total CFU"])
S2_B_Exp=sum(S2_B_MainOut["Total CFU"])
S2_C_Exp=sum(S2_C_MainOut["Total CFU"])

S3_A_Exp=sum(S3_A_MainOut["Total CFU"])
S3_B_Exp=sum(S3_B_MainOut["Total CFU"])
S3_C_Exp=sum(S3_C_MainOut["Total CFU"])

S4_A_Exp=sum(S4_A_MainOut["Total CFU"])
S4_B_Exp=sum(S4_B_MainOut["Total CFU"])
S4_C_Exp=sum(S4_C_MainOut["Total CFU"])

Exps = [S0_0_Exp,S1_A_Exp,S1_B_Exp,S1_C_Exp,S2_A_Exp,S2_B_Exp,S2_C_Exp,S3_A_Exp,S3_B_Exp,S3_C_Exp,S4_A_Exp,S4_B_Exp,S4_C_Exp]

Exps_Emp=[]
for i in range(0,len(Exps)):
    A = Exps[i]/Exps[0]
    Exps_Emp.append(A)
Exps_Emp

Exp_Main_Df =pd.DataFrame({
    "Exposure": Exps,
    "Relative": Exps_Emp
    })

#%%
Inproc_Prog_S0_0 = Outs_S0[4]
Inproc_Prog_S0_0_M=Inproc_Prog_S0_0.melt()

Inproc_Prog_S1_B = Outs_S1_B[4]
Inproc_Prog_S1_B_M=Inproc_Prog_S1_B.melt()

sns.lineplot(data = Inproc_Prog_S1_B_M , x = "variable", y = "value")
plt.xticks(rotation=90)