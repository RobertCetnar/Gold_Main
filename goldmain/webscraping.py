
import requests
from bs4 import BeautifulSoup


def parse_price(price):
    return float(price.replace('.', '').replace(',', '.').replace(' ', '').replace('USD', ''))


def gold_price_from_website():
    URL = 'https://www.mennica.com.pl/produkty-inwestycyjne/analiza-rynku-zlota'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    page_html = soup.find_all('div', class_='col-md-3')
    for currency in page_html:
        gold_price = parse_price(currency.find('div', class_='currency').get_text())
        print(f'Aktualna Cena zlota ($): {gold_price}')



gold_price_from_website()



