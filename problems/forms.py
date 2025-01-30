from django import forms
from.models import *

class SolutionForm(forms.ModelForm):
    class Meta:
        model=Solution
        fields=['code','language']