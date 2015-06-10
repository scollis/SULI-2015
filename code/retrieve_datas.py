"""Script to retrieve dates from HRRR files"""
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
		for j in range(8,16):
			numbers += (files[i][j])
		if (i>0 and i<len(files)):
			dates += ','
		dates += numbers
	dates = dates.split(',')
	
	ordered_dates = ','.join(sorted(dates))
	print ordered_dates
	ordered_dates = ordered_dates.split(',')

	print "Start Date: " + str(ordered_dates[0])
	print "End Date: " + str(ordered_dates[len(ordered_dates)-1]) 


files = listfiles()
retrieve_dates(files)

 
