from django.urls import path
from . import views

app_name = 'app_board'

urlpatterns = [
    path('', views.index, name='index'),
#    path('<int:article_id>/', views.read_article, name='read_article'),

]