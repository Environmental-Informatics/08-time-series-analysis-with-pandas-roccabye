#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 12:05:12 2020
Program description: This script uses numpy, pandas and matplotlib to conduct timeseries analysis of 
 Arctic Oscillation (AO ) and North Atlantic Oscillation (NAO) data sets from 
 1950 to 2020 but NAO has single data for 2020 while AO has two data for 2020.
 Three plots are generated at the end,
1.  Daily Arctic Oscillation (AO) plot (line [59]:)
2.  Annual median values for AO (line [138]:)
3.  Rolling mean for both AO and NAO (line [160]:)

@author: Alka Tiwari (tiwari13) Github: roccabye
"""
#import os
# os.chdir('/home/tiwari13/ABE65100/08-time-series-analysis-with-pandas-roccabye/PandasDemo')

# /home/tiwari13/ABE65100/08-time-series-analysis-with-pandas-roccabye
#Module import

import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
plt.close('all')
pd.set_option('display.max_rows',15) # this limit maximum numbers of rows

pd.__version__

##############################################
# Loading data
# Download ascii files - monthly.ao.index.b50.current.ascii

!wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/monthly.ao.index.b50.current.ascii

# Read data with numpy
ao = np.loadtxt('monthly.ao.index.b50.current.ascii')

# check the data
ao[0:2]
ao.shape

##############################################
#TIMEsERIES

#Convert this data in to time series,
#create the range of dates for our time series - record starts at January 1950.
# generate as many time stamps as we have records. 
# Frequency of the data is one month (freq='M').
dates = pd.date_range('1950-01', periods=ao.shape[0], freq='M')

# create our first time series. 
# Dates from the dates variable will be our index, 
# and AO values will be our, hm... values:

AO = Series(ao[:,2], index=dates)
print(AO)
# plot complete time series:
AO.plot()
plt.title('Daily Atlantic Oscillation')
plt.xlabel('Year')
plt.ylabel('Atlantic Oscillation Value')
plt.savefig("/home/tiwari13/ABE65100/08-time-series-analysis-with-pandas-roccabye/PandasDemo/Output/DailyAtlanticOscillation.pdf")

# its part:
AO['1980':'1990'].plot()
# even smaller part
AO['1980-05':'1981-03'].plot()

# DataFrame
#!curl http://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii >> 'norm.nao.monthly.b5001.current.ascii'

# Download ascii files - norm.nao.monthly.b5001.current.ascii
!wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii
nao = np.loadtxt('norm.nao.monthly.b5001.current.ascii')
dates_nao = pd.date_range('1950-01', periods=nao.shape[0], freq='M')
NAO = Series(nao[:,2], index=dates_nao)

#check timeperiod
NAO.index

# create Data Frame, that will contain both AO and NAO data. 
#It sort of an Excel table where the first row contain 
# headers for the columns and firs column is an index:

aonao = DataFrame({'AO' : AO, 'NAO' : NAO})

# One can plot the data straight away:
aonao.plot(subplots=True)

#  look at the first several rows:
aonao.head()

# reference each column by its name:
aonao['NAO']

#as method of the Data Frame variable (if name of the variable is a valid python name)
aonao.NAO

# simply add column to the Data Frame:
aonao['Diff'] = aonao['AO'] - aonao['NAO']
aonao.head()

#And delete it:
del aonao['Diff']
aonao.tail()
#Slicing will also work:
aonao['1981-01':'1981-03']

#even in some crazy combinations:
# choose all NAO values in the 1980s for months where AO is positive 
#and NAO is negative, and then plot them.
import datetime
aonao.loc[(aonao.AO > 0) & (aonao.NAO < 0) 
        & (aonao.index > datetime.datetime(1980,1,1)) 
        & (aonao.index < datetime.datetime(1989,1,1)),
        'NAO'].plot(kind='barh')

# Statistics
# statistical information over elements of the Data Frame. Default is column wise:
aonao.mean()
aonao.max()
aonao.min()

# doing it row wise.
aonao.mean(1)

# Or get everything at once:
aonao.describe()

#Resampling
AO_mm = AO.resample("A").mean()
AO_mm.plot(style='g--')


# Annual Median value for Atlantic Oscillations.
AO_mm = AO.resample("A").median()
AO_mm.plot()
plt.title('Annual Median value for Atlantic Oscillations')
plt.xlabel('Year')
plt.ylabel('Atlantic Oscillations Values')
plt.savefig("/home/tiwari13/ABE65100/08-time-series-analysis-with-pandas-roccabye/PandasDemo/Output/AnnualMedian_AO.pdf")

#can use your methods for resampling, for example np.max (in this case we change 
# resampling frequency to 3 years):

AO_mm = AO.resample("3A").apply(np.max)
AO_mm.plot()

# specify several functions at once as a list:

AO_mm = AO.resample("A").apply(['mean', np.min, np.max])
AO_mm['1900':'2020'].plot(subplots=True)
AO_mm['1900':'2020'].plot()
AO_mm


# Moving (rolling) statistics
# Rolling mean:
aonao.rolling(window=12, center=False).mean().plot(style='-g')
plt.title('Rolling Mean for AO and NAO')
plt.xlabel('Year')
plt.ylabel('Rolling Mean Values')
plt.savefig("/home/tiwari13/ABE65100/08-time-series-analysis-with-pandas-roccabye/PandasDemo/Output/RollingMean_AONAO.pdf")

# Rolling correlation:
aonao.AO.rolling(window=120).corr(other=aonao.NAO).plot(style='-g')

# getting correlation coefficients for members of the Data Frame 
aonao.corr()







