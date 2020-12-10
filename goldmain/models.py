from django.db import models


class GoldPrice(models.Model):
    day = models.DateField(auto_now_add=True)
    price = models.FloatField()

class User(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    password = models.CharField(max_length=256)

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
