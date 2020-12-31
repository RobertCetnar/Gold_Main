from django.db import models
from django.contrib.auth.models import User


class GoldPrice(models.Model):
    day = models.DateField(auto_now_add=True)
    price = models.FloatField()


class Notes(models.Model):
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=256)
    note_author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created', ]


class Forecast(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    gold_forecast = models.FloatField("Gold-price Forecast")
    verification_date = models.DateField("Expected Date(yyyy-mm-dd)", auto_now_add=False, auto_now=False, blank=True)


class ForecastVerification(models.Model):
    forecast_to_verification = models.OneToOneField(Forecast, on_delete=models.CASCADE)
    verification_result = models.BooleanField()
    accuracy = models.IntegerField()
