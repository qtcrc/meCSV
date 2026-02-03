import argparse
import csv


class RawRow:
    def __init__(self, country, year,
                 gdp, gdp_growth,
                 inflation, unemployment,
                 population, continent,
                 src):
        self.country = country
        self.year = year
        self.gdp = gdp
        self.inflation = inflation
        self.unemployment = unemployment
        self.population = population
        self.continent = continent
        self.src = src


class DataEntry:
    def __init__(self, gdp, inflation, unemployment, population,
                 src=-1):
        self.gdp = float(gdp)
        self.inflation = float(inflation)
        self.unemployment = float(unemployment)
        self.population = int(population)
        self.src = int(src)

    def compress(self):
        return (self.gdp, self.inflation,
                self.unemployment, self.population,
                self.src)


def data_reader(files):
    for csv_file_path in files:
        with open(str(csv_file_path)) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            colums = reader.__next__()

            print("columns ->", colums)
            for row in reader:
                print(row)
                yield RawRow(*tuple(row), src=csv_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--files", dest="files",
                        nargs="*", help="csv files to parce")
    parser.add_argument("-r", "--report", dest="report_type",
                        nargs=1, help="average-gdp")
    args = parser.parse_args()

    print(args)

    db = {}  # ("Russia", 2020) : [(a, b, c, d), (a, b, c, d)]
    country_list = {}
    sources = {}
    sources_count = 0

    for row in data_reader(args.files):
        new_key = (row.country, row.year)
        new_entry = DataEntry(
            row.gdp, row.inflation, row.unemployment,
            row.population)

        # index src string
        if (row.src not in sources):
            sources[row.src] = sources_count
            sources_count += 1
        new_entry.src = sources[row.src]

        # assure unique continent for country
        if country_list.get(row.country) != row.continent:
            if (row.country not in country_list):
                country_list[row.country] = row.continent
            else:
                print("---\nWRONG CONTINENT:", row.country, "\n",
                      "old:", country_list[row.country],
                      "/ new:", row.continent)
                print(new_entry, "\n---")

        if new_key in db:
            # old_entry = db[new_key]
            print("DUBLICATED entry:", row)

        db.setdefault((row.country, row.year), []).append(new_entry.compress())

    # map continents
    continents = {}
    for (country, cont) in country_list.items():
        continents.setdefault(cont, set()).add(country)

    print(sources)
    print(continents)
    print(db)
    print(country_list)
