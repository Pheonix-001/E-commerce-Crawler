import csv
import requests
from bs4 import BeautifulSoup

from DataWriter import DataWriter

class Amazon(DataWriter):

    name = ''
    details = []
    
    # Take product name using constructor
    def __init__(self, name):
        self.name = name
    

    # Generate url
    def get_url(self):

        self.name = self.name.replace(' ', '+')
        temp = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss'
        url = temp.format(self.name)
        url += '&page{}'

        return url


    # Fetch all pages for a particular search and store into a 'page_list' list
    def get_pages(self):
        page_list = []
        temp = self.get_url()

        for i in range(2):

            if i == 0:
                page_list.append(temp)
            else:
                ss = self.get_soup(temp)
                nextBtn = ss.find_all('li', class_='a-last')

                next_link = nextBtn[0].a.get('href')
                next_url = self.get_url().format(next_link)
                temp = next_url
                page_list.append(temp)

        return page_list


    # Generate soup for a particular url
    def get_soup(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup


    # Fetch all items from a page and store into a 'items' list
    def get_items(self):
        items = []
        page = self.get_pages()

        for i in range(len(page)):
            temp = self.get_soup(page[i])
            item = temp.find_all('div', {'data-component-type': 's-search-result'})
            
            for a in item:
                items.append(a)
        return(items)


    # It fetch all products details and store into a 'details' list
    def get_details(self):
        print("\n Fetching data on Amazon.in...")
        items = self.get_items()
        p_title = ' '
        p_rating = ''
        p_review = ''
        p_price = ''
        p_delivery_date = ''
        p_delivery_type = ''
        p_link = ''

        for item in items:

            # Title
            title = item.h2.a.text
            p_title = title.strip()

            # Rating
            try:
                rating = item.find('span', class_='a-icon-alt')
                p_rating = rating.text
            except AttributeError:
                p_rating = 'rating not available'

            # Review count
            try:
                review = item.find('span', class_='a-size-base')
                p_review = review.text
            except AttributeError:
                p_review = 'review not available'

            # Price
            try:
                parent = item.find('span', class_="a-price")
                price = parent.find('span', class_='a-offscreen')
                p_price = price.text
            except AttributeError:
                p_price = 'price not available'

            # Delivery Date 
            try:
                delivery_date = item.find('span', class_='a-text-bold')
                p_delivery_date = delivery_date.text
            except AttributeError:
                p_delivery_date = 'delivery date not available'

            # Delivery type
            # Using multiple try-catch for different types of tags
            try:
                delivery_type = item.find('span', {"aria-label": "FREE Delivery by Amazon"})
                p_delivery_type = delivery_type.text.strip()
            except:
                try:
                    delivery_type = item.find('span', {"aria-label": "FREE Delivery over ₹499. Fulfilled by Amazon."})
                    p_delivery_type = delivery_type.text.strip()
                except AttributeError:
                    p_delivery_type = "Delivery type not available"

            # Buy link
            parent = item.h2.a
            title_link = parent.get('href')
            buy_link = "https://www.amazon.in/" + title_link
            p_link = buy_link

            d = (p_title, p_price, p_rating, p_review, p_delivery_date, p_delivery_type, p_link)
            self.details.append(d)


    # Store all prducts details into a CSV file
    def store_data(self):

        rowtitle = ["Product Name", "Price", "Rating", "No. of reviews", "Delivery Date", "Delivery Type", "Buy link"]
        w = DataWriter('Amazon.csv', rowtitle)
        w.writer(self.details)
        
