# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 10:32:59 2021

@author: gareyes3
"""
Final_Temp = 25
initial_temp = 5

7544*temp**(-3.11)

lag =[]
Times_Growth = list(range(0,60*10))
print(Times_Growth)
Temp = initial_temp
for i in Times_Growth:
    if Temp < Final_Temp:
        Change_p_min = 0.017
        Temp = Temp + Change_p_min
    if Temp == Final_Temp:
        Temp = Temp
    Per_Lag = (7544*Temp**(-3.11))/600
    lag.append(Per_Lag)
    
sum(lag)


b = 0.023
Temp = 25
Tmin = 1.2
Time_T = 1
mu = (b*(Temp-Tmin))**2

growth_log = (mu*Time_T)/2.303
growth_log

50000*10**growth_log


(1*10**5.4) - (1*10**5.1)
math.log10(125296)
