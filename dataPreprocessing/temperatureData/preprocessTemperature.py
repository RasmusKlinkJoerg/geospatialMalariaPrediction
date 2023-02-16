from os import listdir
from os.path import isfile, join

import numpy as np
from osgeo import gdal, osr, ogr  # Python bindings for GDAL

import cv2

folder_path = "LST2016"

files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
print(len(files))

print(files[0])
file_name = files[0]
file_path = folder_path + "/" + file_name

data = gdal.Open(file_path)
print(type(data))
geoTransform = data.GetGeoTransform()
minx = geoTransform[0]
maxy = geoTransform[3]
maxx = minx + geoTransform[1] * data.RasterXSize
miny = maxy + geoTransform[5] * data.RasterYSize
print([minx, miny, maxx, maxy])

# Define the data extent (min. lon, min. lat, max. lon, max. lat)
lon_min, lat_min, lon_max, lat_max = minx, miny, maxx, maxy
extent = [lon_min, lat_min, lon_max, lat_max]

print(type(data))

print("Raster count:", data.RasterCount)

band = data.GetRasterBand(1)
data_array = band.ReadAsArray()

data_shape = data_array.shape
print(data_array.shape)

snip = data_array[2000, :]


def print_stuff(arr):
    print(np.amin(arr), np.amax(arr))
    print(np.average(arr))
    print(np.median(arr))
    f = arr.flatten()
    s = set(f)
    l = sorted(list(s))
    print("Lowest unique values:", l[:10])
    print("Highest unique values:",  l[-10:])


# print_stuff(snip)
# print_stuff(data_array)

# Converting it to celsius, see here https://gis.stackexchange.com/questions/72524/how-do-i-convert-the-lst-values-on-the-modis-lst-image-to-degree-celsius
def convert_to_celsius(arr):
    arr = arr * 0.02 - 273.15
    return arr

# data_array_celsius = convert_to_celsius(data_array)
# print_stuff(data_array_celsius)

# Get average in each pixel across each file
sum_array = np.zeros(data_shape)
exists_data_array = np.zeros(data_shape)

for file_name in files:
    file_path = folder_path + "/" + file_name
    data = gdal.Open(file_path)
    band = data.GetRasterBand(1)
    data_array = band.ReadAsArray()
    sum_array = np.add(sum_array, data_array)

    # We should should only divide by the number of observed values in each pixel when calculating the average,
    # so we keep track of this
    non_zero = data_array > 0
    non_zero = non_zero.astype(int)
    exists_data_array = np.add(exists_data_array, non_zero)

# If a pixel has never had an observed value, we need to set that entry to 1 so we don't divide by 0
exists_data_array[exists_data_array == 0] = 1

# Calculate the average
avg_array = sum_array/exists_data_array

# print_stuff(avg_array)
# c = convert_to_celsius(avg_array)
# print_stuff(c)


# Make into tiff file with osgeo-gdal =======================================
# inspired by https://geonetcast.wordpress.com/2022/05/12/creating-a-geotiff-from-a-numpy-array/

def getGeoTransform(extent, nlines, ncols):
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3], 0, -resy]

def create_tiff_file(folderpath, data, extent):

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
    output_folder = "tiffTemperatureData/"
    out_file_name = output_folder + folderpath + "_avg" + '.tiff'
    print(f'Generated GeoTIFF: {out_file_name}')
    driver.CreateCopy(out_file_name, grid_data, 0)

    # Close the file
    driver = None
    grid_data = None

    # Delete the temp grid
    import os

    os.remove('grid_data')


create_tiff_file(folder_path, data_array, extent)

data = None
