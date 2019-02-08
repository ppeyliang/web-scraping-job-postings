"""
This module is used to srape data science job information on MyCareersFuture.
"""
import pandas as pd
from selenium import webdriver
from time import sleep

driver = webdriver.Chrome('/Users/janice/Developer/chromedriver')

# Create empty DataFrame to store the data.
columns = [
    'title',
    'location',
    'employment_type',
    'level',
    'category',
    'salary_min',
    'salary_max',
    'salary_type',
    'description',
    'requirements'
]
jobs = pd.DataFrame(columns=columns)

# Loop through 100 pages.
count = -1
for page in range(64):
    driver.get('https://www.mycareersfuture.sg/search?search=analyst&sortBy=new_posting_date&page={}'.format(page))
    assert 'MyCareersFuture' in driver.title
    sleep(6)

    for i in range(20):
        try:
            # Extract job title and location.
            title_elem = "//div[@class='card-list']/div[{}]/div/a/div[1]/div/section/div[2]/div/h1".format(i+1)
            loc_elem = "//div[@class='card-list']/div[{}]/div/a/div[1]/div/section/div[2]/div[2]/section/p[1]".format(i+1)

            title = driver.find_element_by_xpath(title_elem).text
            loc = driver.find_element_by_xpath(loc_elem).text

            # Click in job details.
            card = driver.find_element_by_xpath("//div[@class='card-list']/div[{}]".format(i+1))
            try:
                card.click()
            except:
                bar = driver.find_element_by_xpath("//div[@id='snackbar']/div/div/span")
                bar.click()
                sleep(2)
                card.click()
            sleep(8)

            # Extract other detail job information.
            emp_type = driver.find_element_by_id('employment_type').text
            level = driver.find_element_by_id('seniority').text
            cat = driver.find_element_by_id('job-categories').text
            desc = driver.find_element_by_id('job_description').text
            req = driver.find_element_by_id('requirements').text

            # Input None if no salary specified.
            try:
                smin = driver.find_element_by_xpath("//div[@class='lh-solid']/span[1]").text
                smax = driver.find_element_by_xpath("//div[@class='lh-solid']/span[2]").text
                stype = driver.find_element_by_xpath("//div[@class='salary tr-l']/span[3]").text
            except:
                smin = None
                smax = None
                stype = None

            count += 1

            # Save data in DataFrame.
            jobs.loc[count] = [title, loc, emp_type, level, cat, smin, smax, stype, desc, req]

            driver.back()
            sleep(3)

        # Terminate the loop at the last page.
        except:
            break

jobs.to_csv('analyst.csv', index=False)
driver.close()