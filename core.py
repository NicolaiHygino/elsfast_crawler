from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv


def make_soup(url):
	html = urlopen(url)
	soup = BeautifulSoup(html, 'lxml')
	return soup


soup = make_soup('https://www.eslfast.com/robot/')

a_tag = soup.find('p', { 'class':'MsoNormal' }).find_all('a')

topics_links = []
for a in a_tag:
	href = a['href'] 
	topics_links.append('https://www.eslfast.com/robot/{}'.format(href))


conversation_links = []
for topic_url in topics_links:
	topic_soup = make_soup(topic_url)
	
	a_tag_topic = topic_soup.find('font', { 'size':'6' }).find_all('a')
	
	for a in a_tag_topic:
		href = a['href']
		url = topic_url[:-len(href)+2]
		conversation_links.append( ''.join([url, href]) )


with open('links_to_scrap.csv', 'w', newline='') as f:
	fieldnames = ['url']
	thewriter = csv.DictWriter(f, fieldnames=fieldnames)

	thewriter.writeheader()
	for pos in range(len(conversation_links)):
		thewriter.writerow({
			'url':conversation_links[pos]
			})
