from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from .models import *

# Create your views here.
def index(request:WSGIRequest):
    print(type(request))
    lastest_article_list = Article.objects.all().order_by('cret_dt')[:10]
    context = { 'lastest_article_list' : lastest_article_list }
    return render(request, 'app_board/index.html', context)