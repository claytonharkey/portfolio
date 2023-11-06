# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 10:32:50 2017

@author: harkey
"""
#TTime Series - Cash Forecasting
#===========================================================================#
#### Import needed Packages
#===========================================================================#
import pandas as pd
import numpy as np
import datetime
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
from matplotlib import pyplot
plt.style.use('fivethirtyeight')
#===========================================================================#
#### Environment settings-- better trouble shooting, null outside ipython
#===========================================================================#
pd.set_option("display.max_rows",999) #Increase Row printing
pd.set_option("max_seq_items", 2000) #Increase sequential printing
pd.set_option("display.max_columns", 999) #increase max columns
np.set_printoptions(threshold=np.inf) #Eliminate thresholds for numpy

#===========================================================================#
#### Read in the data
#===========================================================================#

data = pd.read_csv('F:/HP/2nd run/e drive/CashForecasting/TempBankActualsTS.txt')
data.info()

#===========================================================================#
#### Graphs for quick reference and initial analysis 
#===========================================================================#
ax = data.set_index('TranDate').plot(figsize=(20, 12))
ax.set_ylabel('Amt')
ax.set_xlabel('Date')
plt.show()

