from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.generic import View, TemplateView, FormView
from django.core.handlers.wsgi import WSGIRequest
import re

# 회원 가입
class SignUp(View):
    # 내부적으로 dispatch()을 통해 HTTP Method 를 식별하여 get(), post(),... 등을 호출
    def get(self, request, *args, **kwargs):
        return render(request, 'app_sign/sign_up.html')

    def post(self, request, *args, **kwargs):
        # return 시 가입 페이지에 데이터가 남도록 context 딕셔너리 유지
        context             = {'user_id': request.POST['user_id']}

        user_id             = request.POST['user_id']
        password            = request.POST['password']
        password_confirm    = request.POST['password_confirm']

        # Fail Case 1. user_id 유효성
        # Fail Case 1-1.
        if re.compile(r'[^a-zA-Z0-9_]').findall(user_id):
            context['error'] = 'user_id 는 알파벳 혹은 숫자, 언더바(_)로만 가능합니다.'
            return render(request, 'app_sign/sign_up.html', context=context)
        # Fail Case 1-2.
        if len(user_id) >= 20:
            context['error'] = 'user_id 는 20자 미만이어야 합니다.'
            return render(request, 'app_sign/sign_up.html', context=context)
        # Fail Case 1-3.
        if User.objects.filter(username=user_id).exists():
            context['error'] = f'user_id "{ user_id }"는 이미 exist 합니다.'
            return render(request, 'app_sign/sign_up.html', context=context)

        # Fail Case 2. password 유효성
        # Fail Case 2-1.
        if password == '':
            context['error'] = '비밀번호를 입력해주세요.'
            return render(request, 'app_sign/sign_up.html', context=context)

        # Fail Case 2-2.
        if password != password_confirm:
            context['error'] = '비밀번호 확인 값이 다릅니다.'
            return render(request, 'app_sign/sign_up.html', context=context)

        # Save
        try:
            user = User.objects.create_user(username=user_id, password=password)
        except Exception as ex:
            context['error'] = f'신규 유저 생성 실패 [error:{ str(ex) }]'
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
        user_id     = request.POST['user_id']
        password    = request.POST['password']

        # 해당 username과 password와 일치하는 user 객체를 가져온다.
        user = auth.authenticate(request, username=user_id, password=password)

        # 해당 user 객체가 존재한다면
        if user is not None:
            # 로그인 한다
            auth.login(request, user)
            return redirect('/')
        # 존재하지 않는다면
        else:
            context = {'username':user_id, 'password':"", 'error': 'username or password is incorrect 입니다.'}
            # 딕셔너리에 에러메세지를 전달하고 다시 login.html 화면으로 돌아간다.
            return render(request, 'app_sign/login.html', context=context)

# 로그 아웃
class Logout(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app_sign/login.html')

    def post(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect('/')


# 회원 정보 수정
class MyPage(View):
    # 내부적으로 dispatch()을 통해 HTTP Method 를 식별하여 get(), post(),... 등을 호출
    def get(self, request, *args, **kwargs):
        return render(request, 'app_sign/my_page.html')

    def post(self, request, *args, **kwargs):
        context = {'password': ''}

        password            = request.POST['password']
        password_confirm    = request.POST['password_confirm']

        # Fail Case 1. password와 confirm에 입력된 값이 같다면
        if password != password_confirm:
            context['error'] = '비밀번호 확인 값이 다릅니다.'
            return render(request, 'app_sign/my_page.html', context=context)

        # Fail Case 2. password 공백
        if password == '':
            context['error'] = '비밀번호를 입력해주세요.'
            return render(request, 'app_sign/my_page.html', context=context)

        # Save
        try:
            user = request.user
            user.set_password(password)
            user.save()
        except Exception as ex:
            context['error'] = f'변경 실패.... { str(ex) }'
            return render(request, 'app_sign/my_page.html', context=context)

        # 로그인
        auth.login(request, user)
        return redirect('/')
