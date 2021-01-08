
from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from .models import GoldPrice, Notes, Forecast, ForecastVerification
from django.contrib import messages
from .forms import UserRegisterForm, LoginForm, ForecastForm
from django.contrib.auth import authenticate, login, logout
import datetime
from django.contrib.auth.decorators import login_required


# Main page
def home(reguest):
    return render(reguest, 'home.html')


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
    if request.method == 'POST':
        form = LoginForm(request.POST)
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
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# Logout
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')


# Note book for logged user
@login_required
def note_book(request):
    noteid = int(request.GET.get('noteid', 0))
    notes = Notes.objects.filter(note_author=request.user)

    if request.method == 'POST':
        noteid = int(request.POST.get('noteid', 0))
        title = request.POST.get('title')
        content = request.POST.get('content', '')
        note_author = request.user
        note = Notes.objects.create(
            title=title,
            content=content,
            note_author=note_author)
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


# Delete Note
def delete_note(request, noteid):
    note = Notes.objects.get(pk=noteid)
    note.delete()
    return redirect('note_book')


# Create Forecast for logged user
@login_required
def forecast(request):
    if request.method == 'POST':
        form = ForecastForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, 'Your Forecast has been saved !')
            return redirect('forecast')
    else:
        form = ForecastForm()
    context = {
        'form': form
    }
    return render(request, 'forecast.html', context)


# Verification of User Forecasts
@login_required
def forecast_verification(request):
    lista_prognoz = []
    forecast_to_verification = Forecast.objects.filter(author=request.user).order_by('-created')
    for f in forecast_to_verification:
        create_date = f.created
        gold_price = GoldPrice.objects.filter(day=create_date)
        for g in gold_price:
            create_gold_price = g.price
        forecast_price = f.gold_forecast
        ver_date = f.verification_date
        gold_price_verificate = GoldPrice.objects.filter(day=ver_date)
        if len(gold_price_verificate) > 0:
            for v in gold_price_verificate:
                verificate_gold_price = v.price
        else:
            verificate_gold_price = 0
        if create_gold_price > 0 and forecast_price > 0 and verificate_gold_price > 0:
            if create_gold_price > forecast_price and create_gold_price > verificate_gold_price:
                result_of_verification = True
                accuracy = int((verificate_gold_price - create_gold_price) / (forecast_price - create_gold_price) * 100)
            elif create_gold_price < forecast_price and create_gold_price < verificate_gold_price:
                result_of_verification = True
                accuracy = int((verificate_gold_price - create_gold_price) / (forecast_price - create_gold_price) * 100)
            elif create_gold_price == forecast_price and create_gold_price == verificate_gold_price:
                result_of_verification = True
                accuracy = 100
            elif create_gold_price <= forecast_price and create_gold_price > verificate_gold_price:
                result_of_verification = False
                accuracy = 0
            elif create_gold_price < forecast_price and create_gold_price >= verificate_gold_price:
                result_of_verification = False
                accuracy = 0
            elif create_gold_price >= forecast_price and create_gold_price < verificate_gold_price:
                result_of_verification = False
                accuracy = 0
            elif create_gold_price > forecast_price and create_gold_price <= verificate_gold_price:
                result_of_verification = False
                accuracy = 0

            verificated = ForecastVerification.objects.filter(forecast_to_verification_id=f.id)
            if len(verificated) == 0:
                verification = ForecastVerification.objects.create(verification_result=result_of_verification,
                                                                   accuracy=accuracy,
                                                                   forecast_to_verification_id=f.id)
        else:
            result_of_verification = 'No data'
            accuracy = 'No data'
        ocena_prognozy = {
            'forecast_to_verification': forecast_to_verification,
            'create_date': create_date,
            'create_gold_price': create_gold_price,
            'forecast_price': forecast_price,
            'ver_date': ver_date,
            'verificate_gold_price': verificate_gold_price,
            'result_of_verification': result_of_verification,
            'accuracy': accuracy
        }
        lista_prognoz.append(ocena_prognozy)
    context = {
        'lista_prognoz': lista_prognoz
    }
    return render(request, 'forecast_history.html', context)
