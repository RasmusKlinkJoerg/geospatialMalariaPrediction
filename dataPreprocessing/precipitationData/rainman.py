import netCDF4 as nc
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2

from osgeo import gdal, osr, ogr  # Python bindings for GDAL



fn = "2020rain_africa.nc"
ds = nc.Dataset(fn)
# print(ds)

# print("____________")
# print(ds.__dict__)

# print("TIME", ds.__dict__['time'])
# for dim in ds.dimensions.values():
#     print(dim)

# print("_______________________________________")
# for var in ds.variables.values():
#     print(var)

print("_______________________________________")
# float32 precip(time, lat, lon)
precip = ds.variables['precip']

# Make good figure (But is not tiff)
plt.imshow(precip[11, :, :])
plt.savefig('goodfigureForMonth12.tiff')

print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
lon = ds.variables['lon']
lat = ds.variables['lat']
lon = np.array(lon)
lat = np.array(lat)
lon_min = min(np.array(lon))
lon_max = max(np.array(lon))
lat_min = min(np.array(lat))
lat_max = max(np.array(lat))

print(lon_min, lon_max,lat_min, lat_max)



data = np.array(precip)
# print(data[11, 55, 55])
# plt.contourf(data[0, :, :])
# plt.imshow(data[0, :, :])
# plt.show()
# plt.savefig('afr.tiff')


# print(ds.variables['time'])

avg = []
for i in range(data.shape[0]):
    d = data[i, 200, 200]
    # print("asdfasdf", data[i, 200, 200])
    avg.append(d)
print(np.average(avg))

print(data.shape)
data = np.mean(data, axis=0)
print(data.shape)
print("asdfasdf", data[200, 200])
# print(data[0,:20])

# im_new = Image.fromarray(data)
# im_new.save("africaRain14_b.tif")
#
#
# data = np.mean(precip, axis=0)
#
data[data < 0] = -1
plt.imshow(data)
# plt.show()
plt.savefig('africaRain1414141414.tiff')
# print("helle", data[200,200:220])
# print("hello", precip[0:5, 200,200:220])


myImg = data
cv2.imwrite('cv2Image.png', myImg)

cv2.imwrite('greyImage.png', myImg)
grey = cv2.imread('greyImage.png')
imC = cv2.applyColorMap(grey, cv2.COLORMAP_JET)

cv2.imwrite('colImage.png', imC)


#Normalize data
data_normalized = data/np.linalg.norm(data)
cv2.imwrite('cv2ImageNorm.tiff', data_normalized)


 # applyColorMap(im_gray, im_color, COLORMAP_OCEAN);


# #### Convert to Pillow image and save it as tiff

# im_new = Image.fromarray(data)
# im_new.save("data_pillow.tiff")




data = data_normalized

## Make into tiff file with osgeo-gdal, inspired by https://geonetcast.wordpress.com/2022/05/12/creating-a-geotiff-from-a-numpy-array/
# ---------------------------------------------------------------------------------------------------------------------------
# Required modules
# from osgeo import gdal, osr, ogr  # Python bindings for GDAL


# ---------------------------------------------------------------------------------------------------------------------------

def getGeoTransform(extent, nlines, ncols):
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3], 0, -resy]


# Define the data extent (min. lon, min. lat, max. lon, max. lat)

extent = [lon_min, lat_min, lon_max, lat_max]  # South America

# Export the data to GeoTIFF ================================================

# Get GDAL driver GeoTiff
driver = gdal.GetDriverByName('GTiff')

# Get dimensions
nlines = data.shape[0]
ncols = data.shape[1]
# print("nlines", nlines)
nbands = len(data.shape)
data_type = gdal.GDT_Float32  # gdal.GDT_Float32 / gdal.GDT_Int16

# Create a temp grid
# options = ['COMPRESS=JPEG', 'JPEG_QUALITY=80', 'TILED=YES']
grid_data = driver.Create('grid_data', ncols, nlines, 1, data_type)  # , options)

# Write data for each bands
outBand = grid_data.GetRasterBand(1)
outBand.SetNoDataValue(-1)
outBand.WriteArray(data)

# Lat/Lon WSG84 Spatial Reference System
srs = osr.SpatialReference()
srs.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

# Setup projection and geo-transform
grid_data.SetProjection(srs.ExportToWkt())
grid_data.SetGeoTransform(getGeoTransform(extent, nlines, ncols))

# Save the file
file_name = 'my_test_data.tif'
print(f'Generated GeoTIFF: {file_name}')
driver.CreateCopy(file_name, grid_data, 0)

# Close the file
driver = None
grid_data = None

# Delete the temp grid
import os

os.remove('grid_data')

#TODO find ud af om det giver det rigtige format, og så kør det for alle årstal







