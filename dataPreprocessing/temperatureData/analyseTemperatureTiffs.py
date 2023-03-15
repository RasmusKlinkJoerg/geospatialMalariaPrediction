from os import listdir
from os.path import isfile, join
import numpy as np
from PIL import Image

folder_path = "tiffTemperatureData"

files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

file_name = files[0]
file_path = folder_path + "/" + file_name


def print_stuff(arr):
    print(np.amin(arr), np.amax(arr))
    # print(np.average(arr))
    # print(np.median(arr))
    print("flattening")
    f = arr.flatten()
    print("making set")
    s = set(f)
    print("sorting")
    l = sorted(list(s))
    print("Lowest unique values:", l[:10])
    print("Highest unique values:", l[-10:])


# print_stuff(snip)
# print_stuff(data_array)

# Converting it to celsius, see here https://gis.stackexchange.com/questions/72524/how-do-i-convert-the-lst-values-on-the-modis-lst-image-to-degree-celsius
def convert_to_celsius(arr):
    arr = arr * 0.02 - 273.15
    return arr


data = None
for file_name in files:
    print(file_name)
    file_path = folder_path + "/" + file_name
    im = Image.open(file_path)
    data = np.array(im)

    print(data.shape)
    print_stuff(data)
    # print(data)

celsius_arr = convert_to_celsius(data)

print("avg_arr")
print_stuff(data)

print("celsius_arr")
print_stuff(celsius_arr)
