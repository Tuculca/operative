import sqlite3
import time
from datetime import datetime
import sys
import numpy
import matplotlib.pyplot as plt
import random
import string

#costante tempo = 631148400

def connectToDb(dbName):
	connection = sqlite3.connect(dbName)
	cursor_pointer = connection.cursor()	
	return cursor_pointer, connection

def sqliteToNumpy(cursor):
	cursor.execute("SELECT * FROM ascat WHERE lat > 30 AND lat < 47 AND lon > 6 AND lon < 38 AND time > '15/09/2020, 09:30:00' AND time < '15/09/2020, 09:36:00' ORDER by time")
	#cursor.execute("SELECT * FROM ascat WHERE lat > 30 AND lat < 47 AND lon > 6 AND lon < 38 AND time > '16/09/2020, 09:09:00' AND time < '16/09/2020, 09:15:00' ORDER by time;")
	#cursor.execute("SELECT * FROM ascat WHERE time > '03/05/2018, 09:00:00' AND time < '03/05/2018, 11:00:00' ORDER by lon;")
	#cursor.execute("SELECT * FROM ascat;")
	output = cursor.fetchall()
	output = numpy.array(output)
	return output

def extractDataFromFetch(Array):
	Time      = Array[:,0]
	#Time = datetime.fromtimestamp(Time + 631148400).strftime("%d/%m/%Y, %I:%M:%S")
	Lat       = Array[:,1].astype(numpy.float)
	Lon       = Array[:,2].astype(numpy.float)
	WindSpeed = Array[:,3].astype(numpy.float)
	WindDir   = Array[:,4].astype(numpy.float)
	return Time, Lat, Lon, WindSpeed, WindDir

def extractDataFromNC(NetCDF):
	Time      = NetCDF['time'][:]
	#Time = datetime.fromtimestamp(Time + 631148400).strftime("%d/%m/%Y, %I:%M:%S")
	Lat       = NetCDF['lat'][:]
	Lon       = NetCDF['lon'][:]
	WindSpeed = NetCDF['wind_speed'][:]
	WindDir   = NetCDF['wind_dir'][:]
	return Time, Lat, Lon, WindSpeed, WindDir

def fromDateToTimestamp(TimeArray):
	for i in range(len(TimeArray)):
		Z = datetime.strptime(TimeArray[i], "%d/%m/%Y, %I:%M:%S")
		Z = datetime.timestamp(Z)
		TimeArray[i] = Z
	Times = TimeArray.astype(numpy.float)
	return Times

def writeHeader(totalNum):
	with open("ob.ascii", "w") as text_file:
		text_file.write(\
"TOTAL ="+"{0:>7}".format(str(totalNum))+", MISS. =-888888., \n\
SYNOP =      0, METAR =      0, SHIP  =      0, BUOY  =      0, BOGUS =      0, TEMP  =      0, \n\
AMDAR =      0, AIREP =      0, TAMDAR=      0, PILOT =      0, SATEM =      0, SATOB =      0, \n\
GPSPW =      0, GPSZD =      0, GPSRF =      0, GPSEP =      0, SSMT1 =      0, SSMT2 =      0, \n\
TOVS  =      0, QSCAT ="+"{0:>7}".format(str(totalNum))+", PROFL =      0, AIRSR =      0, OTHER =      0, \n\
PHIC  =  40.00, XLONC = -95.00, TRUE1 =  36.72, TRUE2 =  36.72, XIM11 =   1.00, XJM11 =   1.00, \n\
base_temp= 290.00, base_lapse=  50.00, PTOP  =  1000., base_pres=100000., base_tropo_pres= 20000., base_strat_temp=   215., \n\
IXC   =     60, JXC   =     90, IPROJ =      1, IDD   =      1, MAXNES=      1, \n\
NESTIX=     60, \n\
NESTJX=     90, \n\
NUMC  =      1, \n\
DIS   =  60.00, \n\
NESTI =      1, \n\
NESTJ =      1, \n\
INFO  = PLATFORM, DATE, NAME, LEVELS, LATITUDE, LONGITUDE, ELEVATION, ID. \n\
SRFC  = SLP, PW (DATA,QC,ERROR). \n\
EACH  = PRES, SPEED, DIR, HEIGHT, TEMP, DEW PT, HUMID (DATA,QC,ERROR)*LEVELS. \n\
INFO_FMT = (A12,1X,A19,1X,A40,1X,I6,3(F12.3,11X),6X,A40) \n\
SRFC_FMT = (F12.3,I4,F7.2,F12.3,I4,F7.3) \n\
EACH_FMT = (3(F12.3,I4,F7.2),11X,3(F12.3,I4,F7.2),11X,3(F12.3,I4,F7.2))\n\
#------------------------------------------------------------------------------#\n")

def writeBody(Date, Lat, Lon, WS, WD):
	#WD = str(90-float(WD)+360)
	#if float(WD)<=90:
	#	WD = str(90-float(WD))
	#else:
	#	WD = str(90-float(WD)+360)
	WD = round(float(WD),2)
	with open("ob.ascii", "a") as text_file:
		text_file.write(\
"FM-281 Quiks"+"{0:>20}".format(str(Date))+"{0:>48}".format(str(1))+"{0:>12}".format(str(Lat))+"{0:>23}".format(str(Lon))+"{0:>23}".format("10.000")+"{0:>22}".format("QSCAT") + "\n\
 -888888.000   0 200.00 -888888.000 -88  0.200\n\
 -888888.000   0 160.00"+"{0:>12}".format(str(WS))+"   0   0.50"+"{0:>12}".format(str(WD))+"   0   4.00                 10.000   0   6.00 -888888.000   0   2.00 -888888.000   0   2.00            -888888.000   0  10.00\n")

def main():
	cur, con     = connectToDb('ascatMany.db')
	times,       \
	lats,        \
	lons,        \
	windSpeeds,  \
	windDirs     = extractDataFromFetch(sqliteToNumpy(cur))
	times = fromDateToTimestamp(times)
	dataLength = len(times)
	writeHeader(dataLength)
	for i in range(dataLength):
		#ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
		date = datetime.fromtimestamp(times[i]).strftime("%Y-%m-%d_%I:%M:%S")
		writeBody(date, '%.3f'%(lats[i]) ,'%.3f'%(lons[i]), '%.3f'%(windSpeeds[i]), '%.3f'%(windDirs[i]))
	con.close()

if __name__ == '__main__':
    main()
