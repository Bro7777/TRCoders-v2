from django.urls import path

from.views import *

urlpatterns = [
    path('',ranking,name='ranking'),
    path('mobile',ranking_mobile,name='ranking_mobile')

]