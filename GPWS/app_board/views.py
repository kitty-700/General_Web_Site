from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import *

from .ArticleEditForm import ArticleEditForm
from .models import *

# Create your views here.
def index(request:WSGIRequest):
    lastest_article_list = Article.objects.all().order_by('-create_dt')[:10]
    context = { 'lastest_article_list' : lastest_article_list }
    return render(request, 'app_board/index.html', context)

def read_article(request:WSGIRequest, article_id:int):
    article = get_object_or_404(Article, pk=article_id)

    ip = get_client_ip(request)


    try: # 조회수 중복집계 방지
        print(article)
        print(ip)
        ViewCheck.objects.get(
            article=article,
            author=ip,
        )
    except ViewCheck.DoesNotExist:
        print("없어서 만들려구")
        vc = ViewCheck(
            article=article,
            author=ip,
        )
        vc.save()
        article.view_cnt += 1
        article.save()


    try:
        comments = get_list_or_404(Comment, article=article_id)
    except:
        comments = []
    context = { 'article' : article, 'comments' : comments, 'ip': get_client_ip(request) }
    return render(request, 'app_board/read_article.html', context)

def write_article(request:WSGIRequest):
    context = {}
    ip = get_client_ip(request)

    if request.method == 'GET': # 1차로는 GET 으로 Form을 얻고
        write_form = ArticleEditForm()
        context['forms'] = write_form
        return render(request, 'app_board/write_article.html', context)
    elif request.method == 'POST': # 2차로는 받아온 Form에 내용을 넣어 입력 처리
        write_form = ArticleEditForm(request.POST)
        if write_form.is_valid():
            author = ip # 추후 User.objects.get(user_id=login_session) 를 통해 User nickname 식별
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

def write_comment(request:WSGIRequest, article_id:int):
    if request.method == 'POST':
        comment = Comment(
            article_id=article_id,
            contents=request.POST['comment'],
        )
        comment.save()
    return redirect('/app_board/%s/' % (article_id))

def update_article(request:WSGIRequest, article_id:int):
    context = {}
    ip = get_client_ip(request)

    article = get_object_or_404(Article, pk=article_id)

    if article.author != ip:
        return redirect('/app_board/')

    if request.method == 'GET': # 1차로는 GET 으로 Form을 얻고
        write_form = ArticleEditForm(instance=article)
        context['forms'] = write_form
        return render(request, 'app_board/update_article.html', context)
    elif request.method == 'POST': # 2차로는 받아온 Form에 내용을 넣어 입력 처리
        write_form = ArticleEditForm(request.POST)
        if write_form.is_valid():
            article.title = write_form.title
            article.contents = write_form.contents
            # article.modify_dt =
            article.save()
            return read_article(request=request, article_id=article_id)
        else:
            context['forms'] = write_form
            if write_form.errors:
                for val in write_form.errors.values():
                    context['error'] = val
            return render(request, 'app_board/write_article.html', context)

def get_client_ip(request:WSGIRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip