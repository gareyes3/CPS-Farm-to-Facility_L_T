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

d.at[0,0:1] = 100000
d.at[0,400:600] =75000

d.at[0,240:260] = 100000


d.drop(d.iloc[:,0:200], inplace = True, axis = 1)

ax =sns.heatmap(d,cmap="crest", cbar_kws={"shrink": 0.4}, yticklabels = 10, xticklabels=200, cbar=False,vmax  = 100_000 , vmin = 0)
ax.set_aspect(80)
plt.xlabel('Partition Number')


linewidths=0.004, linecolor='black'