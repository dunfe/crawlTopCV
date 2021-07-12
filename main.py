from selenium import webdriver
from bs4 import BeautifulSoup
import csv

number_of_page = 24

driver = webdriver.Chrome()
url = 'https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-c10131?exp=4'
file_name = 'two_year'
driver.get(url)

salaries = []


def login():
    login_button = driver.find_element_by_xpath('//*[@id="navbar"]/ul/li[7]/a')
    login_button.click()

    email_field = driver.find_element_by_xpath('//*[@id="form-login"]/p[1]/input')
    email_field.send_keys('email')

    password_field = driver.find_element_by_xpath('//*[@id="form-login"]/p[2]/input')
    password_field.send_keys('password')

    sign_in_button = driver.find_element_by_xpath('//*[@id="form-login"]/p[3]/input')
    sign_in_button.click()

    driver.get(url)

    no_button = driver.find_element_by_xpath('//*[@id="topcv-popover-allow-button"]')
    no_button.click()


def get_salary():
    page_source = BeautifulSoup(driver.page_source, features="html.parser")
    salaries_html = page_source.find_all('span', class_='text-highlight')
    for salary in salaries_html:
        text = salary.text.strip()
        if text != 'Thoả thuận' and text != 'Topcv' and text != '':
            salaries.append(salary.text.strip())


def print_to_csv():
    with open(file_name + '.csv', 'w', newline='', encoding='utf-16') as salaries_file:
        salaries_writer = csv.writer(salaries_file)
        for salary in salaries:
            salaries_writer.writerow([salary])


def get_data():
    for page in range(number_of_page - 1):
        get_salary()
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        next_button = driver.find_element_by_xpath('//*[@id="box-job-result"]/div[2]/nav/ul/li[last()]/a')
        if next_button is not None:
            next_button.click()


if __name__ == '__main__':
    login()
    get_data()
    print_to_csv()


