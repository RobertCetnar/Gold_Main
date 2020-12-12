from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import GoldPrice

# Main page
def main_page(reguest):
    return render(reguest, 'base.html')


# Webscraping current gold price and save to database
def gold_price_from_website(request):
    url = 'https://www.mennica.com.pl/produkty-inwestycyjne/analiza-rynku-zlota'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    page_html = soup.find_all('div', class_='col-md-3')
    for currency in page_html:
        gold_p = currency.find('div', class_='currency').get_text()
    gold_price = float(gold_p.replace('.', '').replace(',', '.').replace(' ', '').replace('USD', ''))

    gold_object = GoldPrice.objects.create(price=gold_price)
    gold_object.save()

    return render(request, "gold_price.html", {"gold_price": gold_price})
