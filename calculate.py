import csv
from statistics import mean, variance


def read_it_file(file_name):
    _data = []
    with open(file_name + '.csv', 'r', encoding='utf-16') as salaries_file:
        salaries_reader = csv.reader(salaries_file)
        for row in salaries_reader:
            _data.append(row)

    return _data


def read_file(file_name):
    all_salary = []
    with open(file_name + '.csv', 'r', encoding='utf-16') as salaries_file:
        salaries_reader = csv.reader(salaries_file)
        line_count = 0
        for row in salaries_reader:
            line_count += 1
            all_salary.append(float(row[0]))

    return all_salary


def calculate_mean(name):
    data = read_file(name)

    if len(data) > 0:
        _sum = sum(data)
        mean_result = mean(data)
        print('Mean of ' + name + ' is: ' + str(mean_result))


def calculate_variance(name):
    data = read_file(name)

    if len(data) > 0:
        variance_result = variance(data)
        print('Variance of ' + name + ' is: ' + str(variance_result))


def cal(majors):
    for major in majors:
        calculate_mean(major)
        calculate_variance(major)
