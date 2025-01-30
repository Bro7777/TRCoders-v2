from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.urls import reverse
from.models import *
from users.models import UserProfile
from django.contrib.auth.decorators import login_required
import io
import sys
import docker
from.forms import SolutionForm
from.run_user_code import run_code_in_piston
from users.models import UserProblemStatus
from django.core.paginator import Paginator

# Create your views here.

def problem_detail(request,pk):
    problem=get_object_or_404(Problem,pk=pk)
    if request.user.is_authenticated:
        user=UserProfile.objects.filter(user__username=request.user.username)
        return render(request,'problems/detail.html',context={'problem':problem,'profile':user[0]})
    #user=UserProfile.objects.filter(user__username=request.user.username)
    return render(request,'problems/detail.html',context={'problem':problem})



import subprocess
import tempfile
import os
import json
import uuid
from django.utils.html import strip_tags
from bs4 import BeautifulSoup

import os

def read_test_cases_from_txt(test_cases):
    """
    TestCases queryset'i içindeki dosyaları okuyarak giriş ve beklenen çıkış verilerini döndürür.
    :param test_cases: TestCases queryset
    :return: List of tuples (input_data, expected_output)
    """
    test_data = []

    for test_case in test_cases:
        # Dosyaları oku
        try:
            with open(test_case.input_file.path, 'r') as input_f:
                input_data = input_f.read().strip()
            with open(test_case.output_file.path, 'r') as output_f:
                expected_output = output_f.read().strip()

            test_data.append((input_data, expected_output))
        except FileNotFoundError as e:
            print(f"Dosya bulunamadı: {e}")
        except Exception as e:
            print(f"Dosya okuma sırasında hata oluştu: {e}")

    return test_data

def convert_html_to_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text_lines = [line.get_text() for line in soup.find_all('p')]
    return "\n".join(text_lines)


@login_required(login_url="/users/login")
def submit_solution(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    form = SolutionForm(request.POST or None)
    profile=UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        code = request.POST.get("code")
        language = request.POST.get("language")
        test_cases = problem.test_cases.all()

        # Çözüm kaydı oluştur
        solution = Solution.objects.create(
            problem=problem,
            user=request.user,
            code=code,
            language=language,
        )

        results = []
        flag=True
        for test_case in test_cases:
            output, error, status_code = run_code_in_piston(
                language=language,
                code=code,
                input_data=test_case.input_data.strip()
            )

            if status_code != 200 or error:
                solution.feedback = f"Error: {error}"
                flag=False
                break

            is_correct = output.split() == test_case.expected_output.split()
            results.append(is_correct)
            print((test_case.expected_output.split()))
            print((output.split()))

            if not is_correct:
                solution.feedback = f"Yanlis cevap"
                flag=False
                #break
        
        if flag:
            solution.feedback=f"Tüm testler başarıyla geçti"

        # Sonuçları değerlendir
        solution.is_correct = all(results)
        status, created = UserProblemStatus.objects.get_or_create(user=request.user, problem=problem)
        if is_correct and not status.is_solved:
           status.is_solved = True
           profile.solved_problem_count+=1
           status.save()
           profile.save()
        print(results)
        solution.all_results=results
        solution.result_value=str(round((results.count(True)/len(results))*100,2))
        print(str(round(results.count(True)/len(results)*100,2)))
        solution.save()

        # Yönlendirme - Sonuçları problem detay sayfasında gösteriyoruz
        return HttpResponseRedirect(reverse('problems:solution', kwargs={'solution_id': solution.id}))

    return render(request, 'problems/submit_solution.html', {'form': form, 'problem': problem,'profile':profile})



@login_required(login_url="/users/login")
def solution_result(request, solution_id):
    solution = get_object_or_404(Solution, id=solution_id)
    results=solution.all_results
    user=UserProfile.objects.filter(user__username=request.user.username)
    return render(request, 'problems/solution.html', {'solution': solution,'results':results,'profile':user[0]})

@login_required(login_url="/users/login")
def problem_attempts(request,problem_id):
    problem=get_object_or_404(Problem,id=problem_id)
    user=UserProfile.objects.filter(user__username=request.user.username)
    attempts=Solution.objects.filter(problem=problem,user=request.user)
    return render(request,'problems/attempts.html',context={'problem':problem,'profile':user[0],'attempts':attempts[::-1]})

@login_required(login_url="/users/login")
def problem_stats(request,problem_id):
    problem=get_object_or_404(Problem,id=problem_id)
    user=UserProfile.objects.filter(user__username=request.user.username)
    attempts=Solution.objects.filter(problem=problem)
    successed=Solution.objects.filter(problem=problem,is_correct=True)
    success_rate=round(len(successed)/len(attempts)*100,2)
    return render(request,'problems/statistics.html',context={'problem':problem,'profile':user[0],'attempts_count':len(attempts),'successed':len(successed),'success_rate':success_rate})

def all_problems(request):
    problems=Problem.objects.all()
    paginator=Paginator(problems,20)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    if request.user.is_authenticated:
        user=UserProfile.objects.filter(user__username=request.user.username)
        return render(request,'problems/all.html',context={'page_obj':page_obj,'profile':user[0]})
    
    else:
        return render(request,'problems/all.html',context={'page_obj':page_obj})



#========================================  MOBILE VERSIONS  =========================================



def all_problems_mobile(request):
    problems=Problem.objects.all()
    paginator=Paginator(problems,20)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    if request.user.is_authenticated:
        user=UserProfile.objects.filter(user__username=request.user.username)
        return render(request,'problems/all_mobile.html',context={'page_obj':page_obj,'profile':user[0]})
    
    else:
        return render(request,'problems/all_mobile.html',context={'page_obj':page_obj})
    


def problem_detail_mobile(request,pk):
    problem=get_object_or_404(Problem,pk=pk)
    if request.user.is_authenticated:
        user=UserProfile.objects.filter(user__username=request.user.username)
        return render(request,'problems/detail_mobile.html',context={'problem':problem,'profile':user[0]})
    #user=UserProfile.objects.filter(user__username=request.user.username)
    return render(request,'problems/detail_mobile.html',context={'problem':problem})


@login_required(login_url="/users/login")
def submit_solution_mobile(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    form = SolutionForm(request.POST or None)
    profile=UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        code = request.POST.get("code")
        language = request.POST.get("language")
        test_cases = problem.test_cases.all()

        # Çözüm kaydı oluştur
        solution = Solution.objects.create(
            problem=problem,
            user=request.user,
            code=code,
            language=language,
        )

        results = []
        flag=True
        for test_case in test_cases:
            output, error, status_code = run_code_in_piston(
                language=language,
                code=code,
                input_data=test_case.input_data.strip()
            )

            if status_code != 200 or error:
                solution.feedback = f"Error: {error}"
                flag=False
                break

            is_correct = output.split() == test_case.expected_output.split()
            results.append(is_correct)
            print((test_case.expected_output.split()))
            print((output.split()))

            if not is_correct:
                solution.feedback = f"Yanlis cevap"
                flag=False
                #break
        
        if flag:
            solution.feedback=f"Tüm testler başarıyla geçti"

        # Sonuçları değerlendir
        solution.is_correct = all(results)
        status, created = UserProblemStatus.objects.get_or_create(user=request.user, problem=problem)
        if is_correct and not status.is_solved:
           status.is_solved = True
           profile.solved_problem_count+=1
           status.save()
           profile.save()
        print(results)
        solution.all_results=results
        solution.result_value=str(round((results.count(True)/len(results))*100,2))
        print(str(round(results.count(True)/len(results)*100,2)))
        solution.save()

        # Yönlendirme - Sonuçları problem detay sayfasında gösteriyoruz
        return HttpResponseRedirect(reverse('problems:solution_mobile', kwargs={'solution_id': solution.id}))

    return render(request, 'problems/submit_solution_mobile.html', {'form': form, 'problem': problem,'profile':profile})


@login_required(login_url="/users/login")
def solution_result_mobile(request, solution_id):
    solution = get_object_or_404(Solution, id=solution_id)
    results=solution.all_results
    user=UserProfile.objects.filter(user__username=request.user.username)
    return render(request, 'problems/solution_mobile.html', {'solution': solution,'results':results,'profile':user[0]})


@login_required(login_url="/users/login")
def problem_stat_mobile(request,problem_id):
    problem=get_object_or_404(Problem,id=problem_id)
    user=UserProfile.objects.filter(user__username=request.user.username)
    attempts=Solution.objects.filter(problem=problem)
    successed=Solution.objects.filter(problem=problem,is_correct=True)
    success_rate=round(len(successed)/len(attempts)*100,2)
    return render(request,'problems/statistics_mobile.html',context={'problem':problem,'profile':user[0],'attempts_count':len(attempts),'successed':len(successed),'success_rate':success_rate})


@login_required(login_url="/users/login")
def problem_attempts_mobile(request,problem_id):
    problem=get_object_or_404(Problem,id=problem_id)
    user=UserProfile.objects.filter(user__username=request.user.username)
    attempts=Solution.objects.filter(problem=problem,user=request.user)
    return render(request,'problems/attempts_mobile.html',context={'problem':problem,'profile':user[0],'attempts':attempts[::-1]})