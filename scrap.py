# -*- coding: utf-8 -*-


import pandas as pd
from bs4 import BeautifulSoup as bs
from time import sleep
from selenium import webdriver
import requests
import pandas as pd

driver = webdriver.Chrome(executable_path='chromedriver.exe')
req = driver.get(
    'https://www.etsy.com/listing/514988912/beach-tote-bags-for-women-canvas-print?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sr_gallery-1-45')
sleep(5)
cust_name = []
review_list = []

for r in range(0, 35):

    # response = requests.get(req).text

    # soup = bs(response, 'lxml')

    page = requests.get(req).text

    soup = bs(page.content, 'html.parser')
    soup.prettify()

    names = soup.find_all('a', class_="wt-text-link wt-mr-xs-1")

    for i in range(0, len(names)):
        cust_name.append(names[i].get_text())

    reviews = soup.find_all('p', class_="wt-text-truncate--multi-line wt-break-word")

    for i in range(0, len(reviews)):
        review_list.append(reviews[i].get_text())
        reviews[i].get_text().replace('/n', ' ')
    sleep(34)

    review_list[:] = [titles.lstrip('\n') for titles in review_list]

    review_list[:] = [titles.rstrip('\n') for titles in review_list]

    next_button = driver.find_element_by_xpath('//*[@id="reviews"]/div[2]/nav/ul/li[position() = last()]/a')
    next_button.click()
    sleep(5)



df = pd.DataFrame()

df['Customer Name'] = cust_name

df['Reviews'] = review_list

df.to_csv(r'D:/Competitions_2020_2021/Apscript/task/:/Review_data.csv', index=True)

























#conecting to  sql db


conn = sql.connect('reviews.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM statetable")

for record in cursor:
    print (record)

