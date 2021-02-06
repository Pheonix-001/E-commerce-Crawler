import csv
import requests
from bs4 import BeautifulSoup

from DataWriter import DataWriter

class Olx(DataWriter):

    name = ''
    details = []

    def __init__(self, name):
        self.name = name

    
    def get_url(self):
        fname = self.name
        fname = fname.replace(' ', '-')
        url = 'https://www.olx.in/items/q-{}?isSearchCall=true'
        url = url.format(fname)
        return url


    def get_soup(self):
        url = self.get_url()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup


    def get_details(self):
        print("\n Fetching data on Olx.in...")
        soup = self.get_soup()
        items = soup.find_all('li', class_='EIR5N')

        for item in items:

            # Title
            title = item.find('span', class_='_2tW1I').text.strip()

            # Price 
            price = item.find('span', class_='_89yzn').text

            # Location
            loc = item.find('span', class_='tjgMj').text

            # Date 
            date = item.find('span', class_='zLvFQ').text

            # Buy link
            parent = item.find('a', class_='fhlkh')
            link = parent['href']
            link = 'https://www.olx.in' + link

            d = (title, price, loc, date, link)
            self.details.append(d)


    def store_data(self):

            w = DataWriter('OLX.csv')

            w.writer(self.details)