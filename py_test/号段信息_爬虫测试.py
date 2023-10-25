import os
import re
from selenium import webdriver
from requests.models import Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

chrome_options=webdriver.ChromeOptions()
chrome_options.headless=True
chrome_options.add_argument('--headless')         # 无界面
chrome_options.add_argument('--no-sandbox')       # 解决DevToolsActivePort文件不存在报错问题
chrome_options.add_argument('--disable-gpu')      # 禁用GPU硬件加速。如果软件渲染器没有就位，则GPU进程将不会启动。
chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument('--window-size=1920,1080')      # 设置当前窗口的宽度和高度
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument('--hide-scrollbars')
browser=webdriver.Chrome('chromedriver')

#url地址拼接
def new_url(i):
    old_url1='https://www.ip138.com/mobile.asp?mobile='
    old_url2='&action=mobile'
    new_url=old_url1+i+old_url2
    return new_url

#获取号段归属地和运营商的Xpath和Text信息
def tel_pro_ope_msg(tel):
    browser.get(new_url(tel))
    try:
        tel_p=browser.find_element_by_xpath(
            '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[2]/span')
        tel_o=browser.find_element_by_xpath(
            '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[2]/span')
    except:
        return "NULL"
    return tel_p.get_attribute('innerHTML'),tel_o.get_attribute('innerHTML')

#运营商正则匹配
ope_pattern=re.compile('电信|联通|移动')
#号段正则匹配
seg_pattern=re.compile('1[0-9]{6}')

#打开号段归属地的文件
f=open('C:/Users/Z_Q/Desktop/tel_pro_city——20220516.txt',mode='w+',encoding='utf-8')
#打开号码源文件并进行查询
path='C:/Users/Z_Q/Desktop/tel' 
with open(path,'rt',encoding='utf-8') as files:
    for tel in files:
        browser.get(new_url(tel))
        tel_row=tel.split("\n",-1)
        segment_no=seg_pattern.findall(tel_row[0])
        for i in segment_no:
            ar=tel_pro_ope_msg(tel)[0]
            tel_province_city=ar.split("&nbsp;",-1)
            if tel_province_city[0]=="":
                tel_province_city[1]=tel_province_city[0]="NULL"
            elif tel_province_city[1]=="":
                tel_province_city[1]=tel_province_city[0]
            else:       
                tel_province_city[0]=tel_province_city[0]
                tel_province_city[1]=tel_province_city[1]
            operator=tel_pro_ope_msg(tel)[1]
            tel_province_city[1]=re.sub("市","",tel_province_city[1])
            tel_ope=ope_pattern.findall(operator)
            for j in tel_ope:
                f.writelines([i,' ',j,' ',tel_province_city[0],' ',tel_province_city[1]])
                f.writelines('\n')
browser.close()
f.close()
