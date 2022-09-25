from django.db import models
from datetime import datetime

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=300, null=False)
    main_text = models.CharField(max_length=10000, null=True)

    create_dt = models.DateTimeField(default=datetime.now)
    modify_dt = models.DateTimeField(default=datetime.now)
    author    = models.CharField(max_length=100, null=True)
    view_cnt  = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    main_text = models.CharField(max_length=10000)

    create_dt = models.DateTimeField(default=datetime.now)
    modify_dt = models.DateTimeField(default=datetime.now)
    author    = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.cntn
