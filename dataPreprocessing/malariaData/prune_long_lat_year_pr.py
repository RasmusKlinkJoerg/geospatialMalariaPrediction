import csv
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt

filename = 'long_lat_year_country.csv'
# filename = 'Africa_with_confidential.csv'

intervals = [(0.0, 0.0), (0.000001, 0.2), (0.20000001, 0.49999999), (0.5, 1)]

with open(filename, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    interval_map = {0: [], 1: [], 2: [], 3: []}
    # print(csv_reader)
    for row in csv_reader:
        pr = float(row[4])
        # print(pr)
        index = None
        # print("hello")
        for i, (low, high) in enumerate(intervals):
            if low <= pr <= high:
                index = i

        # print(index)
        interval_map[index].append(row)


threshold = 1822

pruned_long_lat_year_list = []

for vals in interval_map.values():
    # print("vals", vals)

    newlist = sorted(vals, key=lambda d: d[5])

    pruned_list = newlist[:threshold]
    # print(len(pruned_list))
    # print(pruned_list)
    for row in pruned_list:
        pruned_long_lat_year_list.append(row)

print(len(pruned_long_lat_year_list))
print(pruned_long_lat_year_list)

# Write file
with open('pruned_long_lat_year_country.csv', 'w', encoding="utf8", newline='') as f:
    # using csv.writer method from CSV package
    print("hello")
    write = csv.writer(f)
    write.writerows(pruned_long_lat_year_list)

