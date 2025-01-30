from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']

    members = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'id': 'member-search',
        'placeholder': 'Üyeleri ara ve seç...'
    }))

