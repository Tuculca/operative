#!/bin/bash

ulimit -s unlimited

. /home/model/.bashrc
. /home/model/.export_intel.2017


#. /mnt/disk2/afalcione/start.sh
HOME=/mnt/disk2/afalcione/OPER_intel

YearStart=$(date -d "now" +"%Y")
MonthStart=$(date -d "now" +"%m")
DayStart=$(date -d "now" +"%d")
#DayStart=14
HourStart=12
YearEnd=$(date -d "now + 48 hour" +"%Y")
MonthEnd=$(date -d "now + 48 hour" +"%m")
DayEnd=$(date -d "now + 48 hour" +"%d")
#DayEnd=14
HourEnd=12

echo 'Start: ' $YearStart $MonthStart $DayStart $HourStart 'End: ' $YearEnd $MonthEnd $DayEnd $HourEnd

cd ${HOME}/DATA
rm -r gfs*
./downloadDataGFS.sh $YearStart $MonthStart $DayStart

cd ${HOME}
./writeNamelistWPS.sh $YearStart $MonthStart $DayStart $YearEnd $MonthEnd $DayEnd

./writeNamelistInput.sh $YearStart $MonthStart $DayStart $YearEnd $MonthEnd $DayEnd

cd ${HOME}/WPSv4.4

./geogrid.exe

rm GRIBFILE* 
./link_grib.csh ${HOME}/DATA/gfs*

rm FILE*
./ungrib.exe

rm met_em*
./metgrid.exe

cd ${HOME}/WRFv4.4.1/run

rm -f met_em*
ln -s ${HOME}/WPSv4.4/met_em* .

rm wrfinput*
rm wrfbdy*
/opt/intel/local/openmpi/bin/mpirun -np 18 real.exe

rm wrfout*
/opt/intel/local/openmpi/bin/mpirun -np 18 wrf.exe

rm ${HOME}/out/wrfout*
mv wrfout* ${HOME}/out

rm ${HOME}/plots/*.jpg
cd ${HOME}/plots
./plotParallel.sh "${HourStart}:00:00 ${YearStart}-${MonthStart}-${DayStart}"

exit
