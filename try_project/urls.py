"""
URL configuration for try_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from TRCodersTrying.views import index,index_contact,index_about

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/',include(("TRCodersTrying.urls",'myapp'),namespace='postlar')),
    path('index/',include(("index.urls",'myapp'),namespace='index')),
    path('users/',include(("users.urls",'myapp'),namespace='users')),
    path('problems/',include(("problems.urls",'myapp'),namespace='problems')),
    path('groups/',include(("groups.urls",'myapp'),namespace='groups')),
    path('ranking/',include(("ranking.urls",'myapp'),namespace='rankings'))
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
