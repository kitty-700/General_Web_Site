from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('',            lambda req: redirect('/app_board/')),
    path('admin/',      admin.site.urls),
    path('app_board/',  include('app_board.urls')),
    path('sign/',       include('app_sign.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]

from  django.conf import settings
from django.conf.urls.static import static

print("STATIC_ROOT..%s" % settings.STATIC_ROOT)
print("STATICFILES_DIRS..%s" % settings.STATICFILES_DIRS)
print("BASE_DIR..%s" % settings.BASE_DIR)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# django-ckeditor image upload 관련, staff 권한 패스하도록 가상환경 내의 라이브러리 조작이 필요함
# venv/Lib/site-pakages/ckeditor_uploader/urls.py 에서 경로 upload 와 browse 를 다음과 같이 수정
#   re_path(r'^upload/', views.upload, name='ckeditor_upload'),
#   re_path(r'^browse/', never_cache(views.browse), name='ckeditor_browse'),
# 기존에는 view 부분에 staff_member_required() 적용되어있었으나 이를 배제