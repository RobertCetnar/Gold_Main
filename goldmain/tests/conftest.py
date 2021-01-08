
import pytest
from django.test import Client
from django.contrib.auth import get_user_model


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user_data():
    user = {
        'username': 'Robert',
        'email': 'robert@wp.pl',
        'password1': 'Rc123456',
        'password2': 'Rc123456'
    }
    return user


@pytest.fixture
def create_test_user(user_data):
    user_model = get_user_model()
    test_user = user_model.objects.create_user(user_data)
    test_user.set_password(user_data.get('password1'))
    return test_user


@pytest.fixture
def forecast():
    forecast = {
        'gold_forecast': '1910.11',
        'verification_date': '2021-01-10'
    }
    return forecast

@pytest.fixture
def authenticated_user(client, user_data):
    user_model = get_user_model()
    test_user = user_model.objects.create_user(user_data)
    test_user.set_password(user_data.get('password'))
    test_user.save()
    client.force_login(test_user)
    return test_user

