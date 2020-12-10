from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from goldmain.models import GoldPrice


def gold_price_from_website(request):
    URL = 'https://www.mennica.com.pl/produkty-inwestycyjne/analiza-rynku-zlota'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    page_html = soup.find_all('div', class_='col-md-3')
    for currency in page_html:
        gold_p = currency.find('div', class_='currency').get_text()
    gold_price = float(gold_p.replace('.', '').replace(',', '.').replace(' ', '').replace('USD', ''))

    g = gold_price
    gold_object = GoldPrice.objects.create(price=g)
    gold_object.save()

    return render(request, "base.html", {"gold_price": gold_price})







