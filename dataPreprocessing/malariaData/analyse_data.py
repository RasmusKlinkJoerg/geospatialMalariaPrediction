import csv
from collections import Counter

import numpy as np

c_set = set()
c_list = []
year_list = []
examined_list = []

filename = 'Africa_open_access.csv'
# filename = 'Africa_with_confidential.csv'

with open(filename, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # print(line_count)
        # # print(row)
        if line_count == 0:
            line_count = 1
            continue
        country = row[7]
        start_year = row[11]
        examined = int(row[16])
        # print(country)
        c_set.add(country)
        c_list.append(country)
        year_list.append(start_year)
        examined_list.append(examined)
        line_count+=1

print("Number of surveys", len(year_list), len(c_list))

print(c_set)
print("Number of unique countries", len(c_set))


def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]


freq_country = most_frequent(c_list)
print("Most frequent country", freq_country, c_list.count(freq_country))

freq_year = most_frequent(year_list)
print("Most frequent year", freq_year, year_list.count(freq_year))

print("Survey sizes: min max avg median", min(examined_list), max(examined_list),
      np.average(examined_list), np.median(examined_list))

freq_size = most_frequent(examined_list)
print("Most frequent size", freq_size, examined_list.count(freq_size))