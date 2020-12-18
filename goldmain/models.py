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
        ordering = ['-created']


class Forecast(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    gold_forecast = models.FloatField()
    verification_date = models.DateField("Purchase Date(yyyy-mm-dd)", auto_now_add=False, auto_now=False, blank=True)


class History_Forecast(models.Model):
    forecast_author = models.ForeignKey(User, on_delete=models.CASCADE)
    forecast_verification = models.BooleanField()
