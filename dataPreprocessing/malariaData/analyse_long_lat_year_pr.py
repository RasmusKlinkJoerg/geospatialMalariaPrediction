import csv
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt

# filename = 'long_lat_year_with_confidential_from2010to18_size10orGreater.csv'
filename = 'pruned_long_lat_year_pr_examined_with_confidential_from2010to18_size10orGreater.csv'
# filename = 'Africa_with_confidential.csv'

pr_list = []
with open(filename, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        pr_list.append(float(row[4]))

# Plot Histogram on x
# x = np.random.normal(size = 1000)
plt.hist(np.asarray(pr_list, float), bins=100)
plt.gca().set(title='Frequency Histogram')
plt.show()

print("min", min(pr_list), "max", max(pr_list))
print("avg", np.mean(pr_list), "median", np.median(pr_list))

total_lenght = len(pr_list)
print(len(pr_list))
nonzeros = pr_list.count(0.0)
print(nonzeros)

# intervals = [(0, 0), (0.0001, 0.33), (0.333, 0.66), (0.666, 1)]
intervals = [(0, 0), (0.000001, 0.49999999), (0.5, 1)]
# intervals = [(0, 0), (0.000001, 0.5), (0.5000001, 1)]


no_zeros_list = [x for x in pr_list if x != 0.0]
print("no zero list", len(no_zeros_list))
intervals_new = [(0, 0),(0.000001, 0.2), (0.20000001, 0.49999999), (0.5, 1)]


print("------- no zeros intervals")
sum = 0
for (low, high) in intervals_new:
    l = [x for x in pr_list if low <= float(x) <= high]
    print(len(l), "/", len(no_zeros_list), "=", len(l)/len(no_zeros_list))
    sum += len(l)
print("sum", sum)

print("------- with the 0-class")
sum = 0
for (low, high) in intervals_new:
    l = [x for x in pr_list if low <= float(x) <= high]
    print(len(l), "/", total_lenght, "=", len(l)/total_lenght)
    sum += len(l)
print("sum", sum)

no_zero = [x for x in pr_list if x != 0.0]

print("median no zero", np.median(no_zero))
print(len(no_zero))

plt.hist(np.asarray(no_zero, float), bins=100)
plt.gca().set(title='Frequency Histogram')
plt.show()
