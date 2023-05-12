import csv

import numpy as np


def filterALLdata(input_file_name, output_file_name):
    new_file = []
    fields = ""

    # Read data and filter it
    with open(input_file_name, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                fields = row
            line_count += 1
            confidential = False
            lat = row[4]
            long = row[5]
            start_month = row[10]
            lower_age = row[14]
            upper_age = row[15]
            examined = row[16]
            positive = row[17]
            important = [lat, long, start_month, lower_age, upper_age, examined, positive]
            for feature in important:
                if feature == "NA":
                    confidential = True
            if confidential:
                continue
            continent = row[9]
            if continent != "Africa":
                continue
            lat = row[4]
            long = row[5]
            if float(lat) == 0 and float(long) == 0:  # Filter out if on "zero island"
                continue
            new_file.append(row)

    # Write file
    with open(output_file_name, 'w', encoding="utf8", newline='') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(new_file)

    # ##Test
    # for i, row in enumerate(new_file):
    #     print(i, row)
    # print(len(new_file))
    # print(fields)
    # print(new_file[0])


filterALLdata("TANZ_plus.csv", "Tanzania_with_confidential_2.csv")


def prune_data():
    new_file_map = {}
    fields = ""
    pr_list = [] # for printing average pr

    # Read data and filter it
    with open('Africa_with_confidential.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                fields = row
                line_count = 1
                continue

            start_year = int(row[11])
            # if start_year != 2010 and start_year != 2015:
            if start_year < 1992:
                continue
            species = row[19]
            if species == 'P. vivax':
                continue

            examined = int(row[16])
            if examined < 50:
                continue

            site_name = row[3]
            lat = row[4]
            long = row[5]
            start_month = row[10]
            survey_id = (site_name, lat, long, start_year, start_month, species)
            lower_age = row[14]
            upper_age = row[15]
            positive = int(float(row[17]))

            # Update values if it is an existing survey id
            if survey_id in new_file_map:
                new_file_map[survey_id][14] = min(new_file_map[survey_id][14], lower_age)
                new_file_map[survey_id][15] = max(new_file_map[survey_id][15], upper_age)
                new_file_map[survey_id][16] = int(new_file_map[survey_id][16]) + examined
                new_file_map[survey_id][17] = int(float(new_file_map[survey_id][17])) + positive
            else:  # It is a new survey id
                new_file_map[survey_id] = row
            line_count += 1

    # # Extra pruning
    # for key, row in new_file_map.items():
    #     examined = int(row[16])
    #     positive = int(float(row[17]))
    #     pr = positive / examined

    long_lat_year = []
    for i, row in enumerate(new_file_map.values()):
        start_year = int(row[11])
        lat = row[4]
        long = row[5]
        country = row[7]
        examined = int(row[16])
        positive = int(float(row[17]))
        pr = positive / examined
        pr_list.append(pr) # for printing average pr
        long_lat_year.append((i, float(long), float(lat), start_year, pr, examined, country))

    new_file_values = new_file_map.values()

    print("len(pr_list)", len(pr_list)) # for printing average pr
    print("np.average(pr_list)", np.average(pr_list)) # for printing average pr

    # Write file
    with open('Africa_with_confidential_pruned_someName.csv', 'w', encoding="utf8", newline='') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(new_file_values)

    # Write file
    with open('long_lat_year_country.csv', 'w', encoding="utf8", newline='') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(long_lat_year)


prune_data()


# -------- Getting difference between two csv files ---------
# Below Not working
def get_different_rows(file1, file2, output_file_name):
    new_file = []
    fields = []
    rows1 = []
    with open(file1, encoding="utf8") as csv_file1, open(file2, encoding="utf8") as csv_file2:
        csv_reader_1 = csv.reader(csv_file1, delimiter=',')
        print(csv_reader_1)
        len1 = len(list(csv_reader_1))
        for row in csv_reader_1:
            print(row)
            rows1.append(row)
        csv_reader_2 = csv.reader(csv_file2, delimiter=',')
        print(csv_reader_2)
        len2 = len(list(csv_reader_2))
        line_count = 0
        for row in csv_reader_2:
            print(line_count)
            print(row)
            # Still get the row names
            if line_count == 0:
                print("hello")
                fields = row
                new_file.append(row)
                line_count = 1
                continue
            # Only get rows that are not in file 2.
            if row in rows1:
                continue
            new_file.append(row)
            line_count += 1
    # Write new file
    len_out = len(new_file)
    print(len1, len2, len_out, "should be ", len1 - len2)
    with open(output_file_name, 'w', encoding="utf8", newline='') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(new_file)

# get_different_rows("Africa_with_confidential.csv", "Africa_open_access.csv", "Africa_only_confidential.csv")
