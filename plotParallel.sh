#!/bin/bash -l

addressWrfouts=/mnt/disk2/afalcione/OPER_intel/out

eval "$(conda shell.bash hook)"
conda activate
/mnt/disk2/afalcione/miniconda3/bin/conda activate

cd /mnt/disk2/afalcione/OPER_intel/plots

for domain in d01 d02
do

dateStart=$1
#dateStart="12:00:00 2022-12-17"
dateEnd=$(date -d "$dateStart + 48 hour" +%Y-%m-%d_%H:%M:%S)
dateNewFmt=$dateStart
dateNew=$dataStart

while [ "$dateNew" != $dateEnd ]
do
dateOld=$(date -d "$dateNewFmt" +"%Y-%m-%d_%H:%M:%S")
dateNewFmt=$(date -d "$dateNewFmt + 3 hour" +"%H:%M:%S %Y-%m-%d")
dateNew=$(date -d "$dateNewFmt" +%Y-%m-%d_%H:%M:%S)
echo "Start: "$dateOld
echo "End  : "$dateNew
echo " "
echo "python plotRainDiff.py ${addressWrfouts}/wrfout_${domain}_${dateOld} ${addressWrfouts}/wrfout_${domain}_${dateNew} /mnt/disk2/afalcione/OPER_intel/plots/Rain3h_${domain}_"
echo " "
python plotRainDiff_OPER.py ${addressWrfouts}/wrfout_${domain}_${dateOld} ${addressWrfouts}/wrfout_${domain}_${dateNew} /mnt/disk2/afalcione/OPER_intel/plots/Rain3h_${domain}_ &

done


date2End=$(date -d "$dateStart + 48 hour" +%Y-%m-%d_%H:%M:%S)
date2NewFmt=$dateStart
date2New=$dataStart

while [ "$date2New" != $date2End ]
do
date2Old=$(date -d "$date2NewFmt" +"%Y-%m-%d_%H:%M:%S")
date2NewFmt=$(date -d "$date2NewFmt + 1 hour" +"%H:%M:%S %Y-%m-%d")
date2New=$(date -d "$date2NewFmt" +%Y-%m-%d_%H:%M:%S)
echo "Start: "$date2Old
echo "End  : "$date2New
echo " "
echo "python plotCloud_OPER.py ${addressWrfouts}/wrfout_${domain}_${date2Old} ${addressWrfouts}/wrfout_${domain}_${date2New} /mnt/disk2/afalcione/OPER_intel/plots/Clouds_${domain}_"
echo " "
python plotCloud_OPER.py ${addressWrfouts}/wrfout_${domain}_${date2New} /mnt/disk2/afalcione/OPER_intel/plots/Clouds_${domain}_ &

echo " "
echo "python plotCloudTot_OPER.py ${addressWrfouts}/wrfout_${domain}_${date2Old} ${addressWrfouts}/wrfout_${domain}_${date2New} /mnt/disk2/afalcione/OPER_intel/plots/CloudTot_${domain}_"
echo " "
python plotCloudTot_OPER.py ${addressWrfouts}/wrfout_${domain}_${date2New} /mnt/disk2/afalcione/OPER_intel/plots/CloudTot_${domain}_ &

echo " "
echo "python plotGeop_OPER.py ${addressWrfouts}/wrfout_${domain}_${date2Old} ${addressWrfouts}/wrfout_${domain}_${date2New} /mnt/disk2/afalcione/OPER_intel/plots/Clouds_${domain}_"
echo " "
python plotGeop_OPER.py ${addressWrfouts}/wrfout_${domain}_${date2New} /mnt/disk2/afalcione/OPER_intel/plots/Geop_${domain}_ &

echo " "
echo "python plotTemperature_OPER.py ${addressWrfouts}/wrfout_${domain}_${date2Old} ${addressWrfouts}/wrfout_${domain}_${date2New} /mnt/disk2/afalcione/OPER_intel/plots/Temperature_${domain}_"
echo " "
python plotTemperature_OPER.py ${addressWrfouts}/wrfout_${domain}_${date2New} /mnt/disk2/afalcione/OPER_intel/plots/Temperature_${domain}_ &

echo " "
echo "python plotWind_OPER.py ${addressWrfouts}/wrfout_${domain}_${date2Old} ${addressWrfouts}/wrfout_${domain}_${date2New} /mnt/disk2/afalcione/OPER_intel/plots/Wind_${domain}_"
echo " "
python plotWind_OPER.py ${addressWrfouts}/wrfout_${domain}_${date2New} /mnt/disk2/afalcione/OPER_intel/plots/Wind_${domain}_ &

wait
done
done
