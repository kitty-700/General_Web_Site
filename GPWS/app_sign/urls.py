from django.urls import path, include
from . import views
from .views import *

app_name = 'app_sign'

urlpatterns = [
    path('sign_up/',    SignUp.as_view(), name='sign_up'),
    path('login/',      Login.as_view(),  name='login'),
    path('logout/',     Logout.as_view(), name='logout'),
]