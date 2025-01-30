from django.urls import path
from.views import *


urlpatterns = [
    path('index',index,name="index"),
    path('contact',index_contact,name="index_contact"),
    path('about',index_about,name="index_about"),
    path('in-dev',indev,name="indev"),
    path('index_mobile',index_mobile,name="index_mobile"),
    path('contact_mobile',index_contact_mobile,name="index_contact_mobile"),
    path('about_mobile',index_about_mobile,name="index_about_mobile")
]
