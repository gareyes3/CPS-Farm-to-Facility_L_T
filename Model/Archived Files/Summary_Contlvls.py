# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 14:44:21 2021

@author: gareyes3
"""


#PreHarvest 4D
exec(open("MainModel2.0.py").read())
FiftyK_PH_PR = Out_PH4d_PercRej

exec(open("MainModel2.0.py").read())
TenK_PH_PR = Out_PH4d_PercRej

exec(open("MainModel2.0.py").read())
FiveK_PH_PR = Out_PH4d_PercRej

exec(open("MainModel2.0.py").read())
OneK_PH_PR = Out_PH4d_PercRej

exec(open("MainModel2.0.py").read())
OneH_PH_PR = Out_PH4d_PercRej

#Pre-Harvest 4h
exec(open("MainModel2.0.py").read())
FiftyK_PH4h_PR = Out_PH4h_PercRej

exec(open("MainModel2.0.py").read())
TenK_PH4h_PR = Out_PH4h_PercRej

exec(open("MainModel2.0.py").read())
FiveK_PH4h_PR = Out_PH4h_PercRej

exec(open("MainModel2.0.py").read())
OneK_PH4h_PR = Out_PH4h_PercRej

exec(open("MainModel2.0.py").read())
OneH_PH4h_PR = Out_PH4h_PercRej


#Pre-Harvest Intense
exec(open("MainModel2.0.py").read())
FiftyK_PHInt_PR = Out_PHInt_PercRej

exec(open("MainModel2.0.py").read())
TenK_PHInt_PR = Out_PHInt_PercRej

exec(open("MainModel2.0.py").read())
FiveK_PHInt_PR = Out_PHInt_PercRej

exec(open("MainModel2.0.py").read())
OneK_PHInt_PR = Out_PHInt_PercRej

exec(open("MainModel2.0.py").read())
OneH_PHInt_PR = Out_PHInt_PercRej



data_scenarios_Conts = {
                ' 50K':   FiftyK_PH_PR,
                ' 10K':   TenK_PH_PR,
                ' 5K':   FiveK_PH_PR,
                ' 1K':   OneK_PH_PR,
                ' 100':   OneH_PH_PR,
          }

df_data_scenarios_Conts = pd.DataFrame(data_scenarios_Conts)
df_data_scenarios_Conts_melted = pd.melt(df_data_scenarios_Conts)
df_data_scenarios_Conts_melted["Type"] = "4d"
Scenariosplot =sns.catplot(x="variable", y="value", data=df_data_scenarios_Conts_melted ,kind="point",  height=4, aspect=2 )
plt.xlabel("Initial Hazard Level Total CFU")
plt.ylabel("Percentage of CFU Rejected at PHS")


data_scenarios_Conts_PH4h = {
                ' 50K':   FiftyK_PH4h_PR,
                ' 10K':   TenK_PH4h_PR,
                ' 5K':   FiveK_PH4h_PR,
                ' 1K':   OneK_PH4h_PR,
                ' 100':   OneH_PH4h_PR,
          }

df_data_scenarios_Conts_PH4h = pd.DataFrame(data_scenarios_Conts_PH4h)
df_data_scenarios_Conts_PH4h_melted = pd.melt(df_data_scenarios_Conts_PH4h)
df_data_scenarios_Conts_PH4h_melted["Type"] = "4h"






CombinedData = pd.concat([df_data_scenarios_Conts_melted,
                          df_data_scenarios_Conts_PH4h_melted])


Scenariosplot =sns.lineplot(x="variable", y="value", hue = "Type", data=CombinedData)
plt.xlabel("Initial Hazard Level Total CFU")
plt.ylabel("Proportion of CFU Rejected at PHS")