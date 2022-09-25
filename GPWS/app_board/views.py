from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import *
from .models import *

# Create your views here.
def index(request:WSGIRequest):
    lastest_article_list = Article.objects.all().order_by('create_dt')[:10]
    context = { 'lastest_article_list' : lastest_article_list }
    return render(request, 'app_board/index.html', context)

def read_article(request:WSGIRequest, article_id:int):
    article = get_object_or_404(Article, pk=article_id)
    context = { 'article' : article }
    return render(request, 'app_board/read_article.html', context)