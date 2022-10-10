from django.urls import path, include
from . import views

app_name = 'app_sign'

urlpatterns = [
    path('sign_up/',    views.sign_up,  name='sign_up'),
    path('login/',      views.login,    name='login'),
    path('logout/',     views.logout,   name='logout'),
]