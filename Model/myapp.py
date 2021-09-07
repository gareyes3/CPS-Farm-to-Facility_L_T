# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 09:16:17 2021

@author: gareyes3
"""
#import sys
#sys.path
#sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility\Model')

import streamlit as st
import pandas as pd

import pandas as pd 
import seaborn as sns
from matplotlib import pyplot as plt
import base64


#Own Libraries ----------------------------------------------------------------
import Funz
import ContScen
import Listz 
import OutFunz
import InFunz
import ScenCondz
import ContCondz
import Inputz
from importlib import reload 

reload(Listz)
reload(Inputz)
#Main Model Loops
import MainModel3z


#Header------------------------------------------------------------------------

#Main Header and Title for the model
st.write("""
# CPS Farm to Facility Web App
This App Predicts the Following:
- Percent of CFU Rejected
- Percent of Lb. Rejected
""")

#SideBar
st.sidebar.header('Scenario Input Parameters')
Inputz.N_Iterations = st.sidebar.number_input("Enter Iteration Number",value = 10, min_value = 0, max_value =1000)

#Contamination Scenarios
st.sidebar.write("""
Select Contamination Scenarios
""")

ContCondz.Background_C = st.sidebar.checkbox("Background")
ContCondz.Point_Source_C = st.sidebar.checkbox("Point Source")
ContCondz.Systematic_C = st.sidebar.checkbox("Systematic")
ContCondz.Crew_C = st.sidebar.checkbox(" Harvesting Crew")
ContCondz.Harvester_C = st.sidebar.checkbox("Harvester")
ContCondz.PE_C = st.sidebar.checkbox("Processing Equipment")
ContCondz.Pack_C = st.sidebar.checkbox("Packing")
#Cont_Scen = st.sidebar.selectbox('Contamination Scenario', ["Background","Point Source","Systematic", "Processing Line", "Harvesting Crew","Harvester","Finished Product"])
Inputz.Field_Weight = st.sidebar.select_slider('Field Size [Lb]',options=[1000,10000,50000,100000,200000],value = 100000)


#Contamination Scenarios
#if Cont_Scen == "Background":
#    ContCondz.Background_C = 1


def get_table_download_link_csv(df):
    #csv = df.to_csv(index=False)
    csv = df.to_csv().encode()
    #b64 = base64.b64encode(csv.encode()).decode() 
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="Results.csv" target="_blank">Download csv file</a>'
    return href



st.subheader('Results Will be Here')

#Looks
if st.sidebar.button('Click Here to Iterate'):
    #Side Bar Inputs
    Main_Mod_Outs=MainModel3z.F_MainLoop()
    D_PH4d = Main_Mod_Outs[1]
    DProg_PH4d=Main_Mod_Outs[0]
    
    
    #Results
    st.subheader('Outputs DataFrame')
    st.write(D_PH4d)
    st.markdown(get_table_download_link_csv(D_PH4d), unsafe_allow_html=True)
    
    st.subheader('Boxplot')
    fig = plt.figure(figsize=(8,4)) # try different values
    sns.boxplot(y=D_PH4d["PerRejected at PH"])
    plt.ylabel("Percenta CFU Rejected by Sampling Plan")

    st.pyplot(fig)
    
    

    

    



