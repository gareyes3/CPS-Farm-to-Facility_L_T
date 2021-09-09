# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 13:49:05 2021

@author: gareyes3
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

x= [0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0,0,10]
df = pd.DataFrame(x)


plt.imshow(df, cmap='viridis')
plt.colorbar()
plt.show()