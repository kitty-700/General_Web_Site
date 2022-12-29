from django import forms
from .models import Article, Board
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'board',
            'title',
            'contents',
        ]

        widgets = {
            'contents': forms.CharField(widget=CKEditorUploadingWidget()),
        }

    def clean(self): # override 된 메소드. 값이 비어있는지를 체크한다.
        cleaned_data = super().clean()

        title = cleaned_data.get('title', '')
        contents = cleaned_data.get('contents', '')
        board = cleaned_data['board']

        if title == '':
            self.add_error('title', '글 제목을 입력하세요.')
        elif contents == '':
            self.add_error('contents', '글 내용을 입력하세요.')
        elif board == '':
            self.add_error('board', '게시판 종류를 선택하세요.')
        else:
            self.title = title
            self.contents = contents
            self.board = board