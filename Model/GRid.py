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

d = pd.DataFrame(np.zeros((20, 100)))

d.at[13,40] = 50
ax =sns.heatmap(d,cmap="crest", cbar_kws={"shrink": 0.4}, yticklabels = 10, xticklabels=10)
ax.set_aspect("equal")

