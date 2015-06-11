"""Script to retrieve dates from HRRR files"""
from datetime import date, timedelta as td
import datetime
import matplotlib.pyplot as plt
import numpy as np
import glob
import os


"""Extracts and collects files into a list"""
def listfiles():
	files = []
	os.chdir("/data/san_store/HRRR")
	for file in glob.glob("*.grib2"):
		files.append(file)
	return files
	

"""Extracts dates within file names"""
def retrieve_dates(files):
	dates = ''
	for i in range(len(files)):
		numbers = ''
		for j in range(8,20):
			numbers += (files[i][j])
		if (i>0 and i<len(files)):
			dates += ','
		dates += numbers
	dates = dates.split(',')
	
	ordered_dates = ','.join(sorted(dates))
	ordered_dates = ordered_dates.split(',')

	t0 = ordered_dates[0]
	tf = ordered_dates[len(ordered_dates)-1]
	
	print "Start Date: " + str(ordered_dates[0])
	print "End Date: " + str(ordered_dates[len(ordered_dates) - 1])

	return t0, tf, ordered_dates 

'''Identifies year, month, and time of beginning and end dates'''
def time_conversion(t0, tf):
	list_d0 = [str(i) for i in t0]
	list_df = [str(i) for i in tf]
	
	y1, y2 = list_d0[0:4], list_df[0:4]
	yr0, yrf = ''.join(y1), ''.join(y2)

	m1, m2 = list_d0[4:6], list_df[4:6]
	m0, mf = ''.join(m1), ''.join(m2)

	d1, d2 = list_d0[6:8], list_df[6:8]
	d0, df = ''.join(d1), ''.join(d2)

	yr0, m0, d0, yrf, mf, df = int(yr0), int(m0), int(d0), int(yrf), int(mf), int(df)
	return yr0, m0, d0, yrf, mf, df

"""Returns a list with all possible dates and times within 
the specified time period"""	
def all_dates(yr0, m0, d0, yrf, mf, df):
	d1 = date(yr0, m0, d0)
	d2 = date(yrf, mf, df)
	
	delta = d2 - d1
	dates = []
	nodashdates = []
	officialdates = []

	for i in range(delta.days + 1):
		d = d1 + td(days = i)
		dates.append(str(d))

	for i in range(len(dates)):
		newdates = dates[i].replace("-", "")
		nodashdates.append(newdates)

	for w in range(len(nodashdates)):
		timedate = nodashdates[w] + '0000'
		count = int(timedate)
		newcount = count + 2300
		while (count < newcount):
			count += 100
			officialdates.append(str(count))
	
	print officialdates
	return officialdates

"""Compares two sets of dates to identify missing dates"""
def comparison(officialdates, ordered_dates):
	missing_dates = list(set(officialdates) - set(ordered_dates))

	print missing_dates
	missing = ','.join(sorted(missing_dates))
	missing = missing.split(',')
	print "Missing Dates: " + str(missing)

files = listfiles()
t0, tf, ordered_dates = retrieve_dates(files)
yr0, m0, d0, yrf, mf, df = time_conversion(t0, tf)
officialdates = all_dates(yr0, m0, d0, yrf, mf, df)
comparison(officialdates, ordered_dates)
