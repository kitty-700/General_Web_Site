from django.urls import path, include
from . import views

app_name = 'app_board'

urlpatterns = [
    path('', views.index, name='index'),
    path('write/', views.write_article, name='write_article'),
    path('<int:article_id>/', views.read_article, name='read_article'),
    path('<int:article_id>/write_comment', views.write_comment, name='write_comment'),

]