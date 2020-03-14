#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:08:42 2020
Program description: This script uses oanda to conduct timeseries analysis of 
Wabash river streamflow at Lafayette gauge. The data is from Mar. 17 2015 to Mar. 24, 2016.
It is 15 minute discharge (cfs) data. Three plots are generated at the end,
1. Daily average value of streamflow for the entire 13 months
2. Ten peak daily average value of streamflow for the period.
3. Monthly average value of the streamflow for the entire period.
@author: tiwari13
"""

#import os
# os.chdir('/home/tiwari13/ABE65100/08-time-series-analysis-with-pandas-roccabye/SourceCode')
#Module import

import pandas as pd
import numpy as np
from pandas import Series, DataFrame, Panel
import matplotlib.pyplot as plt
plt.close('all')
pd.set_option('display.max_rows',15) # this limit maximum numbers of rows

pd.__version__

##############################################
# Loading data

streamflow = '/home/tiwari13/ABE65100/08-time-series-analysis-with-pandas-roccabye/Input/WabashRiver_DailyDischarge_20150317-20160324.txt'

# Read data in Pandas dataframe
# Skipping 25 columns of th etext file and using only column 2 for datetime column 4 for discharge in cfs
strflw = pd.read_table(streamflow,parse_dates=True, header=24,skiprows=[25], delimiter= '\t',
                    usecols=[2,4], index_col= ['datetime'], names = ['datetime','Discharge(cfs)'])

# check the data
strflw[0:2]
strflw.shape

##############################################
'''
Create a plot of daily average streamflow for the period of record, written to a PDF or PS file.
'''
# Computing daily mean/average using 'resample' command.

Q_avg_daily = strflw.resample('D').mean()
Q_avg_daily[0:2]
Q_avg_daily.shape

# Plot daily mean of discharge values.

Q_avg_daily.plot(color = 'coral')

# Set title and labels for axes

plt.xlabel('DateTime', fontsize=10)                                         # Label x-axis
plt.ylabel('Discharge (cfs)', fontsize=10)                # Label y-axis
plt.title('Daily Average Streamflow for Wabash River at Lafayette \nfrom Mar. 17 2015 to Mar. 24, 2016', fontsize=10) # Title
plt.savefig("/home/tiwari13/ABE65100/08-time-series-analysis-with-pandas-roccabye/Output/DailyAverage_Q.pdf")

##############################################
'''
Using the daily average flow data, identify and plot the 10 days with highest flow, 
written to a PDF or PS file. Use symbols to represent the data on the same time axis 
used for the full daily flow record.'''

# Sorting 10 highest streamflow values from daily average flow data (Q_avg)
Q_avg_daily_highestFlow = Q_avg_daily.nlargest(10,['Discharge(cfs)'])
x = pd.to_datetime(Q_avg_daily_highestFlow .index)

# check the data
Q_avg_daily_highestFlow[0:2]
Q_avg_daily_highestFlow.shape

# Plot ten highest daily mean values on the daily mean streamflow plot.

plt.figure()
Q_avg_daily.plot(color = 'chartreuse')
plt.scatter(x,Q_avg_daily_highestFlow['Discharge(cfs)'], color = 'violet')
leg=plt.legend()
leg.get_texts()[1].set_text('10 Peak Discharge')

# Set title and labels for axes

plt.xlabel('DateTime', fontsize=10)                                         # Label x-axis
plt.ylabel('Discharge (cfs)', fontsize=10)                # Label y-axis
plt.title('Daily Average Streamflow for Wabash River with top 10 peak values \nfrom Mar. 17 2015 to Mar. 24, 2016', fontsize=10) # Title
plt.savefig("/home/tiwari13/ABE65100/08-time-series-analysis-with-pandas-roccabye/Output/10Peak_DailyAverage_Q.pdf")

##############################################
'''
Create a plot of monthly average streamflow for the period of record, 
written to a PDF or PS file.
'''
# Computing monthly mean/average using 'resample' command.

Q_avg_monthly = strflw.resample('M').mean()
Q_avg_monthly[0:2]
Q_avg_monthly.shape
# Plot daily mean of discharge values.

Q_avg_monthly.plot(color = 'orangered')

# Set title and labels for axes

plt.xlabel('DateTime', fontsize=10)                                         # Label x-axis
plt.ylabel('Discharge (cfs)', fontsize=10)                # Label y-axis
plt.title('Monthly Average Streamflow for Wabash River at Lafayette \nfrom Mar. 17 2015 to Mar. 24, 2016', fontsize=10) # Title
plt.savefig("/home/tiwari13/ABE65100/08-time-series-analysis-with-pandas-roccabye/Output/MonthlyAverage_Q.pdf")

##############################################





















