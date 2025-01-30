from typing import Any
from django import forms
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from.models import UserProfile

class RegisterForm(forms.ModelForm):
    class Meta:
     model=User
     fields=['first_name','username','email','password']

    def clean_email(self):
       email=self.cleaned_data['email']
       
       
       uzunluk=User.objects.filter(email=email)

       if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu email adresi daha önce kullanılmış.")
       return email

class LoginForm(forms.Form):
   username=forms.CharField(max_length=50,required=True)
   password=forms.CharField(max_length=50)
   

   def clean_username(self):
      username=self.cleaned_data['username']
      if '@' in username:
         user=User.objects.filter(email=username)
         if len(user)==1:
            user=user.first()
            return user.username
         
         else:
            raise forms.ValidationError("Böyle bir kullanıcı bulunamadı")
      return username
   
class UserProfileForm(forms.ModelForm):
   class Meta:
      model=UserProfile
      fields=('profile_photo',)

class UserEditForm(forms.ModelForm):
   class Meta:
      model=User
      fields=('first_name',)

class PasswordChangeForm(PasswordChangeForm):
   class Meta:
      model = User
      fields = ('password',)
