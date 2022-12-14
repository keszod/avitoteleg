 # -*- coding: utf8 -*-
import datetime
import time
import json
import traceback
import csv
import requests
import ssl
import urllib.parse
from datetime import datetime
from time import sleep

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_

CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""


class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)

session = requests.session()
adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
session.mount("https://", adapter)


def get_page(url):
	headers = get_headers()
	print(url)
	r = session.get(url,headers=headers)
	test(r.text,'test.html')


	return r.json()

def get_headers():
	with open('headers.txt','r',encoding='utf-8') as file:
		headers = file.read()
		headers = headers.splitlines()
		py_headers = {}
		for header in headers:
			key,value = header.split(': ')
			py_headers[key] = value

		return py_headers

def test(content,name):
	with open(name,'w',encoding='utf-8') as f:
		f.write(content)

def parse():
	ids = []
	with open('key_words.txt','r',encoding='utf-8-sig') as file:
		key_words = file.read().splitlines()
	
	parse_link = 'https://m.avito.ru/api/11/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&locationId=621540&priceMin=20000&sort=date&page=1&lastStamp=1670232360&display=list&limit=100&pageId=H4sIAAAAAAAA_0q0MrSqLrYyNLRSKskvScyJT8svzUtRss60MjYyMjG3rgUEAAD__6Us-7UhAAAA&presentationType=serp'

	while True:
		categories = ['orgtehnika_i_rashodniki','oborudovanie_dlya_biznesa']
		try:
			for key_word in key_words:
				url = parse_link+'&query='+key_word
				data = get_page(url)
				test(str(json.dumps(data)),'test.html')
				items = data['result']['items']
				
				for item in items:
					item = item['value']
					title = item['title']
					date = (datetime.now() - datetime.fromtimestamp(item['time']))
					print(title,date,date.seconds//60)
					if date.days >= 1 or date.seconds >= 60*60:
						break
					link = 'https://www.avito.ru'+item['uri_mweb']

					if item['id'] in ids:
						continue
					
					for key_word in key_words:
						if key_word in title:
							break
					else:
						continue

					for category in categories:
						if category in link:
							break

					else:
						continue

					price = item['price']
					address = item['address']
					photo = item['galleryItems'][0]['value']['678x678']
					text = title + '\n\n' + '<b>????????????</b>: '+address+'\n\n'+'<b>??????????????????</b>: '+price
					send_message(text,photo,link)
					send_message(text,photo,link,'618939593')
					
					ids.append(item['id'])
				
				sleep(5)
		except:
			sleep(60*3)
			continue
		sleep(60*3)

def send_message(text,photo,link,chat_id='917403306'):
	token = '934338853:AAHfa6yri8ktKUUtgIRZGaVgKMrn2oB_GLk'
	#chat_id = '917403306'
	#chat_id = '618939593'
	print(text)

	keyboard = []
	keyboard.append({'url':link,'text':'????????????'})
	keyboard = {'inline_keyboard':[keyboard]}
	keyboard = json.dumps(keyboard)
	#text = urllib.parse.quote_plus(text)
	url = f'https://api.telegram.org/bot{token}/sendPhoto?caption={text}&photo={photo}&chat_id={chat_id}&parse_mode=html&reply_markup='+keyboard
	print(url)
	requests.get(url)



				

if __name__ == '__main__':
	parse()