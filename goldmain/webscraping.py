
import requests
from bs4 import BeautifulSoup


def gold_price_from_website():
    url = 'https://www.mennica.com.pl/produkty-inwestycyjne/analiza-rynku-zlota'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    page_html = soup.find_all('div', class_='col-md-3')
    for currency in page_html:
        gold_p = currency.find('div', class_='currency').get_text()
    print (f'Aktualna Cena zlota ($): {gold_p}')

    # Otrzymujemy string z roznymi znakami, aby zmienic na float pozbywam sie znakow

    gold_price = float(gold_p.replace('.', '').replace(',', '.').replace(' ', '').replace('USD', ''))
    print(f'Aktualna Cena zlota ($): {gold_price}')

gold_price_from_website()





