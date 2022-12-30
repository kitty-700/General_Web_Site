import json

from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import *
from .ArticleEditForm import ArticleEditForm
from .CommentEditForm import CommentEditForm
from .models import *
from typing import List
from django.views.generic import View, TemplateView, FormView
from django.http import JsonResponse

def audience(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # do something
        if data['username'] == '':
            data['username'] = f'Guest {get_client_ip(request)}'

        print( "Message from " + data['username'] + " : " + data['audience_msg'])
        context = {
            'result': data,
        }
        return JsonResponse(context)

class IndexView(View):
    # 내부적으로 dispatch()을 통해 HTTP Method 를 식별하여 get(), post(),... 등을 호출
    def get(self, request:WSGIRequest): # HTTP Method 가 GET일 때의 동작을 오버라이딩
        # (임시) 하드코딩으로 게시판 나눔
        # 첫번째 Sector
        lastest_article_list_1: List[Article] = (
            Article.objects.filter(board__isnull=True) |
            Article.objects.filter(board=1)
        ).order_by('-id')[:30]
        view_cnt_list_1: List[int] = []
        for a in lastest_article_list_1:
            view_cnt_list_1.append(Comment.objects.filter(article=a).count())
        board_1 = Board.objects.filter(id=1)[0]

        # 두번째 Sector
        lastest_article_list_2: List[Article] = (
            Article.objects.filter(board=2)
        ).order_by('-id')[:30]
        view_cnt_list_2: List[int] = []
        for a in lastest_article_list_2:
            view_cnt_list_2.append(Comment.objects.filter(article=a).count())
        board_2 = Board.objects.filter(id=2)[0]

        context = {
            'lastest_article_list_1': lastest_article_list_1,
            'view_cnt_list_1'       : view_cnt_list_1,
            'board_1'               : board_1,

            'lastest_article_list_2': lastest_article_list_2,
            'view_cnt_list_2'       : view_cnt_list_2,
            'board_2'               : board_2,
        }
        return render(request, 'app_board/index.html', context)

class BoardView(View):
    def get(self, request:WSGIRequest, board_id:int): # HTTP Method 가 GET일 때의 동작을 오버라이딩
        if board_id == 1: # 1번 게시판은 특수 취급 -> 게시판 구분 null인 게시물도 포함
            lastest_article_list: List[Article] = (
                Article.objects.filter(board__isnull=True) | # 게시판 구분이 없으면 자유게시판으로 취급됨
                Article.objects.filter(board=board_id)
            ).order_by('-id')[:30] # 이 부분도 추후 page 에서 한 번에 조회 가능한 개수 넘겨받고 하드코딩 풀면 될듯
        else:
            lastest_article_list: List[Article] = (
                Article.objects.filter(board=board_id)
            ).order_by('-id')[:30]

        view_cnt_list: List[int] = []
        for a in lastest_article_list:
            view_cnt_list.append(Comment.objects.filter(article=a).count())
        board = Board.objects.filter(id=board_id)[0].title

        context = {
            'lastest_article_list': lastest_article_list,
            'view_cnt_list'       : view_cnt_list,
            'board'               : board,
        }
        return render(request, 'app_board/read_board.html', context)

def read_article(request:WSGIRequest, article_id:int):
    ip      = get_client_ip(request)
    article = get_object_or_404(Article, pk=article_id)

    try: # 조회수 중복집계 방지
        ViewCheck.objects.get(
            article=article,
            work_ip=ip,
        )
    except ViewCheck.DoesNotExist:
        vc = ViewCheck(
            article=article,
            work_ip=ip,
        )
        vc.save()
        article.view_cnt += 1
        article.save()

    try:
        comments = get_list_or_404(Comment, article=article_id)
    except:
        comments = []
    context = { 'article' : article, 'comments' : comments, 'comment_form' : CommentEditForm() }
    return render(request, 'app_board/read_article.html', context)

class WriteArticle(View):
    form_class = ArticleEditForm
    template_name = 'write_article.html'
    success_url = '/'
    context = {}

    def get(self, request, *args, **kwargs):
        write_form = ArticleEditForm()
        self.context['form'] = write_form
        return render(request, 'app_board/write_article.html', self.context)

    def post(self, request, *args, **kwargs):
        write_form = ArticleEditForm(request.POST)
        if write_form.is_valid():
            article = Article(
                title=      write_form.title,
                contents=  write_form.contents,
                author=request.user if isinstance(request.user, User) else None,
                board=write_form.board,
                work_ip=get_client_ip(request)
            )
            article.save()
            return redirect('/app_board')
        else:
            self.context['form'] = write_form
            if write_form.errors:
                for val in write_form.errors.values():
                    self.context['error'] = val
            return render(request, 'app_board/write_article.html', self.context)

class UpdateArticle(View):
    form_class = ArticleEditForm
    template_name = 'update_article.html'
    success_url = '/'
    context = {}

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['article_id'])
        if is_article_owner(request, get_client_ip(request), article) == False:
            return redirect('/app_board/')

        write_form = ArticleEditForm(instance=article)
        self.context['form'] = write_form
        return render(request, 'app_board/update_article.html', self.context)

    def post(self, request, *args, **kwargs):
        article_id = kwargs['article_id']
        article = get_object_or_404(Article, pk=article_id)
        if is_article_owner(request, get_client_ip(request), article) == False:
            return redirect('/app_board/')

        write_form = ArticleEditForm(request.POST)
        if write_form.is_valid():
            article.title = write_form.title
            article.contents = write_form.contents
            article.modify_dt = datetime.now()
            article.board = write_form.board
            article.save()
            return read_article(request=request, article_id=article_id)
        else:
            self.context['form'] = write_form
            if write_form.errors:
                for val in write_form.errors.values():
                    self.context['error'] = val
            return render(request, 'app_board/write_article.html', self.context)
def delete_article(request:WSGIRequest, article_id:int):
    article = get_object_or_404(Article, pk=article_id)

    # 권한
    if is_article_owner(request, get_client_ip(request), article) == False:
        return redirect('/app_board/')

    article.delete()

    return redirect('/app_board/')


def block_article(request:WSGIRequest, article_id:int, block_tp:int):
    if not request.user.is_superuser:
        return redirect('/app_board/')

    article = get_object_or_404(Article, pk=article_id)
    article.is_blocked = False if block_tp == 0 else True
    article.save()

    return redirect('/app_board/%s/' % (article_id))

def write_comment(request:WSGIRequest, article_id:int):
    if request.method == 'POST':
        if len(request.POST['contents'].strip()) == 0:
            return redirect('/app_board/%s/' % (article_id))
        write_form = CommentEditForm(request.POST)
        if write_form.is_valid():
            comment = Comment(
                article_id=article_id,
                contents=write_form.contents,
                author=request.user if isinstance(request.user, User) else None,
                work_ip=get_client_ip(request)
            )
            comment.save()
            return redirect('/app_board/%s/' % (article_id))
    return redirect('/app_board/%s/' % (article_id))

def delete_comment(request:WSGIRequest, article_id:int, comment_id:int):
    comment = get_object_or_404(Comment, pk=comment_id)

    # 권한
    if is_comment_owner(request, get_client_ip(request), comment) == False:
        return redirect('/app_board/')

    comment.delete()

    return redirect('/app_board/%s/' % (article_id))

def get_client_ip(request:WSGIRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_comment_owner(request:WSGIRequest, ip, comment: Comment):
    # 작성 계정이 존재한다면 계정을 통해 검사
    if comment.author is not None:
        if comment.author != request.user:
            return False
    # 작성 계정이 따로 없다면 ip를 통해 검사
    else:
        if comment.work_ip != ip:
            return False
    return True

def is_article_owner(request:WSGIRequest, ip, article: Article):
    # 작성 계정이 존재한다면 계정을 통해 검사
    if article.author is not None:
        if article.author != request.user:
            return False
    # 작성 계정이 따로 없다면 ip를 통해 검사
    else:
        if article.work_ip != ip:
            return False
    return True
