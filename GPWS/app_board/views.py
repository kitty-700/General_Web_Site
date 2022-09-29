from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import *

from .ArticleWriteForm import ArticleWriteForm
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

def write_article(request:WSGIRequest):
    context = {}
    if request.method == 'GET': # 1차로는 GET 으로 Form을 얻고
        write_form = ArticleWriteForm()
        context['forms'] = write_form
        print(write_form)
        return render(request, 'app_board/write_article.html', context)
    elif request.method == 'POST': # 2차로는 받아온 Form에 내용을 넣어 입력 처리
        write_form = ArticleWriteForm(request.POST)
        if write_form.is_valid():
            author = "Annonymous" # 추후 User.objects.get(user_id=login_session) 를 통해 User nickname 식별
            article = Article(
                title=      write_form.title,
                contents=  write_form.contents,
                author=     author,
            )
            article.save()
            return redirect('/app_board')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for val in write_form.errors.values():
                    context['error'] = val
            return render(request, 'app_board/write_article.html', context)