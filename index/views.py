from django.shortcuts import render


def index(request):
    return render(request,'index/index.html')

def index_contact(request):
    return render(request,'index/index_contact.html')

def index_about(request):
    return render(request,'index/index_about.html')

def indev(request):
    return render(request,'index/in_dev.html')

def index_mobile(request):
    return render(request,'index/index_mobile.html')

def index_contact_mobile(request):
    return render(request,'index/index_contact_mobile.html')

def index_about_mobile(request):
    return render(request,'index/index_about_mobile.html')

# Create your views here.
