import csv


c_set = set()
c_list = []

with open('Africa_open_access.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # print(line_count)
        # # print(row)
        country = row[7]
        # print(country)
        c_set.add(country)
        c_list.append(country)

print(c_set)
print(len(c_set))

from collections import Counter


def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]

print(most_frequent(c_list))

print(c_list.count("Kenya"))

