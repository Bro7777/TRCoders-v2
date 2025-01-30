from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from.forms import RegisterForm,LoginForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from.models import UserProfile,UserProblemStatus
from.forms import UserProfileForm,UserEditForm
from django.contrib.auth.decorators import login_required
from problems.models import Solution

def sign_up(request):
    form=RegisterForm(request.POST or None)
    if request.user.is_authenticated==True:
       return HttpResponseRedirect(reverse('postlar:post_lister'))

    if form.is_valid():
        new_user=form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        yetkilimi=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
        if yetkilimi:
          login(request,yetkilimi)
          return HttpResponseRedirect(reverse('postlar:post_lister'))
    else:
       print(print(form.errors))
    
       
        
    return render(request,"users/signup.html",context={'form':form})

def user_login(request):
   form=LoginForm(request.POST or None)
   if request.user.is_authenticated==True:
       return HttpResponseRedirect(reverse('postlar:post_lister'))
       
   if request.method == 'POST':
        if form.is_valid():
               yetkilimi=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
               if yetkilimi:
                   login(request,yetkilimi)
                   return HttpResponseRedirect(reverse('postlar:post_lister'))
               else:
                   hata="Kullanici adi ve ya parola yanlis"
                   return render(request,"users/login.html",context={'hata':hata})

   
   return render(request,"users/login.html",context={'form':form})

def user_logout(request):

    if request.user.is_authenticated!=True:
       return HttpResponseRedirect(reverse('postlar:post_lister'))
    logout(request)
    return HttpResponseRedirect(reverse("postlar:post_lister"))
   

def update_solved_problem_count(self):
    correct_solutions = UserProblemStatus.objects.filter(
        user__username=self.user.username,
    ).values('problem').distinct()
    
    self.solved_problem_count = correct_solutions.count()
    self.save()


def user_profile(request,username):
    user=UserProfile.objects.filter(user__username=username)
    rq_user=UserProfile.objects.filter(user=request.user)
    problem_count=UserProblemStatus.objects.filter(user__username=username)
    solution_count=Solution.objects.filter(user__username=username)
    user[0].update_solved_problem_count()
    print(rq_user[0].user.username)
    return render(request,'users/profile.html',context={'profile':user[0],'quser':rq_user[0],'problems':len(problem_count),'solutions':len(solution_count)})

@login_required
def update_profile(request,username):
    user=UserProfile.objects.filter(user__username=username)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profiles.first())
        
            

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            if 'delete_image' in request.POST and profile.profile_photo:
                profile.profile_photo.delete(save=False)  # Mevcut resmi dosya sisteminden sil
                profile.profile_photo = 'default/default_pfp.jpg'

            

            profile.save()
            return HttpResponseRedirect(reverse('users:profile_viewer',kwargs={'username': request.user.username}))
        
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=user[0])
            

    

    return render(request, 'users/user_settings.html', {
        'user_form': user_form,
        'profile_form': profile_form,'prof':user[0]
    })
# Create your views here.





def user_login_mobile(request):
   form=LoginForm(request.POST or None)
   if request.user.is_authenticated==True:
       return HttpResponseRedirect(reverse('postlar:post_lister'))
       
   if request.method == 'POST':
        if form.is_valid():
               yetkilimi=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
               if yetkilimi:
                   login(request,yetkilimi)
                   return HttpResponseRedirect(reverse('postlar:post_lister'))
               else:
                   hata="Kullanici adi ve ya parola yanlis"
                   return render(request,"users/login_mobile.html",context={'hata':hata})

   
   return render(request,"users/login_mobile.html",context={'form':form})


def sign_up_mobile(request):
    form=RegisterForm(request.POST or None)
    if request.user.is_authenticated==True:
       return HttpResponseRedirect(reverse('postlar:post_lister'))

    if form.is_valid():
        new_user=form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        yetkilimi=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
        if yetkilimi:
          login(request,yetkilimi)
          return HttpResponseRedirect(reverse('postlar:post_lister'))
    else:
       print(print(form.errors))
    
       
        
    return render(request,"users/sign_up_mobile.html",context={'form':form})



'''def user_profile_mobile(request,username):
    user=UserProfile.objects.filter(user__username=username)
    return render(request,'users/profile_mobile.html',context={'profile':user[0]})'''


def user_profile_mobile(request,username):
    user=UserProfile.objects.filter(user__username=username)
    problem_count=UserProblemStatus.objects.filter(user__username=username)
    solution_count=Solution.objects.filter(user__username=username)
    user[0].update_solved_problem_count()
    rq_user=UserProfile.objects.filter(user=request.user)
    realuser=request.user
    return render(request,'users/profile_mobile.html',context={'profile':user[0],'ruser':realuser,'quser':rq_user[0],'problems':len(problem_count),'solutions':len(solution_count)})



@login_required
def update_profile_mobile(request,username):
    user=UserProfile.objects.filter(user__username=username)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profiles.first())
        
            

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            if 'delete_image' in request.POST and profile.profile_photo:
                profile.profile_photo.delete(save=False)  # Mevcut resmi dosya sisteminden sil
                profile.profile_photo = 'default/default_pfp.jpg'

            

            profile.save()
            return HttpResponseRedirect(reverse('users:profile_mobile',kwargs={'username': request.user.username}))
        
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=user[0])
            

    

    return render(request, 'users/user_settings_mobile.html', {
        'user_form': user_form,
        'profile_form': profile_form,'prof':user[0]
    })