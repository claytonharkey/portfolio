# -*- coding: utf-8 -*-
"""
Created on Fri May 26 09:40:21 2017

@author: harkey
"""

#Text Processing for Image Recognition
#===========================================================================#
#### Import needed Packages
#===========================================================================#
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#===========================================================================#
#### Environment settings-- better trouble shooting, null outside ipython
#===========================================================================#
pd.set_option("display.max_rows",999) #Increase Row printing
pd.set_option("max_seq_items", 2000) #Increase sequential printing
pd.set_option("display.max_columns", 999) #increase max columns
np.set_printoptions(threshold=np.ALLOW_THREADS) #Eliminate thresholds for numpy
#===========================================================================#
#### Read in the data
#===========================================================================#

df = pd.read_csv('C:/Users/Clayton.Harkey/Data/18-23SalesByCat_unpivot.csv')
df.info()

columns = df.columns.tolist()
columns

#===========================================================================#
#### Correlation Matrix
#===========================================================================#


sns.set_theme(style="darkgrid")

corr = df.corr()

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

# Show the plot
plt.show()