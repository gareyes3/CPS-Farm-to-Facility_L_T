# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 09:26:41 2021

@author: gareyes3
"""

#%%
import sys
sys.path
#sys.path.append('C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model')
sys.path.append('C:\\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility\Model')
#%% 
#Libraries, Modules
import os
os.chdir(r'C:\Users\gareyes3\Documents\GitHub\CPS-Farm-to-Facility\Model')


#%%
#Importing Libraries and Modules

exec(open('Librariez.py').read())
Inputz.Hazard_lvl = 20000
exec(open('Temp_Trial3.py').read())
reload(Listz)
reload(Inputz)
exec(open('LoopOnly.py').read())
