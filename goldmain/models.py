from django.db import models
from django.contrib.auth.models import User


class GoldPrice(models.Model):
    day = models.DateField(auto_now_add=True)
    price = models.FloatField()


class User_Notes(models.Model):
    day = models.DateField(auto_now_add=True)
    note = models.CharField(max_length=256)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Forecast(models.Model):
    day = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    gold_forecast = models.CharField(max_length=256)


class History_Forecast(models.Model):
    forecast_author = models.ForeignKey(User, on_delete=models.CASCADE)
    forecast_verification = models.BooleanField()
