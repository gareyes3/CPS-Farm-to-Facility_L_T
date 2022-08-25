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

#%%

Inputz_T.Iteration_Number = 500
Scen_T.Tomatoes_per_sample = 1
reload(DepInputz)
Outs_S1_A = MainModel.Main_Loop()

Inputz_T.Iteration_Number = 500
Scen_T.Tomatoes_per_sample = 5
reload(DepInputz)
Outs_S1_B = MainModel.Main_Loop()

Inputz_T.Iteration_Number = 500
Scen_T.Tomatoes_per_sample = 100
reload(DepInputz)
Outs_S1_C = MainModel.Main_Loop()