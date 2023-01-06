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


class ArticleInBoard(): # 단일 게시물에 대한 정보
    def __init__(self, article: Article, comment_cnt: int):
        self.article = article
        self.comment_cnt = comment_cnt
        self.board = article.board

    def __str__(self):
        print(f'{self.board.title} - {self.article.title} ({self.comment_cnt})')

class IndexBoard():
    def __init__(self, aibs : List[ArticleInBoard], board : Board):
        self.aibs = aibs
        self.board = board

def articles_in_board(board : Board, article_cnt:int) -> List[ArticleInBoard]:
    articles: List[Article] = (
                                  Article.objects.filter(board=board.id)
                              ).order_by('-id')[:article_cnt]

    articles_in_board: List[ArticleInBoard] = []
    for a in articles:
        articles_in_board.append(
            ArticleInBoard(a, Comment.objects.filter(article=a).count())
        )

    return articles_in_board

class IndexView(View):
    # 내부적으로 dispatch()을 통해 HTTP Method 를 식별하여 get(), post(),... 등을 호출
    def get(self, request:WSGIRequest): # HTTP Method 가 GET일 때의 동작을 오버라이딩
        
        # Query : BOARD_ID 는 NOT NULL 이어야 함
        # - UPDATE APP_BOARD_ARTICLE SET BOARD_ID = 1 WHERE BOARD_ID IS NULL;
        
        # 각 게시판 개수 별로 나열
        DAC = 5 # Default_Article_Cnt

        boards = Board.objects.filter()

        ibs : List[IndexBoard] = []

        for b in boards:
            ibs.append(
                IndexBoard(
                    articles_in_board(b, DAC),
                    b
                )
            )

        context = {
            'ibs': ibs,
        }
        return render(request, 'app_board/index.html', context)

class BoardView(View):
    def get(self, request:WSGIRequest, board_id:int): # HTTP Method 가 GET일 때의 동작을 오버라이딩

        # Query : BOARD_ID 는 NOT NULL 이어야 함
        # - UPDATE APP_BOARD_ARTICLE SET BOARD_ID = 1 WHERE BOARD_ID IS NULL;

        DAC = 30  # Default_Article_Cnt

        board: Board = Board.objects.filter(id=board_id)[0]

        ib : IndexBoard = IndexBoard(
            articles_in_board(board, DAC),
            board
        )

        context = {
            'ib': ib,
        }

        return render(request, 'app_board/read_board.html', context)

def read_article(request:WSGIRequest, article_id:int):
    ip      = get_client_ip(request)
    article = get_object_or_404(Article, pk=article_id)
    print(article_id)
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
        write_form = ArticleEditForm(
            board_id = # 게시판 별도 지정하는 경우 해당 필드 초기값 세팅
            kwargs['board_id'] if 'board_id' in kwargs else None
        )
        
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
