# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 09:22:17 2015

@author: cbharkey
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
file=("C:/Users/107322/Downloads/MarFinalMerge.txt") #Location of source file

#For writing out the file
OUTPUT_DIRECTORY='C:/Users/107322/Downloads/Productivity/March2016/' #Place to save output pickle
RunName='Test' #Set for more clarity in output filename
RunType= 'ProductivityStats' #This could be extended to include Others, now it's just Output
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
localdate_col='ZLOGDATE_LOCAL'
localtime_col='ZLOGTIME_LOCAL'
starttime_col='STARTTIMESTAMP'
endtime_col='ENDTIMESTAMP'
duration_col='DURATION'
task_col='TASKTYPE'
account_col='ACCOUNT'
context_col='CONTEXT_ID'
trans_col='TRANSID'
dialog_col='DIALOG_STEP'
entry_col='ENTRY_ID'
terminal_col='TERMINALID'
users_col='USERID'
report_col='REPORT'
tcode_col='TCODE'
cua_col='CUA_PROG'
client_col='CLIENT'
instance_col='INSTANCE'


#===========================================================================#
################## Define Row and Column Removal
#===========================================================================#
#List of all the columns to keep
retained_cols=[starttime_col,endtime_col, duration_col, account_col,
               context_col,trans_col, users_col,report_col,
               tcode_col, localdate_col]
#Users to Remove
remove_users=['ALE_CPIC','SM_EFWK','Display Customer','TA-BATCH','GRC_ADMIN']
#Codes to remove
remove_codes=['SESSION_MANAGER']
#===========================================================================#
################## Syntax Trash and File Read In
#===========================================================================#

#Pull in the data
df=pd.read_csv(filepath_or_buffer=file,engine='c', dtype={users_col:object},usecols=retained_cols,error_bad_lines=False)
df.dtypes
#print(df[users_col])
#Drop those with Cam in User name
df[users_col]=df[users_col].replace("CAM/","")
#Get rid of random marks
#df[duration_col]=df[duration_col].str.rstrip('-')
#df[duration_col]=df[duration_col].str.replace("-","")
df['durationreplace']=df[duration_col].astype(str)
#df['durationreplace'].isnull().sum()
df['durationreplace']=df['durationreplace'].str.replace("-","")
#df['durationreplace'].isnull().sum()
df['durationreplace']=df['durationreplace'].str.replace(" ","")
#df['durationreplace'].isnull().sum()
df['durationreplace']=df['durationreplace'].astype(float)
#df['durationreplace'].isnull().sum()
df[duration_col]=df['durationreplace']
df=df.drop(['durationreplace'], axis=1)
#df.columns          
#===========================================================================#
#### NEW SECTION: Defining Functions
#===========================================================================#
def CodeUserRowDrop(data, users_col=users_col, tcode_col=tcode_col, 
                    remove_users=remove_users,remove_codes=remove_codes):
    #get only remaining unique values in the remove list
    remove_codes=list(set(remove_codes))
    #remove tcodes in remove_codes list
    data=data[~data[tcode_col].isin(remove_codes)]
    #Removes users in remove_users list
    data=data[~data[users_col].isin(remove_users)]
    data = data[pd.notnull(data['DURATION'])]
    #Returns cleaned data, more importantly, a more mem efficient dataset! Wooo!
    return data
    
#Can do all that in here by moving down the standard deviation call 
def Magic(data, users_col=users_col,tcode_col=tcode_col, context_col=context_col, stds=duration_max_stdevs):
    #Remove every duration >X Standard Deviations away, replace with X*Stdev of Col 
    data['DURATION_RealTime']=data['DURATION']
    data.DURATION[np.abs(data.DURATION - data.DURATION.mean()) > stds * data.DURATION.std()] = data.DURATION.std()*stds
    # Get the average per user per tcode
    tcodeUserMetrics=data.groupby([users_col,tcode_col]).agg({duration_col: np.mean, trans_col: pd.Series.nunique, 'DURATION_RealTime': np.sum})
    #tcodeAverages=tcodeUserStats.groupby([[tcode_col]]).agg({duration_col:np.mean, duration_col: np.std, trans_col: np.mean, trans_col: np.std})
    #get the tcodes per user 
    userMetrics=data.groupby([users_col]).agg({tcode_col: pd.Series.nunique, localdate_col: pd.Series.nunique,
                             trans_col:pd.Series.nunique, duration_col: np.sum,'DURATION_RealTime': np.sum})
    #productivity for tcodes
    tcodeMean=data.groupby([tcode_col]).agg({duration_col: np.mean})
    tcodeRealTime=data.groupby([tcode_col]).agg({'DURATION_RealTime': np.sum})
    tcodeStd=data.groupby([tcode_col]).agg({duration_col: np.std})
    # show me whatchu got 
    return tcodeUserMetrics, userMetrics, tcodeRealTime, tcodeMean, tcodeStd


#Function to prep the consumption metrics 
def Consumption(data, value_to_replace=np.nan, filler_val=0, min_val=.65, max_val=1,stds=3):
    data = data[pd.notnull(data['DURATION'])]
    #data=data.replace(to_replace=value_to_replace, value=filler_val)
    tmp= (data-data.mean())/data.std()
    ConsumptionScore=np.array(tmp.sum(axis=1))
    #print(ConsumptionScore)
    ConsumptionScore[np.abs(ConsumptionScore - ConsumptionScore.mean()) > stds * ConsumptionScore.std()] = stds * ConsumptionScore.std()
    scaler=preprocessing.MinMaxScaler()
    data['Consumption']=scaler.fit_transform(ConsumptionScore)
    data['ConsumptionScore']=min_val+(data['Consumption']*(max_val-min_val))
    data['TCODEMax']=data['TCODE'].max()
    return data

#Function to pull data together by tcode for users data=TcodeUserMetrics
def ProductivityByTcode(data,tcodeMean,tcodeStd,tcodeRealTime,trans_col=trans_col, 
                        value_to_replace=np.nan, filler_val=0, min_val=.65, 
                        max_val=1,stds=3):
    data=data.replace(to_replace=value_to_replace, value=filler_val)
    tcodeMean.columns = ['TCodeMean']
    tcodeStd.columns= ['TCodeStd']
    tcodeRealTime.columns=['TCodeRealTime']
    TCodeMerge= pd.merge(left=tcodeMean.reset_index(),right=tcodeStd.reset_index(), 
                    how='left', left_on=tcode_col, right_on=tcode_col)
    TCodeMerge= pd.merge(left=TCodeMerge.reset_index(),right=tcodeRealTime.reset_index(), 
                    how='left', left_on=tcode_col, right_on=tcode_col)
    TCodeMerge=TCodeMerge.replace(to_replace=value_to_replace, value=filler_val)
    merge= pd.merge(left=data.reset_index(),right=TCodeMerge.reset_index(), 
                    how='left', left_on=tcode_col, right_on=tcode_col)
    merge['DurationNorm']=(merge['DURATION']-merge['TCodeMean'])/merge['TCodeStd']
    merge['TransNorm']=(merge[trans_col]-merge[trans_col].mean())/merge[trans_col].std()
    #merge['MaxTCODE']=merge['TCODE'].max()
    merge.drop(['index'], axis=1, inplace=True)
    ProductivityNorm=np.array(.33*merge['TransNorm']-.99*merge['DurationNorm'])
    ProductivityNorm[np.isnan(ProductivityNorm)] =filler_val
    ProductivityNorm[np.abs(ProductivityNorm - ProductivityNorm.mean()) > stds * ProductivityNorm.std()] = stds * ProductivityNorm.std()
    scaler=preprocessing.MinMaxScaler()
    merge['Productivity']=scaler.fit_transform(ProductivityNorm)
    merge['ProductivityScore']=min_val+(merge['Productivity']*(max_val-min_val))
    #merge.drop(['index'], axis=1, inplace=True)
    return merge
    
#===========================================================================#
#### Executing Functions/ Call and run
#===========================================================================#
df=CodeUserRowDrop(data=df)
#tcodes=df[tcode_col].unique()
#Generate output stats to be combined for Productivity and Consumption metrics
TcodeUserMetrics, UserMetrics, TcodeMean, TcodeStd, TCodeRealTime=Magic(data=df)
#print(UserMetrics[tcode_col])
consumption=Consumption(UserMetrics)
#print(consumption['TCODEMax'])
ProductivityByTCode=ProductivityByTcode(TcodeUserMetrics,tcodeMean=TcodeMean,tcodeStd=TcodeStd,tcodeRealTime=TCodeRealTime)
#print(ProductivityByTCode['MaxTCODE'])
#ProductivityByTCode.columns

#===========================================================================#
#### Outputting Results
#===========================================================================#
BuildTime=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
#Output Cleansed Data
df.to_csv(OUTPUT_DIRECTORY+RunName+RunType+"_DataCleaned_"+BuildTime+'.csv')
#Write Out the Productivity Metrics 
ProductivityByTCode.to_csv(OUTPUT_DIRECTORY+RunName+RunType+"_ProductivityByTcode_"+BuildTime+'.csv')
#Now Write out the Consumption Values
consumption.to_csv(OUTPUT_DIRECTORY+RunName+RunType+"_Consumption_"+BuildTime+'.csv')
#User Metrics wriiteeeeeeeee
UserMetrics.to_csv(OUTPUT_DIRECTORY+RunName+RunType+"_UserMetrics_"+BuildTime+'.csv')
#OutputTcodeMetrics
#TcodeMetrics.to_csv(OUTPUT_DIRECTORY+RunName+RunType+"_TcodeMetrics_"+BuildTime+'.csv')