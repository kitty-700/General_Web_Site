from django import forms
from .models import Article
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

class ArticleWriteForm(forms.ModelForm):
    title = forms.CharField(
        label='글 제목',
        widget=forms.TextInput(
            attrs={
                'placeholder':'게시글 제목'
            }),
        required=True,
    )
    contents = SummernoteTextField()

    field_order = [
        'title',
        'contents',
    ]

    class Meta:
        model = Article
        fields = [
            'title',
            'contents',
        ]
        widgets = {
            'contents' : SummernoteWidget
        }

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title', '')
        contents = cleaned_data.get('contents', '')

        if title == '':
            self.add_error('title', '글 제목을 입력하세요.')
        elif contents == '':
            self.add_error('contents', '글 내용을 입력하세요.')
        else:
            self.title = title
            self.contents = contents