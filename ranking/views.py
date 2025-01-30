
from django.shortcuts import render
from django.core.paginator import Paginator
from.models import *
from users.models import UserProfile
from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from users.models import UserProfile


def ranking(request):
    leaderboard = UserProfile.objects.all().order_by('-solved_problem_count')
    paginator = Paginator(leaderboard, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'users': leaderboard,
    }

    if request.user.is_authenticated:
        user = UserProfile.objects.filter(user=request.user).first()
        if user:
            context['profile'] = user

    return render(request, 'ranking/ranking.html', context)

def ranking_mobile(request):
    leaderboard = UserProfile.objects.all().order_by('-solved_problem_count')
    paginator = Paginator(leaderboard, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'users': leaderboard,
    }

    if request.user.is_authenticated:
        user = UserProfile.objects.filter(user=request.user).first()
        if user:
            context['profile'] = user

    return render(request, 'ranking/ranking_mobile.html', context)

# Create your views here.
