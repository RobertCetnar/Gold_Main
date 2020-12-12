
from django.contrib import admin
from django.urls import path
from goldmain.views import main_page, gold_price_from_website


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='main_page'),
    path('gold_price/', gold_price_from_website, name='gold_price'),

]
