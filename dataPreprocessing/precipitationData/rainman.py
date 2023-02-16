import os

import netCDF4 as nc
import numpy as np

from osgeo import gdal, osr, ogr  # Python bindings for GDAL

def get_data(filepath):
    ds = nc.Dataset(filepath)

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
    coords = (lon_min, lat_min, lon_max, lat_max)

    data = np.array(precip)

    # Take the average across the 12 months
    data = np.mean(data, axis=0)

    # Change NoDataValue to -1
    data[data < 0] = -1
    return data, coords

# Make into tiff file with osgeo-gdal =======================================
# inspired by https://geonetcast.wordpress.com/2022/05/12/creating-a-geotiff-from-a-numpy-array/

def getGeoTransform(extent, nlines, ncols):
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3], 0, -resy]

def create_tiff_file(filepath, data, coords):
    # Define the data extent (min. lon, min. lat, max. lon, max. lat)
    lon_min, lat_min, lon_max, lat_max = coords
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
    output_folder = "tiffRainData/"
    input_file_name = filepath.split("\\")[1]
    input_file_name = input_file_name.split(".")[0]
    out_file_name = output_folder + input_file_name + '.tiff'
    print(f'Generated GeoTIFF: {out_file_name}')
    driver.CreateCopy(out_file_name, grid_data, 0)

    # Close the file
    driver = None
    grid_data = None

    # Delete the temp grid
    import os

    os.remove('grid_data')



# Loop through all files ===============
directory = "ncRainData"
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    print(filepath)
    data, coords = get_data(filepath)
    create_tiff_file(filepath, data, coords)


