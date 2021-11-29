# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:07:18 2021

@author: Gustavo Reyes
"""

import math
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

2000/5
2000/2

math.sqrt(400)

d = pd.DataFrame(np.zeros((1, 2000)))

d.at[0,20:40] = 2500
d.at[0,400:420] = 2500
d.at[0,550:570] = 2500
d.at[0,1200:1220] = 2500

d.drop(d.iloc[:,0:200], inplace = True, axis = 1)

ax =sns.heatmap(d,cmap="crest", cbar_kws={"shrink": 0.4}, yticklabels = 10, xticklabels=200, cbar=False)
ax.set_aspect(80)


linewidths=0.004, linecolor='black'