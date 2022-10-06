from django.db import models
from datetime import datetime

# Create your models here.

class Article(models.Model):
    # PK 명시
    id = models.AutoField(primary_key=True)
    # User Manual Fill
    title = models.CharField(max_length=300, null=False)
    contents = models.CharField(max_length=10000, null=True)
    # Auto Fill
    create_dt = models.DateTimeField(default=datetime.now)
    modify_dt = models.DateTimeField(default=datetime.now)
    author    = models.CharField(max_length=100, null=True)
    view_cnt  = models.IntegerField(default=0)
    # Admin Act
    is_blocked= models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    # PK 명시
    id = models.AutoField(primary_key=True)
    # Manual Fill
    contents = models.CharField(max_length=10000)
    # Auto Fill
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    create_dt = models.DateTimeField(default=datetime.now)
    modify_dt = models.DateTimeField(default=datetime.now)
    author    = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.contents

class ViewCheck(models.Model):
    # PK 명시
    id = models.AutoField(primary_key=True)
    # Auto Fill
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    author  = models.CharField(max_length=100)

    def __str__(self):
        return self.author + " in [" + str(self.article)+"]"

    class Meta:
        unique_together = ('article', 'author')
