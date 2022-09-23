from django.db import models
from datetime import datetime

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=300, null=False)
    cntn = models.CharField(max_length=10000, null=True)
    cret_dt = models.DateTimeField(default=datetime.now)
    mdfy_dt = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    cntn = models.CharField(max_length=10000)
    cret_dt = models.DateTimeField(default=datetime.now)
    mdfy_dt = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.cntn
