
from django.contrib import admin
from django.urls import path
from goldmain.views import home, gold_price_from_website, register, login_user, logout_user


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('gold_price/', gold_price_from_website, name='gold_price'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

]
