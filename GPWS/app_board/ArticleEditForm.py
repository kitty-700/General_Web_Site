from django import forms
from .models import Article

class ArticleEditForm(forms.ModelForm):
    title = forms.CharField(
        label='글 제목',
    )
    
    contents = forms.CharField(
        label='글 내용',
        required=False, # WYSIWYG 사용 시 True 로 세팅되어있으면 An invalid form control with name='contents' is not focusable 오류 발생
        widget=forms.Textarea()
    )

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

    def clean(self): # override 된 메소드. 값이 비어있는지를 체크한다.
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