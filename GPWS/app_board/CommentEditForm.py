from django import forms
from .models import Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'contents',
        ]

        widgets = {
            'contents': forms.CharField(widget=CKEditorUploadingWidget()),
        }

    def clean(self): # override 된 메소드. 값이 비어있는지를 체크한다.
        cleaned_data = super().clean()

        contents = cleaned_data.get('contents', '')

        if contents == '':
            self.add_error('contents', '글 내용을 입력하세요.')
        else:
            self.contents = contents