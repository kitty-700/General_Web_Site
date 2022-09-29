from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('contents',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)


