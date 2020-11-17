import csv


def import_csvs(fpath1, fpath2):
    # This module takes information from the Multi-Tier Energy Survey
    # and adds to the CENI file
    data1 = []
    data2 = []

    with open(fpath1) as csvfile1:
        reader = csv.reader(csvfile1, delimiter=',')

        for row in reader:
            data1 += [row]

    with open(fpath2) as csvfile2:
        reader = csv.reader(csvfile2, delimiter=',')

        for row in reader:
            data2 += [row]

    return data1, data2


def closest_grid(d1, d2):
    # This module adds the ID of the closest grid in the CENI file to the
    # survey file

    # CENI - [grid_id, lon, lat]
    ceni_geocrds = [x[0:3] for x in d1]

    # survey - [lat, lon, cluster_id, hh_id]
    svy_geocrds = [x[0:2] + x[4:6] for x in d2]

    # Loop through each set of geocoordinates in survey file and allocate
    # closest ID in CENI file

    retval = []
    combined_data = []

    for svy in svy_geocrds[1:]:

        svylat = float(svy[0])
        svylon = float(svy[1])
        cluster_id = svy[2]
        hh_id = svy[3]
        min_dist = 1000
        min_id = 0
        min_lat = 0
        min_lon = 0

        for ceni in ceni_geocrds[1:]:
            cenlat = float(ceni[2])
            cenlon = float(ceni[1])

            dist = ((svylat - cenlat) ** 2 + (svylon - cenlon) ** 2) ** (1 / 2)

            if dist < min_dist:
                min_dist = dist
                min_id = ceni[0]
                min_lat = cenlat
                min_lon = cenlon

        val = [svylat, svylon, cluster_id, hh_id, min_dist, min_id, min_lat, min_lon]
        retval += [val]
        combined_data += [svy + val]

    return combined_data, retval


def write_csv(data, fname):
    with open(fname, mode='w', newline='') as write_file:
        writer = csv.writer(write_file, delimiter=',', quotechar='"')

        for row in data:
            writer.writerow(data)
        # writer.writerows(data)


def set_file_paths():
    fpath1 = "C:/Users/User/Desktop/CSVreader/CNN_CENI_KEN_3840_ALL.csv"
    fpath2 = "C:/Users/User/Desktop/CSVreader/Selected_HH_variables.csv"

    return fpath1, fpath2


def run():
    fpath1, fpath2 = set_file_paths()
    [d1, d2] = import_csvs(fpath1, fpath2)
    [d3, d4] = closest_grid(d1, d2)

    print(d3[1:5])
    print(d4[1:2])
    write_csv(d3, "C:/Users/User/Desktop/CSVreader/Selected_HH_variables.csv")
