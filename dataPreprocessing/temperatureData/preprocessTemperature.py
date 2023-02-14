from os import listdir
from os.path import isfile, join

import numpy as np
from osgeo import gdal, osr, ogr  # Python bindings for GDAL

import cv2





folder_path = "LST2015"

files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

print(files[0])
file_name = files[0]
file_path = folder_path +"/"+file_name

data = gdal.Open(file_path)
print(type(data))
geoTransform = data.GetGeoTransform()
minx = geoTransform[0]
maxy = geoTransform[3]
maxx = minx + geoTransform[1] * data.RasterXSize
miny = maxy + geoTransform[5] * data.RasterYSize
print([minx, miny, maxx, maxy])

print(type(data))

print("Raster count:", data.RasterCount)

band = data.GetRasterBand(1)
data_array = band.ReadAsArray()

print(data_array.shape)

snip = data_array[2000, :]
# print(snip)
print(min(snip), max(snip))

print(np.amin(data_array), np.amax(data_array))


#TODO get average in each pixel across each file



data = None

