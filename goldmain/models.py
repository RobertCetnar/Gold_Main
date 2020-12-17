from django.db import models
from django.contrib.auth.models import User


class GoldPrice(models.Model):
    day = models.DateField(auto_now_add=True)
    price = models.FloatField()


class Notes(models.Model):
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=256)
    #note_author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


class Forecast(models.Model):
    day = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    gold_forecast = models.CharField(max_length=256)


class History_Forecast(models.Model):
    forecast_author = models.ForeignKey(User, on_delete=models.CASCADE)
    forecast_verification = models.BooleanField()
