# Generated by Django 2.2.6 on 2020-12-08 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goldmain', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HistoryForecast',
            new_name='History_Forecast',
        ),
        migrations.RenameModel(
            old_name='UserNotes',
            new_name='User_Notes',
        ),
    ]