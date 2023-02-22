# Temperature data: 

The dataset can be requested at the following url:
https://appeears.earthdatacloud.nasa.gov/task/area

# The following request was made:
- In "Select the layers to include in the sample" input `MOD11A2.006`, then new selections pop up, click on `LST_Day_1km`.
- Choose Start Date:	01-01-2000 and End Date:	01-01-2021 
- (The underlying dataset on the website is spanning from 18/2 2000 until present (so our start date must 
      also have gotten cut off at 18/2 2000, but it was possible to choose 1/1 2000) )


The geoextent was chosen manually on the website by drawing a rectangle on the map:
`lon_min`, `lat_min`, `lon_max`, `lat_max = -21.516`, `-36.9916`, `54.0083`, `39.099` ,
which is around Africa.

The dataset contains land surface temperature with 1x1 km resolution for every 8 days in the chosen time span.
An in depth description of the dataset can be found here: https://lpdaac.usgs.gov/products/mod11a2v006/

# Testing: 
- With print statements we have checked that min and max values are matching on encoding and decoding side, 
 i.e. in preprocessTemperature.py and land_cover_extraction.ipynb.
- Manual inspection test on decoding side (land_cover_extraction.ipynb) indicates we get the correct location. 
It was tested the same way as precipitation data.


