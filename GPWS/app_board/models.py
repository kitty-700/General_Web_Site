from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

# 컬럼 추가/변경 등의 사유로 테이블 재생성 시 다음 요령을 따를 것
# 1. db.sqlite3 파일의 django_migrations 테이블에서 app = 'app_board' 에 해당하는 내역 삭제 후 저장
# 2. '../app_board/migrations/' 파일 중 __init__.py 외에 모두 삭제
# 3. >> python manage.py makemigrations
# 4. >> python manage.py migrate

class Article(models.Model):
    # PK 명시
    id = models.AutoField(primary_key=True)
    # User Manual Fill
    title = models.CharField(max_length=300, null=False)
    contents = RichTextUploadingField(null=True)

    # Auto Fill
    create_dt = models.DateTimeField(default=datetime.now)
    modify_dt = models.DateTimeField(default=datetime.now)
    author    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    work_ip   = models.CharField(max_length=20, default="annonymous")
    view_cnt  = models.IntegerField(default=0)
    # Admin Act
    is_blocked= models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    # PK 명시
    id = models.AutoField(primary_key=True)
    # Manual Fill
    contents = RichTextUploadingField(null=True)
    # Auto Fill
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    create_dt = models.DateTimeField(default=datetime.now)
    modify_dt = models.DateTimeField(default=datetime.now)
    author    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    work_ip   = models.CharField(max_length=20, default="annonymous")

    def __str__(self):
        return self.contents

class ViewCheck(models.Model):
    # PK 명시
    id = models.AutoField(primary_key=True)
    # Auto Fill
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    work_ip    = models.CharField(max_length=20)

    user    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.work_ip + " in [" + str(self.article)+"]"

    class Meta:
        unique_together = ('article', 'work_ip') # 실질적인 체크는 ip 를 통해서만
