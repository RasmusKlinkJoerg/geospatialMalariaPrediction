import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import cv2

from osgeo import gdal, osr, ogr  # Python bindings for GDAL

fn = "ncRainData/2020rain_africa.nc"
ds = nc.Dataset(fn)

# Format of precip data: float32 precip(time, lat, lon)
precip = ds.variables['precip']

lon = ds.variables['lon']
lat = ds.variables['lat']
lon = np.array(lon)
lat = np.array(lat)
lon_min = min(np.array(lon))
lon_max = max(np.array(lon))
lat_min = min(np.array(lat))
lat_max = max(np.array(lat))

# print(lat_min, lat_max, lon_min, lon_max)

data = np.array(precip)
print("min val", np.amin(data), "max val", np.amax(data))

# test 2 (27.3684, -17.479)
# test 12 12_12.6756, -1.8496.png, 200
# test 100 100_27.2562, -16.7782.png
# 2: (27.3684, -17.479), 12: (12.6756, -1.8496) , 100 : (27.2562, -16.7782)
# 200: "200_8.8124, 3.7315.png"

test_lat, test_lon = (27.3684, -17.479)
testPrecip = precip[11, test_lat, test_lon]
print("testPrecip", testPrecip)

avg_test = []
for i in range(data.shape[0]):
    testPrecip = precip[i, test_lat, test_lon]
    avg_test.append(testPrecip)
print("Test Average on coordinates", np.average(avg_test))

offset = 100
offset_array = []
for offset_lon in range(offset):
    current_row = []
    for offset_lat in range(offset):
        current_lat = test_lat - offset * 0.25 * 0.5 + offset_lat * 0.25
        current_lon = test_lon - offset * 0.25 * 0.5 + offset_lon * 0.25
        month_vals = []
        # for i in range(data.shape[0]):
        #     testPrecip = precip[i, current_lat, current_lon]
        #     month_vals.append(testPrecip)
        # avg = np.average(month_vals)
        avg = precip[0, current_lat, current_lon]
        current_row.append(avg)
    offset_array.append(current_row)
offset_array = np.array(offset_array)
# print("offset_array:", offset_array, offset_array.shape)
plt.imshow(offset_array)
plt.show()

# Testing that the average is made correctly, i.e. with np.mean
avg = []
idxs = (200, 230)
for i in range(data.shape[0]):
    d = data[i, idxs[0], idxs[1]]
    # print("asdfasdf", data[i, 200, 200])
    avg.append(d)
print(idxs, "Average on nc file", np.average(avg))

# Take the average across the 12 months
data = np.mean(data, axis=0)
print("min val", np.amin(data), "max val", np.amax(data))
print(idxs, "Average from np.mean", data[idxs[0], idxs[1]])
print(data.shape)

# Change NoDataValue to -1
data[data < 0] = -1
print("min val", np.amin(data), "max val", np.amax(data))


# Make into tiff file with osgeo-gdal =======================================
# inspired by https://geonetcast.wordpress.com/2022/05/12/creating-a-geotiff-from-a-numpy-array/

def getGeoTransform(extent, nlines, ncols):
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3], 0, -resy]


# Define the data extent (min. lon, min. lat, max. lon, max. lat)
extent = [lon_min, lat_min, lon_max, lat_max]  # South America

# Export the data to GeoTIFF ===

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


