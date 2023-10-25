#coding=utf-8
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

import os
import time
import requests
from bs4 import BeautifulSoup
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import NoSuchElementException

url = "https://www.jzpx027.com/education/#/login"

# 调用原有插件
option = webdriver.ChromeOptions()
option.add_argument("--user-data-dir="+r"C:/Users/Z_Q/AppData/Local/Google/Chrome/User Data/")
driver = webdriver.Chrome(chrome_options=option)

# 打开登录页面输入用户名和密码               
driver.get(url)
driver.find_element_by_xpath('//*[@id="pane-member"]/form/div[2]/div/div/input').send_keys('430424198209297239')
driver.find_element_by_xpath('//*[@id="pane-member"]/form/div[3]/div/div/input').send_keys('123456')
driver.find_element_by_xpath('//*[@id="pane-member"]/form/button/span').click()

wait = ui.WebDriverWait(driver,10)
wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/section/div/div[2]/a/div/div[14]/span'))
driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/section/div/div[2]/a/div/div[14]/span').click()

wait.until(lambda driver: driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[2]/div[5]/button/span'))
driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[2]/div[5]/button/span').click()


# 重新获取当前页面url 以及页面源代码并输出
new_url = driver.current_url
print(new_url)
r = requests.get(new_url).text
#soup = BeautifulSoup(r,"html.parser")


#//*[@id="pane-first"]/div[2]/a/div[1]/div

#sleep(50)


