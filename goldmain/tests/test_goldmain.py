
import pytest
from django import urls
from django.contrib.auth import get_user_model
from goldmain.models import GoldPrice, Forecast
import datetime
from goldmain.views import forecast_verification

@pytest.mark.parametrize('param', [
    ('home'),
    ('gold_price'),
    ('register'),
    ('login')
])


@pytest.mark.django_db
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_user_register(client, user_data):
    user_model = get_user_model()
    assert len(user_model.objects.all()) == 0
    response = client.post('/register/', user_data)
    assert len(user_model.objects.all()) == 1
    assert response.status_code == 302
    assert response.url == urls.reverse('login')
    user = user_model.objects.get(username='Robert')
    assert user.username == 'Robert'
    assert user.email == 'robert@wp.pl'


@pytest.mark.django_db
def test_user_login(client, create_test_user, user_data):
    user_model = get_user_model()
    assert user_model.objects.count() == 1
    login_url = urls.reverse('login')
    response = client.post(login_url, user_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logout(client):
    logout_url = urls.reverse('logout')
    response = client.get(logout_url)
    assert response.status_code == 302
    assert response.url == urls.reverse('home')


@pytest.mark.django_db
def test_save_gold_price(client):
    gold_price_db = GoldPrice.objects.filter(day=datetime.date.today())
    assert len(gold_price_db) == 0
    response = client.post('/gold_price/', {'price': 'gold_price'})
    today_gold_price = GoldPrice.objects.filter(day=datetime.date.today())
    assert len(today_gold_price) == 1


@pytest.mark.django_db
def test_save_forecast(user_data, client, authenticated_user, forecast):
    assert len(Forecast.objects.all()) == 0
    response = client.post('/forecast/', forecast)
    assert len(Forecast.objects.all()) == 1
    assert response.status_code == 302
    assert response.url == urls.reverse('forecast')




@pytest.mark.django_db
def test_forecast_verification(user_data, client, authenticated_user):
    foracast = Forecast.objects.create(
        author=authenticated_user,
        created='2021-01-07',
        gold_forecast=1900.00,
        verification_date='2021-01-08'
    )
    goldprice = GoldPrice.objects.create(
        day='2021-01-07',
        price=1850.00
    )
    goldprice_ver = GoldPrice.objects.create(
        day='2021-01-08',
        price=1875.00
    )
    response = client.get('/forecast_verification/', {
        'lista_prognoz': lista_prognoz
    })
    print(response.context)
    assert ocena_prognozy['result_of_verification'] == True
