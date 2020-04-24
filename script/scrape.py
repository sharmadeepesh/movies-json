import requests
from bs4 import BeautifulSoup
import json

urls = []
count = 0

dump_to_json = []

def get_name(soup):
	meta = soup.find('div',{'class':'page-meta'})
	temp_tags = meta.find_all('a')
	return temp_tags[-1].find('em').text

def get_download_links(soup):
	links = []
	download_soup = soup.find_all('a',{'class':'buttn'})
	for elem in download_soup:
		links.append(elem.get('href'))
	return links

def get_tags(soup):
	tags = []
	meta = soup.find('div',{'class':'page-meta'})
	temp_tags = meta.find_all('a')
	for i in range(0,len(temp_tags)-1):
		tags.append(temp_tags[i].find('em').text)
	return tags

def get_image(soup):
	try:
		try:
			return soup.find('img',{'class':'aligncenter'}).get('src')
		except AttributeError:
			return soup.find('img').get('src')
	except AttributeError:
		return False

def get_details(soup):
	try:
		try:
			return soup.find('p',{'style':'text-align: center;'}).text
		except AttributeError:
			return soup.find('p').text
	except AttributeError:
		return "No information"

def get_json(movie_details, count):
	global dump_to_json
	outfile = open('data.json','w+')
	json.dump(dump_to_json, outfile)

def get_soup(url, i):
	global dump_to_json
	global movie_details
	movie_details = {}
	response = requests.get(url).text
	soup = BeautifulSoup(response,'html.parser')
	tags = get_tags(soup)
	name = get_name(soup)
	details = get_details(soup)
	links = get_download_links(soup)
	image = get_image(soup)
	movie_details[i] = {
		'name': name,
		'tags':tags,
		'details':details,
		'links':links,
		'image':image,
	}
	dump_to_json.append(movie_details)
	get_json(movie_details,count)

def load_urls():
	global urls
	temp_urls = open("sitemap.txt").readlines()
	for url in temp_urls:
		urls.append(url.strip())

if __name__ == '__main__':
	load_urls()
	for i in range(644,len(urls)):
		print("Turn of", i, "out of", len(urls))
		print(urls[i])
		get_soup(urls[i],i)