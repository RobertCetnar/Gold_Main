
from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from .models import GoldPrice, Notes
from django.contrib import messages
from .forms import UserRegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
import datetime


# Main page
def home(reguest):
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

    today_prices = GoldPrice.objects.filter(day=datetime.date.today())
    if len(today_prices) == 0:
        gold_object = GoldPrice.objects.create(price=gold_price)
        gold_object.save()
    else:
        pass
    return render(request, "gold_price.html", {"gold_price": gold_price})


# Register for new User
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for : {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


# Login
def login_user(request):
    form = LoginForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are now logged in as : {username}')
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')

    return render(request, 'login.html', {'form' : form})


# Logout
def logout_user(request):
    logout(request)
    messages.success(request, f'You have been logged out')
    return redirect('home')


# Note book for logged user
def note_book(request):
    noteid = int(request.GET.get('noteid', 0))
    notes = Notes.objects.all()

    if request.method == 'POST':
        noteid = int(request.POST.get('noteid', 0))
        title = request.POST.get('title')
        content = request.POST.get('content', '')

        note = Notes.objects.create(title=title, content=content)

        return redirect('note_book')

    if noteid > 0:
        note = Notes.objects.get(pk=noteid)
    else:
        note = ''

    context = {
        'noteid': noteid,
        'notes': notes,
        'note': note
    }
    return render(request, 'note_book.html', context)


def delete_note(request, noteid):
    note = Notes.objects.get(pk=noteid)
    note.delete()

    return redirect('note_book')





















