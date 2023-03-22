HOME=/mnt/disk2/afalcione/OPER_intel

YEAR_S=$1
YEAR_E=$4
MONTH_S=$2
MONTH_E=$5
DAY_S=$3
DAY_E=$6
HOUR_S=12
HOUR_E=12


cat << End_Of_Namelist1 | sed -e 's/#.*//; s/  *$//' > ${HOME}/WPSv4.4/namelist.wps
&share
 wrf_core = 'ARW',
 max_dom = 2,
 start_date = '${YEAR_S}-${MONTH_S}-${DAY_S}_${HOUR_S}:00:00', '${YEAR_S}-${MONTH_S}-${DAY_S}_${HOUR_S}:00:00',
 end_date   = '${YEAR_E}-${MONTH_E}-${DAY_E}_${HOUR_E}:00:00', '${YEAR_E}-${MONTH_E}-${DAY_E}_${HOUR_E}:00:00', 
 interval_seconds = 10800,
 io_form_geogrid = 2,
 opt_output_from_geogrid_path = '${HOME}/WPSv4.4',
 debug_level = 0,
/

&geogrid
 parent_id         = 1,1,
 parent_grid_ratio = 1,3,
 i_parent_start    = 1,140,
 j_parent_start    = 1,180,
 e_we          = 379,340,
 e_sn          = 431,319,
 geog_data_res = 'modis_lakes+2m','modis_lakes+30s',
 dx = 3000,
 dy = 3000,
 map_proj =  'lambert',
 ref_lat   = 41.916,
 ref_lon   = 12.47,
 truelat1  = 41.916,
 truelat2  = 41.916,
 stand_lon = 12.47,
 geog_data_path = '${HOME}/geog',
 opt_geogrid_tbl_path = '${HOME}/WPSv4.4/geogrid',
 ref_x = 189.5,
 ref_y = 215.5,
/

&ungrib
 out_format = 'WPS',
 prefix = 'FILE',
/

&metgrid
 fg_name = 'FILE',
 io_form_metgrid = 2,
 constants_name = 'TAVGSFC'
 opt_output_from_metgrid_path = '${HOME}/WPSv4.4',
 opt_metgrid_tbl_path = '${HOME}/WPSv4.4/metgrid',
/

&mod_levs
 press_pa = 201300 , 200100 , 100000 ,
             95000 ,  90000 ,
             85000 ,  80000 ,
             75000 ,  70000 ,
             65000 ,  60000 ,
             55000 ,  50000 ,
             45000 ,  40000 ,
             35000 ,  30000 ,
             25000 ,  20000 ,
             15000 ,  10000 ,
              5000 ,   1000
 /


End_Of_Namelist1
