import argparse
import csv
import re


class AirportNotFoundError(Exception):

    def __init__(self, error_string):
        self.error_message = 'Airport not found: '
        self.error_string = error_string


class CountryNotFoundError(Exception):

    def __init__(self, message, error_string):
        self.error_message = 'Country not found'
        self.error_string = error_string

    def __str__(self):
        return 'Error: ' + self.error_message + self.error_string


class MultipleOptionsError(Exception):
    pass


class NoOptionsFoundError(Exception):
    pass


class AirportFounder:

    def __init__(self, arguments):
        self.args = self.check_arguments(arguments)

    def check_arguments(self, arguments):
        args = [('name', arguments.name), ('country', arguments.country), ('iata_code', arguments.iata_code)]
        res = []
        for a in args:
            if a[1] is not None:
                res.append(a)

        if len(res) > 1:
            raise MultipleOptionsError
        elif len(res) == 0:
            raise NoOptionsFoundError
        else:
            return res

    def find(self):
        filename = 'airport-codes_csv.csv'
        with open(filename, encoding='utf-8') as f:
            reader = csv.reader(f)
            header_row = next(reader)
            target_column = -1
            for index, column_header in enumerate(header_row):
                if column_header == self.args[0][0]:
                    target_column = index
            result = []
            pattern = r"[\w\s]*{self.args[0][1]}[\w\s]*"

            for row in reader:
                if re.fullmatch(pattern, row[target_column], flags=re.IGNORECASE):
                    result.append(row)
        if len(result) == 0:
            raise AirportNotFoundError

        for r in result:
            print(r)

parser = argparse.ArgumentParser(description='World Airports')
parser.add_argument('--iata_code')
parser.add_argument('--country')
parser.add_argument('--name')
arguments = parser.parse_args()

a1 = AirportFounder(arguments)
a1.find()