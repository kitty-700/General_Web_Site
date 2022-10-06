from django.contrib import admin
from django.urls import path, include

from django.shortcuts import redirect

urlpatterns = [
    path('', lambda req: redirect('/app_board/')),
    path('admin/', admin.site.urls),
    path('app_board/', include('app_board.urls')),
]

# summernote (게시글 작성 form) 추가
from  django.conf import settings
from django.conf.urls.static import static

print("STATIC_ROOT..%s" % settings.STATIC_ROOT)
print("STATICFILES_DIRS..%s" % settings.STATICFILES_DIRS)
print("BASE_DIR..%s" % settings.BASE_DIR)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)