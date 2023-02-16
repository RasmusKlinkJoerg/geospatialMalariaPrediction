import csv


def filterALLdata():
    new_file = []
    fields = ""

    # Read data and filter it
    with open('ALL_pr.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                fields = row
            line_count += 1
            confidential = False
            for col in row:
                if col == "NA":
                    confidential = True
            if confidential:
                continue
            continent = row[9]
            if continent != "Africa":
                continue
            new_file.append(row)

            # if line_count == 100:
            #     break

    # Write file
    with open('Africa_open_access.csv', 'w', encoding="utf8", newline='') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(new_file)

    ##Test
    for i, row in enumerate(new_file):
        print(i, row)
    print(len(new_file))
    print(fields)
    print(new_file[0])


def prune_data():
    new_file_map = {}
    new_file = []
    fields = ""

    # Read data and filter it
    with open('Africa_open_access.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                fields = row
                line_count += 1
                continue

            # print(row[11])
            start_year = int(row[11])
            # print(start_year)
            if start_year < 2008:
                continue
            species = row[19]
            if species == 'P. vivax':
                continue
            print(species)

            site_name = row[3]
            lat = row[4]
            long = row[5]
            start_month = row[10]
            survey_id = (site_name, lat, long, start_year, start_month, species)
            lower_age = row[14]
            upper_age = row[15]
            examined = int(row[16])
            positive = int(float(row[17]))

            # if examined < 58:
            #     continue

            # print(lower_age, upper_age,examined,positive)
            if survey_id in new_file_map:
                new_file_map[survey_id][14] = min(new_file_map[survey_id][14], lower_age)
                new_file_map[survey_id][15] = max(new_file_map[survey_id][15], upper_age)
                new_file_map[survey_id][16] = int(new_file_map[survey_id][16]) + examined
                new_file_map[survey_id][17] = int(float(new_file_map[survey_id][17])) + positive
            else:
                new_file_map[survey_id] = row

            line_count += 1

            # new_file.append(row)

    long_lat_year = []
    for i, row in enumerate(new_file_map.values()):
        start_year = int(row[11])
        lat = row[4]
        long = row[5]
        examined = int(row[16])
        positive = int(float(row[17]))
        pr = positive/examined
        long_lat_year.append((i, float(long), float(lat), start_year, pr))

    new_file_values = new_file_map.values()
    print("Length", len(new_file_values))
    print(fields)

    # Write file
    with open('Africa_open_access_pruned_14.csv', 'w', encoding="utf8", newline='') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(new_file_values)

    # Write file
    with open('long_lat_year.csv', 'w', encoding="utf8", newline='') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(long_lat_year)


prune_data()






