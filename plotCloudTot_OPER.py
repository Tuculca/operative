from netCDF4 import Dataset
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.cm import get_cmap
import cartopy
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim, cartopy_ylim, latlon_coords, ALL_TIMES)
import numpy
import os
import sys
import pandas
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature


def plot(fileInput, out_folder):
	fileInput = Dataset(fileInput)
	var = "cloudfrac"
	times = getvar(fileInput, "Times")
	get_var = getvar(fileInput, var)
	low = to_np(get_var[0])
	mid = to_np(get_var[1])
	high = to_np(get_var[2])
	cTot = (low + mid + high)/3
	#lats     = getvar(fileInput, "XLAT_U")
	#lons     = getvar(fileInput, "XLONG_U")
	Vmin = to_np(get_var).min()
	Vmax = to_np(get_var).max()
	lats, lons = latlon_coords(get_var)
	cart_proj = get_cartopy(get_var)
	
	
	#colours=['#d2fffe', '#88fefd', '#00c6ff', '#1996ff', '#3c41ff', '#3cbc3d', '#a5d71f', '#ffe600', '#ffc300', '#ff7d00', '#ff0000', '#c80000', '#d464c3', '#b5199d', '#840094', '#dcdcdc', '#b4b4b4', '#8c8c8c', '#5a5a5a']
	#cmap = (mpl.colors.ListedColormap(colours).with_extremes(over='black', under='white'))

	#cmap=plt.get_cmap('Blues', 20)
	#bounds = numpy.linspace(Vmin, Vmax, 21)
	#norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
	
	fig = plt.figure(figsize=(16, 12), dpi=120)
	ax = fig.add_subplot(projection=cart_proj)
	get_var_np = to_np(get_var)
	#get_var_np[get_var_np<=3] = numpy.nan
	ax.set_xlim(cartopy_xlim(get_var))
	ax.set_ylim(cartopy_ylim(get_var))
	clr=ax.pcolormesh(to_np(lons), to_np(lats), cTot, transform=crs.PlateCarree(), cmap='Greys', shading='gouraud', zorder=1, vmin=0, vmax=1)
	#clr2=ax.pcolormesh(to_np(lons), to_np(lats), mid, transform=crs.PlateCarree(), cmap='Greens', shading='gouraud', zorder=2, alpha=0.33)
	#clr3=ax.pcolormesh(to_np(lons), to_np(lats), high, transform=crs.PlateCarree(), cmap='Reds', shading='gouraud', zorder=3, alpha=0.33)
	#ax.contourf(to_np(lons), to_np(lats), get_var_np, levels=bounds, cmap=cmap, norm=norm, zorder=1, transform=crs.PlateCarree())
	#cs = ax.contour(to_np(lons), to_np(lats), get_var_np, levels=bounds, colors='none', zorder=4, transform=crs.PlateCarree())
	
	#land_50m = cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor=cfeature.COLORS['land'])
	#ax.add_feature(land_50m)
	
	#ocean_50m = cfeature.NaturalEarthFeature('physical', 'ocean', '50m', edgecolor='face')
	#ax.add_feature(ocean_50m)
	
	#ax.add_feature(cfeature.BORDERS)
	ax.add_feature(cfeature.COASTLINE, zorder=4)
	
	fname = 'C:/Users/Aless/Downloads/gadm41_ITA_shp/gadm41_ITA_1.shp'
	adm1_shapes = list(shpreader.Reader(fname).geometries())
	ax.add_geometries(adm1_shapes, crs.PlateCarree(), edgecolor='black', facecolor='none', zorder=5) #faceocolor era "gray"

	plt.title("Copertura nuvolosa totale " + str(pandas.to_datetime(to_np(times))))
	
	#cbar = fig.colorbar(mpl.cm.ScalarMappable(cmap=cmap, norm=norm),
	#extend='both',
	#extendfrac='auto',
	#ticks=bounds,
	#spacing='uniform')
	#cbar1=fig.colorbar(clr1)
	#cbar2=fig.colorbar(clr2)
	#cbar3=fig.colorbar(clr3)
	#cbar3.set_label("Clouds", rotation=0)
	#ax.gridlines(color="black", linestyle="dotted")
	plt.savefig(out_folder + str(pandas.to_datetime(to_np(times))).replace(':00:00','') + '.jpg', bbox_inches='tight')

files = sys.argv[1]
output_folder = sys.argv[2] if len(sys.argv)> 2 else 'D:\Model/'
#files = sorted(os.listdir(input_folder))
#for file in files:
#	file_path = input_folder + file
#	ncfiles.append(Dataset(file_path))

	
plot(files, output_folder)
