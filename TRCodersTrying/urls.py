#from django.contrib import admin
from django.urls import path
from.views import list_post
from.views import create_post
from.views import delete_post
from.views import *





urlpatterns = [
    path('posts',list_post,name="post_lister"),
    path('detail/<int:pk>/',post_detail,name='post_detail'),
    path('delete/<int:pk>',delete_post,name="post_deleter"),
    path('update/<int:pk>/',update_post,name='post_updater'),
    path('create',create_post,name="post_creater"),
    path('delete/comment/<int:pk>/',delete_comment,name='comment_deleter'),
    path('form',ornek_form,name='form_ornegi'),
    path('all',all_posts,name='all_posts'),

    path('posts_mobile',list_post_mobile,name="post_lister_mobile"),
    path('all_mobile',all_posts_mobile,name='all_posts_mobile'),
    path('detail_mobile/<int:pk>/',post_detail_mobile,name='post_detail_mobile'),
    path('create_mobile',create_post_mobile,name="post_creater_mobile"),
    path('update_mobile/<int:pk>/',update_post_mobile,name='post_updater_mobile'),

    
]