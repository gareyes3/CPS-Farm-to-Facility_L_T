# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 09:41:52 2021

@author: gareyes3
"""

#%%
import sys
sys.path
#sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model')
sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility\Model')

#%% Libraries
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
import ContScen
import Listz 
import OutFunz
import InFunz
import ScenCondz
import Inputz
from importlib import reload 

#Main Model Loops
import MainModel3z

#%% 
#Progression DataFrame. 
Progression_DFS = []
#%% First Analysis 
Main_Mod_Outs=MainModel3z.F_MainLoop()


