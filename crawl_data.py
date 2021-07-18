from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import csv
from statistics import mean
from re import findall
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

email = 'qngnud@gmail.com'
password = 'svT5anz!q.6S#9L'

# chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome()

url = 'https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-c10131'

majors = ['Công nghệ thông tin']


def login(_email, _password):
    driver.get(url)
    print('Logging in..')
    login_button = driver.find_element_by_xpath('//*[@id="navbar"]/ul/li[7]/a')
    login_button.click()

    email_field = driver.find_element_by_xpath('//*[@id="form-login"]/p[1]/input')
    email_field.send_keys(_email)

    password_field = driver.find_element_by_xpath('//*[@id="form-login"]/p[2]/input')
    password_field.send_keys(_password)

    sign_in_button = driver.find_element_by_xpath('//*[@id="form-login"]/p[3]/input')
    sign_in_button.click()

    driver.get(url)

    no_button = driver.find_element_by_xpath('//*[@id="topcv-popover-allow-button"]')
    no_button.click()


def search_by_major():
    print('Searching...')

    for name in majors:
        major_field = driver.find_element_by_xpath('//*[@id="select2-category-container"]')
        major_field.click()

        major_input_field = driver.find_element_by_xpath('/html/body/span/span/span[1]/input')
        major_input_field.send_keys(name)
        major_input_field.send_keys(Keys.ENTER)

        search_button = driver.find_element_by_xpath('//*[@id="frm-search-job"]/div[1]/div[2]/button')
        search_button.click()

        number_of_page = get_number_of_pages()
        job_urls = get_job_url(number_of_page)
        data = get_data_of_url(job_urls)
        # data = get_data(number_of_page)
        print_to_csv(data, name)


def scroll_to_bottom():
    seo_box = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "seo-box")))
    actions = ActionChains(driver)
    actions.move_to_element(seo_box).perform()


def get_number_of_pages():
    pagination = driver.find_elements_by_xpath('//*[@id="box-job-result"]/div[2]/nav/ul/li')
    array_len = len(pagination)
    this_number = pagination[array_len - 2].text
    if this_number.isdigit():
        print('Number of pages: ', this_number)
        return int(this_number)
    print('There is no result!')
    return 0


def get_all_url():
    page_source = BeautifulSoup(driver.page_source, features="html.parser")
    jobs = page_source.find_all('h4', class_='job-title')
    all_job_url = []
    for job in jobs:
        job_url = job.contents[1].get('href')
        if job_url not in all_job_url:
            all_job_url.append(job_url)
    return all_job_url


def get_salary():
    salaries = []
    page_source = BeautifulSoup(driver.page_source, features="html.parser")
    salaries_html = page_source.find_all('span', class_='text-highlight')

    for salary in salaries_html:
        salary_text = salary.contents[2].contents[0].contents[0].get_text().strip()
        text = salary_text.strip()
        if text != 'Thoả thuận' and text != 'Topcv' and text != '':
            numbers = findall(r'\b\d+\b', text)
            numbers_converted = list(map(int, numbers))
            numbers_mean = mean(numbers_converted)
            salaries.append(numbers_mean)

    return salaries


def print_to_csv(data, file_name):
    print('Print to csv...')
    with open(file_name + '.csv', 'w', newline='', encoding='utf-16') as salaries_file:
        header = ['Tiêu đề', 'Mức lương', 'Thời gian', 'Số lượng', 'Chức vụ', 'Yêu cầu kinh nghiệm',
                  'Yêu cầu giới tính', 'Địa điểm làm việc']
        salaries_writer = csv.DictWriter(salaries_file, delimiter=',', lineterminator='\n', fieldnames=header)
        salaries_writer.writeheader()
        for job in data:
            try:
                salaries_writer.writerow(
                    {header[0]: job[0], header[1]: job[1], header[2]: job[2], header[3]: job[3], header[4]: job[4],
                     header[5]: job[5]
                        , header[6]: job[6], header[7]: job[7]})
            finally:
                continue


def get_data_of_url(all_job_url):
    all_data = []
    count = 1
    for _url in all_job_url:
        print('Getting job: ', count)
        count += 1

        job_data = []
        driver.get(_url)

        page_source = BeautifulSoup(driver.page_source, 'html.parser')
        job_title = page_source.find('h1', class_='job-title text-highlight bold')
        box_info_job = page_source.find('div', id='box-info-job')

        if box_info_job is not None:
            info_job = box_info_job.find_all('span')

            if '' in info_job:
                info_job.remove('')

            job_salary_text = info_job[0].get_text().strip()
            numbers = findall(r'\b\d+\b', job_salary_text)
            if job_salary_text == 'Thỏa thuận' or job_salary_text is None or numbers is None or len(numbers) <= 0:
                continue

            numbers_converted = list(map(int, numbers))
            numbers_mean = mean(numbers_converted)

            job_salary = numbers_mean
            job_time = info_job[1].get_text().strip()
            job_hr = info_job[2].get_text().strip()
            job_position = info_job[3].get_text().strip()
            job_exp = info_job[4].get_text().strip()
            job_gender = info_job[5].get_text().strip()
            job_location = info_job[6].get_text().strip()

            job_data = [job_title.get_text().strip(), job_salary, job_time, job_hr
                , job_position, job_exp, job_gender, job_location]

        all_data.append(job_data)

    return all_data


def get_job_url(number_of_page):
    all_job_url = []
    if number_of_page > 0:
        for page in range(number_of_page):
            print('Getting url of page: ', page + 1)
            this_page_urls = get_all_url()
            all_job_url += this_page_urls
            scroll_to_bottom()
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.LINK_TEXT, '›')))
                element.click()

            except TimeoutException:
                continue
    return all_job_url


def get_data(number_of_page):
    print('Get data...')
    salaries = []
    if number_of_page > 0:
        for page in range(number_of_page):
            print('Getting page: ', page + 1)

            salary_of_this_page = get_salary()

            if len(salary_of_this_page) > 0:
                salaries = salaries + salary_of_this_page
            scroll_to_bottom()
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.LINK_TEXT, '›')))
                element.click()

            except TimeoutException:
                continue

    return salaries


def crawl_data():
    login(email, password)
    search_by_major()
