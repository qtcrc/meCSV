import argparse
import csv
import tabulate as TB


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


def reader(files):
    for csv_file_path in files:
        with open(str(csv_file_path)) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            colums = reader.__next__()

            print("columns ->", colums)
            for row in reader:
                yield RawRow(*tuple(row), src=csv_file_path)


def report_avg_gdp(files):
    db = {}  # {"country" : {2020 : [gdp, gdp]}}
    results = []

    # build db
    for row in reader(files):
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

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--files", dest="files",
                        nargs="*", help="csv files to parce")
    parser.add_argument("-r", "--report", dest="report_type",
                        nargs=1, help="average-gdp")
    args = parser.parse_args()

    print(args)

    table = report_avg_gdp(args.files)
    headers = ["Country", "avg GDP(desc)"]
    print(TB.tabulate(table,
                      headers=headers, tablefmt="github",
                      floatfmt=".2f", showindex=True)
          )
