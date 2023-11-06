# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 11:16:48 2016

@author: Clayton Harkey
"""

#===========================================================================#
#### Import needed Packages
#===========================================================================#
import pandas as pd #Pandas-- data framework 
import numpy as np #Numpy-- logic framework
import sklearn as sk
from sklearn import preprocessing
import datetime 
import pickle
import gzip
import re
#===========================================================================#
#### CONFIG AREA
#===========================================================================#
pd.set_option("display.max_rows",999)
pd.set_option("max_seq_items", 2000)
pd.set_option("display.max_columns", 999)
np.set_printoptions(threshold=np.nan)
#===========================================================================#
################## I/O Settings
#===========================================================================#
#Your incoming file, this could be a tkinter prompt or loop?
file=("C:/") #Location of source file

#For writing out the file
OUTPUT_DIRECTORY='C:/' #Place to save output pickle
RunName='Test' #Set for more clarity in output filename
RunType= ' ' #This could be extended to include Others, now it's just Output
#===========================================================================#
################## Math Settings
#===========================================================================#
#Settings for the math to work correctly:
duration_max_stdevs=8 #max number of standard deviations that one may be off
chars="'" 
#===========================================================================#
################## Describe the Input File
#===========================================================================#

#Tell me yo columns!
col='name'
col='name'
col='name'

#===========================================================================#
################## Define Row and Column Removal
#===========================================================================#
#List of all the columns to keep
retained_cols=[col, col, col]
#things to Remove
remove_things1=[' ',' ']
#things to remove
remove_things2=[' ']
#===========================================================================#
################## Syntax Trash and File Read In
#===========================================================================#

#Pull in the data
df=pd.read_csv(filepath_or_buffer=file,engine='c', dtype={users_col:object},usecols=retained_cols,error_bad_lines=False)
df.dtypes
#print(df[users_col])

#Get rid of random marks
#df[col]=df[col].str.rstrip('-')
#df[col]=df[col].str.replace("-","")
#df.columns          
#===========================================================================#
#### NEW SECTION: Defining Functions
#===========================================================================#
def function1(data, col=col, col2=col2, 
                    remove_things=remove_things,remove_things2=remove_things2):
    #get only remaining unique values in the remove list
    remove_things2=list(set(remove_things2))
    #remove things in remove_things2 list
    data=data[~data[col].isin(remove_things2)]
    #Removes users in remove_things list
    data=data[~data[col].isin(remove_things)]
    data = data[pd.notnull(data[' '])]
    #Returns cleaned data, more importantly, a more mem efficient dataset! Wooo!
    return data
    
#Can do all that in here by moving down the standard deviation call 
def Magic(data, col=col,col2=col2, col3=col3, stds=duration_max_stdevs):
    
    
    # show me whatchu got 
    return col1, col2, col3

    
#===========================================================================#
#### Executing Functions/ Call and run
#===========================================================================#
df=Col(data=df)

#Generate output stats to be combined
TcodeUserMetrics, UserMetrics, TcodeMean, TcodeStd, TCodeRealTime=Magic(data=df)

output1=output1(data)


#===========================================================================#
#### Outputting Results
#===========================================================================#
BuildTime=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
#Output Cleansed Data
df.to_csv(OUTPUT_DIRECTORY+RunName+RunType+"_DataCleaned_"+BuildTime+'.csv')
#Write Out the Metrics
output1.to_csv(OUTPUT_DIRECTORY+RunName+RunType+"_name_"+BuildTime+'.csv')
