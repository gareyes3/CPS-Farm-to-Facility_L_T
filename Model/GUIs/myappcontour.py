# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 13:06:36 2021

@author: gareyes3
"""

#Importing python modules. 
import streamlit as st
import pandas as pd
import pandas as pd 
import seaborn as sns
from matplotlib import pyplot as plt
import base64
import plotly
import plotly.express as px


#Own Libraries ----------------------------------------------------------------
import Funz
import ContScen
import Listz 
import OutFunz
import InFunz
import ScenCondz
import ContCondz
import Inputz
import SCInputz
import AppFunz
import ContAnalysis
from importlib import reload 

reload(Listz)
reload(Inputz)
#Main Model Loops
import MainModel3z


#%%
st.sidebar.header('Start Here: Select your Inputs')

 
#Field Size
ContAnalysis.FieldSize = st.sidebar.number_input('Field Mass [Lb]',0,1000000,step = 50, value = 100000)

#Select The clustering Level

ContAnalysis.Clust_Weight = st.sidebar.number_input('Cluster Mass [lb]',0,1000000,step = 50, value = 1000)

#Select The CFU in Cluster

ContAnalysis.CFU_Clust = st.sidebar.number_input('Contamintion in Cluster [CFU]',0,10000000,step = 1000, value = 50000)

#Sampling Plan
st.sidebar.write("""
Select Sampling Strategy:
""")

layoutSamp = st.sidebar.columns([3, 3])
with layoutSamp[0]: 
    ContAnalysis.PH_Sampling = st.checkbox("PreHarvest")
    ContAnalysis.H_Sampling = st.checkbox("Harvest")

 
with layoutSamp[-1]: 
    ContAnalysis.R_Sampling = st.checkbox("Receiving")
    ContAnalysis.FP_Sampling = st.checkbox("Finished Product")
    
    
if ContAnalysis.PH_Sampling ==True:
    st.sidebar.write("""
Pre-Harvest sampling tuning parameters
""")
    PH_S_Stratgy = st.sidebar.selectbox(label = "Select Type of Pre-Harvest Sampling", options = ["4 day", "4 Hour", "Intense"])
    if  PH_S_Stratgy == "4 day":
        ContAnalysis.PHS_4d = True
    elif PH_S_Stratgy == "4 Hour":
        ContAnalysis.PHS_4h = True
    elif PH_S_Stratgy == "Intense":
        ContAnalysis.PHS_Int = True
        
if ContAnalysis.H_Sampling ==True:
    st.sidebar.write("""
In-Harvest sampling tuning parameters
""")
    H_S_Stratgy = st.sidebar.selectbox(label = "Select Type of In-Harvest Sampling", options = ["Traditional", "Aggregative"])
    if  H_S_Stratgy == "Traditional":
        ContAnalysis.HS_Trad = True
    elif H_S_Stratgy == "Aggregative":
        ContAnalysis.HS_Agg = True

if ContAnalysis.FP_Sampling ==True:
    st.sidebar.write("""
Finished product sampling tuning parameters
""")
    FP_S_Stratgy = st.sidebar.selectbox(label = "Select Type of Finished Product Sampling", options = ["Traditional", "Aggregative"])
    if  FP_S_Stratgy == "Traditional":
       ContAnalysis.FPS_Trad = True
    elif FP_S_Stratgy == "Aggregative":
        ContAnalysis.FPS_Agg = True
        

##Model Running: 

st.write("""
## Welcome
This is an interactive web app designed to run sampling simulation in a food safety context. The simulation model is maintained by researchers of the Stasiewicz Food Safety Lab under the department of Food Science and Human Nutrition at the University of Illinois at Urbana-Champaign .
### Goal:
We aim to provide a tool to simulate sampling in a Farm to Facility Process. The results evaluate the performance of any specific sampling plan.
""")

st.subheader('Get your sampling heatmap here:')

SCInputz.N_Iterations = st.button("Run")
