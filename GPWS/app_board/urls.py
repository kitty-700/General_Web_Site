from django.urls import path, include
from . import views
from .views import *

app_name = 'app_board'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('notice/', TemplateView.as_view(template_name='notice.html')),
    path('write/', views.write_article, name='write_article'),
    path('<int:article_id>/', views.read_article, name='read_article'),
    path('<int:article_id>/write_comment', views.write_comment, name='write_comment'),
    path('<int:article_id>/update_article', views.update_article, name='update_article'),
    path('<int:article_id>/block_article/<int:block_tp>/', views.block_article, name='block_article'),
    path('<int:article_id>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]