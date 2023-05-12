import csv
from collections import Counter

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

c_set = set()
c_list = []
year_list = []
examined_list = []
pr_list = []
country_pr_list = []

# filename = 'Africa_open_access.csv'
filename = 'Africa_with_confidential.csv'

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
        pr = float(row[18])
        # print(country)
        c_set.add(country)
        c_list.append(country)
        year_list.append(start_year)
        examined_list.append(examined)
        pr_list.append(pr)
        country_pr_list.append((country, pr))
        line_count += 1

print("Number of surveys", len(year_list), len(c_list))

print(c_set)
print("Number of unique countries", len(c_set))

print("Average pr in Africa", np.average(pr_list))


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


# country_counts = {}
def getCountryCounts():
    for country in c_list:
        count = c_list.count(country)
        country_counts[country] = count
    print(country_counts)


country_counts = {'Somalia': 1599, 'Kenya': 1855, 'Burkina Faso': 1210, 'Tanzania': 3578, 'Malawi': 589, 'Zambia': 492,
                  'Senegal': 867, 'Uganda': 1379, 'Central African Republic': 7, 'Sudan': 153, 'Mozambique': 1617,
                  'Burundi': 919, 'Comoros': 12, 'Guinea': 327, 'Niger': 34, 'Ethiopia': 286, 'Guinea-Bissau': 23,
                  "Côte d'Ivoire": 347, 'Gambia': 392, 'Zimbabwe': 158, 'Democratic Republic of the Congo': 856,
                  'South Africa': 53, 'Congo': 13, 'Cameroon': 700, 'Ghana': 736, 'Liberia': 303, 'Swaziland': 5,
                  'Nigeria': 625, 'Mayotte': 9, 'Benin': 783, 'Madagascar': 1253, 'Equatorial Guinea': 86, 'Gabon': 41,
                  'Mali': 356, 'South Sudan': 7, 'Sierra Leone': 370, 'Eritrea': 3, 'Chad': 8, 'Mauritania': 86,
                  'Rwanda': 742, 'Togo': 503, 'Djibouti': 2, 'Angola': 971, 'Cape Verde': 15, 'Morocco': 8,
                  'Sao Tome And Principe': 30}

country_pr_map = {}
for country in c_list:
    country_pr_map[country] = []

for (country, pr) in country_pr_list:
    country_pr_map[country].append(pr)

avg_pr_per_country_map = {}
for country, pr_list in country_pr_map.items():
    avg_pr_per_country_map[country] = np.average(pr_list)

print(avg_pr_per_country_map)

mmapm = {'Somalia': 0.06487404627892432, 'Kenya': 0.20211342318059297, 'Burkina Faso': 0.4731657024793388,
         'Tanzania': 0.17006291224147568, 'Malawi': 0.2781867572156197, 'Zambia': 0.12878699186991868,
         'Senegal': 0.06561626297577855, 'Uganda': 0.3029823060188543, 'Central African Republic': 0.4572857142857143,
         'Sudan': 0.06991699346405228, 'Mozambique': 0.29515572047000616, 'Burundi': 0.24437062023939063,
         'Comoros': 0.36416666666666675, 'Guinea': 0.389177370030581, 'Niger': 0.17828529411764707,
         'Ethiopia': 0.028472727272727275, 'Guinea-Bissau': 0.26422608695652167, "Côte d'Ivoire": 0.2129268011527378,
         'Gambia': 0.33503826530612246, 'Zimbabwe': 0.052018354430379735,
         'Democratic Republic of the Congo': 0.2788009345794393, 'South Africa': 0.033837735849056604, 'Congo': 0.3754,
         'Cameroon': 0.25188571428571427, 'Ghana': 0.2898850543478261, 'Liberia': 0.30097260726072605, 'Swaziland': 0.0,
         'Nigeria': 0.28436000000000006, 'Mayotte': 0.009166666666666665, 'Benin': 0.280088122605364,
         'Madagascar': 0.07082713487629688, 'Equatorial Guinea': 0.3960709302325581, 'Gabon': 0.3385292682926829,
         'Mali': 0.31495786516853935, 'South Sudan': 0.14745714285714287, 'Sierra Leone': 0.42702540540540546,
         'Eritrea': 0.03333333333333333, 'Chad': 0.1432, 'Mauritania': 0.011647674418604651,
         'Rwanda': 0.015087061994609163, 'Togo': 0.3050741550695825, 'Djibouti': 0.06755, 'Angola': 0.1609041194644696,
         'Cape Verde': 0.04341333333333333, 'Morocco': 0.0, 'Sao Tome And Principe': 0.13655000000000003}

year_list = [int(x) for x in year_list]
sns.histplot(year_list)
plt.xticks(rotation=45)
plt.show()

# letter_counts = Counter(year_list)
# df = pd.DataFrame.from_dict(letter_counts, orient='index')
# df.plot(kind='bar')
# plt.show()
