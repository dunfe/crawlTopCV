import csv
from visualization import get_data_question_five


def print_data():
    for localtion in ['Hà Nội', 'Hồ Chí Minh']:
        data = get_data_question_five(localtion)
        print_to_csv(data, localtion)


def print_to_csv(data, file_name):
    print('Print to csv...')
    with open(file_name + '.csv', 'w', newline='', encoding='utf-16') as salaries_file:
        salaries_writer = csv.writer(salaries_file)
        for salary in data:
            try:
                salaries_writer.writerow([salary])
            finally:
                continue
