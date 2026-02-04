from itertools import count
import os
import argparse
import csv
import tabulate as TB
import logging


class RawRow:
    def __init__(self, country, year,
                 gdp, gdp_growth,
                 inflation, unemployment,
                 population, continent,
                 src):
        self.country = str(country)
        self.year = int(year)
        self.gdp = float(gdp)
        self.inflation = float(inflation)
        self.unemployment = float(unemployment)
        self.population = int(population)
        self.continent = str(continent)
        self.src = str(src)


def genIDs():
    return map(lambda x: x+1, count(0))


def validate_files(files):
    OK = True
    for filepath in files:
        if not os.path.exists(filepath):
            logging.error(f"Not found: {filepath}")
            OK = False
    return OK


def make_reader(files):
    if not validate_files(files):
        return None

    return iter(_reader(files))


def _reader(files):

    for csv_file_path in files:
        with open(str(csv_file_path)) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            columns = next(reader)  # skip columns
            # print("columns:", columns)

            for row in reader:
                yield RawRow(*tuple(row), src=csv_file_path)


def report_avg_gdp(reader):
    db = {}  # {"country" : {2020 : [gdp, gdp]}}
    results = []

    # build db
    for row in reader:
        db.setdefault(row.country, {}).setdefault(
            row.year, []).append(row.gdp)

    # make report
    for country, gdps in db.items():
        for year, values in gdps.items():
            # merge yearly reports
            gdps[year] = sum(values) / len(values)

        results.append([country, sum(gdps.values()) / len(gdps)])

    # sort
    results.sort(key=lambda g: -g[1])
    results.insert(0, ["country", "gdp"])

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--files", dest="files",
                        nargs="*", help="csv files to parce", required=True)
    parser.add_argument("-r", "--report", dest="report_type",
                        nargs=1, help="reprots methods", required=True,
                        choices=["average-gdp"])
    # TODO filters
    # parser.add_argument("-y", "--year-range", dest="list_year",
    #                     nargs=1, required=False,
    #                     help="example: '2000' or '2000-2025'")
    # parser.add_argument("-c", "--countrys", dist="list_country",
    #                     nargs=1, required=False,
    #                     help="example: '!Russia, Belarus, Greece'")
    # parser.add_argument("-C", "--continents", dist="list_continents",
    #                     nargs=1, required=False,
    #                     help="example: 'Europe, Africa, Asia'")

    args = parser.parse_args()
    reader = make_reader(args.files)
    if not reader:
        quit(1)

    table = []
    match args.report_type[0]:
        case "average-gdp":
            table = report_avg_gdp(reader)
            print(TB.tabulate(table,
                              headers="firstrow", tablefmt="psql",
                              floatfmt=".2f", showindex=genIDs())
                  )
        case _:
            assert False
