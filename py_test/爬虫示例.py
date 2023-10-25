from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

chrome_options=Options()
chrome_options.add_argument('--headless')         # 无界面
chrome_options.add_argument('--no-sandbox')       # 解决DevToolsActivePort文件不存在报错问题
chrome_options.add_argument('--disable-gpu')      # 禁用GPU硬件加速。如果软件渲染器没有就位，则GPU进程将不会启动。
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920,1080')      # 设置当前窗口的宽度和高度
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument('--hide-scrollbars')

def get_domain_registrant(driver, domain):
    url = f'http://whois.chinaz.com/{domain}'
    driver.get(url)
    try:
        target_element = driver.find_element_by_xpath(
            '//*[@id="whois_info"]/li[4]/div[2]/span')
            
    except:
        return "NULL"
    return target_element.get_attribute('innerHTML')

#获取查询跳转页面的url
# def new_url(tel):
#     browser.get("https://www.baidu.com/")
#     ele=browser.find_element_by_xpath('//*[@id="kw"]')
#     ele.send_keys(tel)
#     ele.submit()
#     sleep(7)
#     tel_url=browser.current_url     
#     return tel_url