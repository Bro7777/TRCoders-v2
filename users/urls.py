from django.urls import path
from.views import *





urlpatterns = [
    path('signup',sign_up,name="signup"),
    path('login',user_login,name='login'),
    path('logout',user_logout,name="logout"),
    path('profile/<str:username>/',user_profile,name="profile_viewer"),
    path('profile/<str:username>/settings',update_profile,name="profile_updater"),


    path('login_mobile',user_login_mobile,name='login_mobile'),
    path('signup_mobile',sign_up_mobile,name='signup_mobile'),
    path('profile_mobile/<str:username>/',user_profile_mobile,name="profile_mobile"),
    path('profile_mobile/<str:username>/settings',update_profile_mobile,name="profile_updater_mobile"),


    
]