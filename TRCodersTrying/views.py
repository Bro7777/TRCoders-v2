from django.shortcuts import render,HttpResponse,HttpResponsePermanentRedirect,get_object_or_404,HttpResponseRedirect
from django.urls import reverse
from.models import Post,Comment
from.forms import Postform,Commentform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
from django.contrib.auth import authenticate
from problems.models import *

def index(request):
    return render(request,'index/index.html')

def index_contact(request):
    return render(request,'index/index_contact.html')

def index_about(request):
    return render(request,'index/index_about.html')


# Create your views here.


#Admin ucun post(duyuru) duzeltme hissesi
def ornek_form(request):
    konu=None
    icerik=None
    if request.method=="POST":
        icerik=request.POST.get('mesaj')
        konu=request.POST.get('Konu')

    
    return render(request,'posts/forms.html',context={'gelen mesaj':icerik,'konu':konu})

@login_required(login_url="/users/login/")
def create_post(request):
    post_form=Postform()
    if request.method=="POST":
        post_form=Postform(request.POST,request.FILES)
        if post_form.is_valid():
            post=post_form.save(commit=False)
            post.user=request.user
            post.save()
            messages.success(request,"Gonderi basariyla olusturuldu.")
            return HttpResponsePermanentRedirect(reverse('postlar:post_lister'))
    return render(request,'posts/create_post.html',context={'forms':post_form})
@login_required( login_url="/users/login")
def update_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    form=Postform(instance=post)
    if request.method=="POST":
        form=Postform(data=request.POST,instance=post,files=request.FILES or None)

        if 'delete_image' in request.POST and post.image:
            post.image.delete()  # Fotoğrafı sil
            post.image = None
        if form.is_valid():
            form.save(commit=True)
            messages.success(request,"Gonderi basariyla guncellendi.")
            print(form.instance.id)
            return HttpResponsePermanentRedirect(reverse('postlar:post_detail',kwargs={'pk':form.instance.id}))
    print(post.pk)
    return render(request,'posts/update_post.html',context={'forms':form,'post':post})

def list_post(request):
    posts=Post.objects.all()
    problems=Problem.objects.all()
    #user=UserProfile.objects.filter(user__username=request.user.username)
    if request.user.is_authenticated:
        user=UserProfile.objects.filter(user__username=request.user.username)
        return render(request,'posts/Trying_Main.html',context={'post_list':(posts[::-1])[0:3],'profile':user[0],'problems':problems})
    
    else:
        return render(request,'posts/Trying_Main.html',context={'post_list':(posts[::-1])[0:3],'problems':problems})
    #return render(request,'posts/Trying_Main.html',context={,'profile':user[0]})

def all_posts(request):
    #user=UserProfile.objects.filter(user__username=request.user.username)
    posts=Post.objects.all()
    paginator = Paginator(posts, 5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    if request.user.is_authenticated:
        user=UserProfile.objects.filter(user__username=request.user.username)
        return render(request,'posts/all.html',context={'page_obj':page_obj,'profile':user[0]})
    
    else:
        return render(request,'posts/all.html',context={'page_obj':page_obj})




def post_detail(request,pk):
    #post=Post.objects.get(pk=pk)
    post=get_object_or_404(Post,pk=pk)
    scroll_to_top = False
    comments = post.comment.all()
    
    commentform=Commentform(request.POST or None)
    flag=False
    if request.user.is_authenticated:
        user=UserProfile.objects.filter(user__username=request.user.username)
        flag=True
    
    
    if request.method == 'POST':
        commentform = Commentform(request.POST)
        if request.user.is_authenticated!=True:
           return HttpResponseRedirect(reverse('users:login'))
        if commentform.is_valid():
            comment = commentform.save(commit=False)
            comment.post = post
            comment.user=request.user
            comment.save()
            commentform = Commentform() 
            scroll_to_top = True 


    if flag:
        return render(request,'posts/detail.html',context={'post':post,'commentform':commentform,'scroll_to_top': scroll_to_top,'comments':comments,'profile':user[0]})

    return render(request,'posts/detail.html',context={'post':post,'commentform':commentform,'scroll_to_top': scroll_to_top,'comments':comments})

def delete_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.delete()
    messages.success(request,"Gonderi basariyla silindi.")
    return HttpResponsePermanentRedirect(reverse('postlar:post_lister_mobile'))


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.user:  # Kullanıcının yetkisini kontrol et
        comment.delete()
    return HttpResponseRedirect(reverse('postlar:post_detail_mobile', kwargs={'pk':comment.post.pk} ))  # Posta geri yönlendir
    




def list_post_mobile(request):
    posts=Post.objects.all()
    problems=Problem.objects.all()
    #user=UserProfile.objects.filter(user__username=request.user.username)
    if request.user.is_authenticated:
        user=UserProfile.objects.filter(user__username=request.user.username)
        return render(request,'posts/Trying_Main_mobile.html',context={'post_list':(posts[::-1])[0:3],'profile':user[0],'problems':problems})
    
    else:
        return render(request,'posts/Trying_Main_mobile.html',context={'post_list':(posts[::-1])[0:3],'problems':problems})
    

def all_posts_mobile(request):
    #user=UserProfile.objects.filter(user__username=request.user.username)
    posts=Post.objects.all()
    paginator = Paginator(posts, 5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    if request.user.is_authenticated:
        user=UserProfile.objects.filter(user__username=request.user.username)
        return render(request,'posts/all_mobile.html',context={'page_obj':page_obj,'profile':user[0]})
    
    else:
        return render(request,'posts/all_mobile.html',context={'page_obj':page_obj})
    

def post_detail_mobile(request,pk):
    #post=Post.objects.get(pk=pk)
    post=get_object_or_404(Post,pk=pk)
    scroll_to_top = False
    comments = post.comment.all()
    
    commentform=Commentform(request.POST or None)
    
    
    
    if request.method == 'POST':
        commentform = Commentform(request.POST)
        if request.user.is_authenticated!=True:
           return HttpResponseRedirect(reverse('users:login_mobile'))
        if commentform.is_valid():
            comment = commentform.save(commit=False)
            comment.post = post
            comment.user=request.user
            comment.save()
            commentform = Commentform() 
            scroll_to_top = True 
    if request.user.is_authenticated:
        user=UserProfile.objects.filter(user__username=request.user.username)
        return render(request,'posts/detail_mobile.html',context={'post':post,'commentform':commentform,'scroll_to_top': scroll_to_top,'comments':comments,'profile':user[0]})


    
    return render(request,'posts/detail_mobile.html',context={'post':post,'commentform':commentform,'scroll_to_top': scroll_to_top,'comments':comments})


@login_required(login_url="/users/login/")
def create_post_mobile(request):
    user=UserProfile.objects.filter(user__username=request.user.username)
    post_form=Postform()
    if request.method=="POST":
        post_form=Postform(request.POST,request.FILES)
        if post_form.is_valid():
            post=post_form.save(commit=False)
            post.user=request.user
            post.save()
            messages.success(request,"Gonderi basariyla olusturuldu.")
            return HttpResponsePermanentRedirect(reverse('postlar:post_lister_mobile'))
    return render(request,'posts/create_post_mobile.html',context={'forms':post_form,'profile':user[0]})

@login_required(login_url="/users/login/")
def update_post_mobile(request,pk):
    user=UserProfile.objects.filter(user__username=request.user.username)
    post=get_object_or_404(Post,pk=pk)
    form=Postform(instance=post)
    if request.method=="POST":
        form=Postform(data=request.POST,instance=post,files=request.FILES or None)

        if 'delete_image' in request.POST and post.image:
            post.image.delete()  # Fotoğrafı sil
            post.image = None
        if form.is_valid():
            form.save(commit=True)
            messages.success(request,"Gonderi basariyla guncellendi.")
            return HttpResponseRedirect(reverse('postlar:post_detail_mobile',kwargs={'pk':form.instance.id}))
    print(post.pk)
    return render(request,'posts/update_post_mobile.html',context={'forms':form,'post':post,'profile':user[0]})