from selenium import webdriver
import pandas as pd

import requests
from lxml.html import fromstring
from time import sleep


targetPageURL = 'https://digital.ces.tech/exhibitors'
driver = webdriver.Chrome('/mnt/d/PycharmProjects/excelAutomation/driver/chromedriver.exe')
url = driver.get(targetPageURL)
sleep(10)

pageNum = 147

companyList = []

for i in range(0,pageNum):
    print(f"page_{i}")
    company = driver.find_element_by_class_name('company-header__title').text
    companyList.append(company)
    print(companyList)
    #driver.find_element_by_xpath("//a[@class='c-glyph mwf-pagination__page-link mwf-pagination__page-arrow-link']").click()
    driver.find_element_by_css_selector("#event-tools > div.content-body > div.view-container.page-container > drawer-container > div > div > sponsor-directory-page > div > div > div > div.session-search__content.content-container > div > div.search-header-bar > div.search-header-bar__search-options.search-chips--no-chips > div.search-header-bar__pagination.search-header-bar__pagination--top > ul > li.mwf-pagination__page-arrow.mwf-pagination__page-arrow--right > button").click()
    sleep(2)
    print('next')


for i in range(0,len(companyList)):
    companyList.append(driver.find_elements_by_class_name('company-header__title')[i].text)
    



a