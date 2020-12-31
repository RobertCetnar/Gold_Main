
from django.contrib import admin
from django.urls import path
from goldmain.views import home, gold_price_from_website, register, login_user, logout_user, note_book, delete_note, forecast, forecast_verification


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('gold_price/', gold_price_from_website, name='gold_price'),
    path('register/', register, name='register'),
    path('accounts/login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('note_book/', note_book, name='note_book'),
    path('delete_note/<int:noteid>/', delete_note, name='delete_note'),
    path('forecast/', forecast, name='forecast'),
    path('forecast_verification/', forecast_verification, name='forecast_verification'),

]
