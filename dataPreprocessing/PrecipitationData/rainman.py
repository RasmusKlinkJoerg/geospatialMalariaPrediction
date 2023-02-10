import netCDF4 as nc
import matplotlib
import matplotlib.pyplot as plt

fn = "2015rain_africa.nc"
ds = nc.Dataset(fn)
print(ds)

print("____________")
print(ds.__dict__)

# print("TIME", ds.__dict__['time'])
for dim in ds.dimensions.values():
    print(dim)

print("_______________________________________")
for var in ds.variables.values():
    print(var)

print("_______________________________________")
#float32 precip(time, lat, lon)
precip = ds.variables['precip']
data = precip[:]*1
print(data[12, 55, 55])
# plt.contourf(data[0, :, :])
plt.imshow(data[0,:,:])
# plt.show()
plt.savefig('afr.png')

print()
print(ds.variables['time'])
print("asdfasdf", data[0, 200, 200])
