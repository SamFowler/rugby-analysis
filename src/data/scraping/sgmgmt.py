
import os.path
from bs4 import BeautifulSoup as bs
import requests
import codecs

def get_page_html(url, filepath):
	if check_page_saved(filepath):
		print("fetching from saved")
		return codecs.open(filepath, 'r').read()
	else:
		print("fetching from website")
		html = request_page(url).text
		save_page_html(html, filepath)
		return html

def request_page(url):
	#todo: add exceptions if request failed
	#todo: add time delay to be nice to server
	request = requests.get(url)
	if request:
		return request
	else:
		print("Error reading page")

def save_page_html(html, full_filename):
	#todo: make an check for overwrite wanted input variable
	print(f'Writing page {full_filename}', flush=True)
	soup = bs(html, 'html.parser')
	file = open(full_filename, "w")
	file.write(soup.prettify())
	file.close()

def get_filepath(url):
	return "_".join(url.split('/')[-1].split("?")[-1].split(";")) + '.html'

def check_page_saved(filepath):
	if os.path.isfile(filepath):
		return True
	else:
		return False