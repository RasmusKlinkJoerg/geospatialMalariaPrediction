from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

idxs = [0, 20, 30, 40, 50, 60, 70, 80, 90, 100, 111, 112, 113, 114, 115, 116, 121, 122, 123, 124, 125, 126, 200]

land_cover_classes = ['oceans_seas',
                      'open_forest_not_matching_any_of_the_other_definitions',
                      'open_forest_mixed',
                      'open_forest_deciduous_broad_leaf',
                      'open_forest_deciduous_needle_leaf',
                      'open_forest_evergreen_broad_leaf',
                      'open_forest_evergreen_needle_leaf',
                      'closed_forest_not_matching_any_of_the_other_definitions',
                      'closed_forest_mixed',
                      'closed_forest_deciduous_broad_leaf',
                      'closed_forest_deciduous_needle_leaf',
                      'closed_forest_evergreen_broad_leaf',
                      'closed_forest_evergreen_needle_leaf',
                      'moss_and_lichen',
                      'herbaceous_wetland',
                      'permanent_water_bodies',
                      'snow_and_ice',
                      'bare_or_sparse_vegetation',
                      'urban_or_built_up',
                      'cultivated_and_managed_vegetation_or_agriculture',
                      'herbaceous_vegetation',
                      'shrubs',
                      'unknown']

colors = ['#000080', '#648c00', '#929900', '#a0dc00', '#8d7400', '#8db400', '#666000',
          '#007800', '#4e751f', '#00cc00', '#70663e', '#009900', '#58481f', '#fae6a0', '#0096a0',
          '#0032c8', '#f0f0f0', '#b4b4b4', '#fa0000', '#f096ff', '#ffff4c', '#ffbb22', '#282828']

# reverse them so it matches the order on deafrica github - https://github.com/digitalearthafrica/deafrica-sandbox-notebooks/blob/main/Datasets/Landcover_Classification.ipynb
land_cover_classes = land_cover_classes[::-1]
colors = colors[::-1]

file = "landcover_1992onwards_min5examined/3.tiff"


# Open the image
img = Image.open(file)

# Create new rgb image
rgbimg = Image.new("RGBA", img.size)

# Get the size of the image
width, height = rgbimg.size

rgbs = []
for hex in colors:
    hex = hex.lstrip('#')
    rgbs.append(tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4)))

idx_to_color_map = {}
for i, idx in enumerate(idxs):
    idx_to_color_map[idx] = rgbs[i]

# Process every pixel, go through the greyscale image, look up each pixel value and find the color it maps
# to and put that into the new rgb image
for x in range(width):
    for y in range(height):
        greyscale_val = img.getpixel((x, y))
        rgbimg.putpixel((x, y), idx_to_color_map[greyscale_val])

#### Plotting the new rgb image
imarray = np.array(rgbimg)

fig, ax = plt.subplots()
fig.subplots_adjust(left=-0.3, right=0.9)
fig.set_size_inches(10, 5)

ax.imshow(imarray)
# Add custom legend
custom_legend = [plt.Rectangle((0, 0), 1, 1, color=colors[i]) for i in range(len(land_cover_classes))]
ax.legend(custom_legend, land_cover_classes, bbox_to_anchor=(1.0, 1.15), loc='upper left', frameon=False)

plt.tick_params(left=False, right=False, labelleft=False,
                labelbottom=False, bottom=False)
plt.show()

#### Convert to Pillow image and save it as tiff
im_new = Image.fromarray(imarray)
im_new.save("landcover2.tiff")
