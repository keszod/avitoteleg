 # -*- coding: utf8 -*-
import datetime
import time
import json
import traceback
import csv
import requests
import urllib.parse
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup as bs
from time import sleep

def proxy_switch():
	sub_driver = create_driver(proxy=False,headless=False)
	sub_driver.get('https://mobileproxy.space/reload.html?proxy_key=c7aa0fba80e2aba694be5d21d2ccd011&format=json')

	return

def get_page(url,driver,fast_exit=False,attemps=0):
	driver.get(url)
	sleep(5)
	
	soup = bs(driver.page_source,'html.parser')
	#driver.back()
	sleep(2)

	return soup


def test(content,name):
	with open(name,'w',encoding='utf-8') as f:
		f.write(content)


def parse_item():
	soup = bs(driver.page_source,'html.parser')
	test(driver.page_source,'test.html')
	title = '<b>'+soup.find('h1').text+'</b>'
	description = soup.find('div','style-item-description-pL_gy').text.replace('Описание',' ')
	if len(description) > 800:
		description = description[:850]+'....'
	description = '<b>Описание</b>: \n' + description

	print(description)
	address = soup.find('span','style-item-address__string-wt61A').text.split(',')[0]
	photo = soup.find('img','css-1qr5gpo').get('src')
	price = soup.find('span','style-price-value-string-rWMtx').text

	text = title + '\n\n' + description + '\n' + '<b>Адресс</b>: '+address+'\n\n'+'<b>Стоимость</b>: '+price
	send_message(text,photo,driver.current_url)

def parse():
	links = []
	with open('key_words.txt','r') as file:
		key_words = file.read().splitlines()
	parse_links = ['https://www.avito.ru/moskva/orgtehnika_i_rashodniki?cd=1&f=ASgCAgECAUXGmgwVeyJmcm9tIjoyMDAwMCwidG8iOjB9&s=104','https://www.avito.ru/moskva/oborudovanie_dlya_biznesa?f=ASgCAgECAUXGmgwVeyJmcm9tIjoyMDAwMCwidG8iOjB9&s=104']
	
	while True:
		for i in range(2):
			driver.get(parse_links[i])
			print(parse_links[i])
			items = driver.find_elements(By.XPATH,'//div[@data-marker="item"]')
			test(driver.page_source,'test.html')
			for i in range(len(items)):
				item = items[i]
				soup = bs(item.get_attribute('innerHTML'),'html.parser')

				date = soup.find('div',{"data-marker" : "item-date"}).text
				if 'мин' in date and int(date.split()[0]) <= 20:
					link = 'https://www.avito.ru'+soup.find('a').get('href')
					title = soup.find('h3').text

					for key_word in key_words:
						if key_word.lower() in title.lower():
							break
					else:
						continue

					if link in links:
						continue

					driver.get(link)
					print(link)
					content = driver.find_element(By.XPATH,'//li[@class="params-paramsList__item-appQw"]').text
					links.append(link)

					if 'ибп' in content.lower():
						continue
					
					parse_item()
					sleep(2)
					
					driver.back()
					items = driver.find_elements(By.XPATH,'//div[@data-marker="item"]')

			sleep(3)
		sleep(30)

def send_message(text,photo,link):
	token = '934338853:AAHfa6yri8ktKUUtgIRZGaVgKMrn2oB_GLk'
	chat_id = '917403306'
	print(text)

	keyboard = []
	keyboard.append({'url':link,'text':'Ссылка'})
	keyboard = {'inline_keyboard':[keyboard]}
	keyboard = json.dumps(keyboard)
	#text = urllib.parse.quote_plus(text)
	url = f'https://api.telegram.org/bot{token}/sendPhoto?caption={text}&photo={photo}&chat_id={chat_id}&parse_mode=html&reply_markup='+keyboard
	print(url)
	requests.get(url)



				

if __name__ == '__main__':
	options = uc.ChromeOptions()
	options.headless=True
	options.add_argument('--headless')
	driver = uc.Chrome(options=options)
	driver.implicitly_wait(30)
	parse()

