# Precipitation (rain) data: 

The dataset can be found at the following url:
https://psl.noaa.gov/mddb2/makePlot.html?variableID=1627&fileID=532575

It contains 0.25x0.25-degree (i.e. about 30x30km) resolution image of monthly precipitation of each month from January 1891 to December 2019.
On the website you can select "Create Composite" and then choose the wanted time range, 
when selected wait until the data has updated and the correct dates is displayed above the map on screen, 
then click on "Download subset of data defined by options".
We have chosen january to december for each year from 2005 to 2019.
We can also choose the region, and we choose africa as the region. 
Other selections (which are selected as default on the website):
- Boundaries: Geophysical, 
- Projection: Cylindrical Equidistant 

The region Africa has the following geografic extent:
Africa: `lon_min`, `lon_max`, `lat_min`, `lat_max = -19.875`, `114.875`, `-39.875`, `39.875`

# Testing: 
- With print statements we have checked that min and max values are matching on encoding and decoding side, 
 i.e. in rainman.py and land_cover_extraction.ipynb.
- Manual inspection test on decoding side (land_cover_extraction.ipynb) indicates we get the correct location. It was tested the same way as Temperature data.



Url to different versions of the dataset:
https://psl.noaa.gov/data/gridded/data.gpcc.html
