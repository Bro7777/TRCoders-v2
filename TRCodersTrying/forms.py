from django import forms
from.models import Post,Comment

class Postform(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','icerik','image','draft']


class Commentform(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['comment_icerik']
