from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.generic import View, TemplateView, FormView
from django.core.handlers.wsgi import WSGIRequest

# 회원 가입
class SignUp(View):
    # 내부적으로 dispatch()을 통해 HTTP Method 를 식별하여 get(), post(),... 등을 호출
    def get(self, request, *args, **kwargs):
        return render(request, 'app_sign/sign_up.html')

    def post(self, request, *args, **kwargs):
        context = {'username': request.POST['username'], 'password': ''}

        # Fail Case 1. ID 가 유효한지 검사
        if request.POST['username'].isalnum() == False:
            context['error'] = 'username은 알파벳 혹은 한글, 숫자로만 가능합니다.'
            return render(request, 'app_sign/sign_up.html', context=context)

        # Fail Case 2. password와 confirm에 입력된 값이 같다면
        if request.POST['password'] != request.POST['confirm']:
            context['error'] = '비밀번호 확인 값이 다릅니다.'
            return render(request, 'app_sign/sign_up.html', context=context)

        # Fail Case 2. user 객체를 새로 생성
        try:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        except:
            context['error'] = f'username "{ request.POST["username"] }"는 이미 exist 합니다.'
            return render(request, 'app_sign/sign_up.html', context=context)

        # 로그인
        auth.login(request, user)
        return redirect('/app_board/notice')

# 로그인

class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app_sign/login.html')

    def post(self, request, *args, **kwargs):
        # login.html에서 넘어온 username과 password를 각 변수에 저장한다.
        username = request.POST['username']
        password = request.POST['password']

        # 해당 username과 password와 일치하는 user 객체를 가져온다.
        user = auth.authenticate(request, username=username, password=password)

        # 해당 user 객체가 존재한다면
        if user is not None:
            # 로그인 한다
            auth.login(request, user)
            return redirect('/')
        # 존재하지 않는다면
        else:
            context = {'username':username, 'password':"", 'error': 'username or password is incorrect 입니다.'}
            # 딕셔너리에 에러메세지를 전달하고 다시 login.html 화면으로 돌아간다.
            return render(request, 'app_sign/login.html', context=context)

# 로그 아웃
class Logout(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app_sign/login.html')

    def post(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect('/')