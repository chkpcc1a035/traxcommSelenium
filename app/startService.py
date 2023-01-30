from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from time import perf_counter
from bs4 import BeautifulSoup
import time
import json
import requests
from collections import OrderedDict
from ta_captcha_solver.ta_captcha_solver import TACaptchaSolver
from RPA.Browser.Selenium import Selenium
import base64
class TraxcommSenleniumService():

    chrome = Selenium()
    chromiumService = Service(r'./win_webdriver/chromedriver109')
    chrome = webdriver.Chrome(service=chromiumService)
    chrome.get("https://webportal.tgt.hk/customer/login/index.php")

    img_base64 =chrome.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele, 0, 0, ele.width ,ele.height);
    return cnv.toDataURL('image/jpeg').substring(22);    
    """, chrome.find_element(By.XPATH,'/html/body/div/div[2]/div/div[1]/form/img'))

    with open("captcha.png", 'wb') as image:
        image.write(base64.b64decode(img_base64))

    file = {'file': open('captcha.png', 'rb')} 

    api_key = 'Input Your 2captcha KEY' 
    payload = {
    'key': 'e23aed51f8032ef551f8e493628851b0',
    }
    captcha_text = ''

    response = requests.post('http://2captcha.com/in.php', files = file, params = payload) 

    print(f'response:{response.text}')

    if response.ok and response.text.find('OK') > -1:

        captcha_id = response.text.split('|')[1]
        print('[captcha]' + captcha_id)
        time.sleep(45)

        response = requests.get(f'http://2captcha.com/res.php?key=e23aed51f8032ef551f8e493628851b0&action=get&id={captcha_id}')

        if response.text.find('CAPCHA_NOT_READY') > -1: 
                time.sleep(10)
        elif response.text.find('OK') > -1:
            captcha_text = response.text.split('|')[1]
        else:
            print('Captcha Error!')

    print('[captcha_text]' + captcha_text)

    emailIn = chrome.find_element(By.XPATH, '/html/body/div/div[2]/div/div[1]/form/div[1]/input')

    passIn = chrome.find_element(By.XPATH, '/html/body/div/div[2]/div/div[1]/form/div[2]/input')

    captcha = chrome.find_element(By.XPATH, '/html/body/div/div[2]/div/div[1]/form/input')

    submitButton = chrome.find_element(By.XPATH, '/html/body/div/div[2]/div/div[1]/form/div[3]/input')

    emailIn.send_keys('product@traxcomm.hk')

    passIn.send_keys('Poc20230131')

    captcha.send_keys(captcha_text)

    submitButton.click()

    time.sleep(10)


