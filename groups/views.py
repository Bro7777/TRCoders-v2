from django.shortcuts import render

from.models import *
from users.models import UserProfile
from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from users.models import UserProfile
from problems.forms import SolutionForm
from problems.run_user_code import run_code_in_piston
from django.urls import reverse
from.forms import GroupForm

@login_required
def group_detail(request,pk):
    group=get_object_or_404(Group,pk=pk)
    user=UserProfile.objects.filter(user__username=request.user.username)
    return render(request,'groups/detail.html',context={'group':group,'profile':user[0]})


def group_leave(request,group_id):
    group=get_object_or_404(Group,id=group_id)
    member_to_remove = request.user
    if member_to_remove in group.members.all():
        group.members.remove(member_to_remove)
    return HttpResponseRedirect(reverse('groups:all_groups'))

def group_delete(request,group_id):
    group=get_object_or_404(Group,id=group_id)
    group.delete()
    return HttpResponseRedirect(reverse('groups:all_groups'))





def all_geoups(request):
    admin_groups = Group.objects.filter(admin=request.user)
    member_groups = Group.objects.filter(members=request.user)
    groups = (admin_groups | member_groups).distinct()
    print(len(groups))
    user=UserProfile.objects.filter(user__username=request.user.username)
    return render(request,'groups/all.html',context={'groups':groups,'profile':user[0]})


def members(request,group_id):
    group=get_object_or_404(Group,id=group_id)
    user=UserProfile.objects.filter(user__username=request.user.username)
    members=group.members.all()
    member_data = []
    for member in members:
        # Her üye için UserProfile alınır
        user_profile = UserProfile.objects.filter(user=member).first()
        member_data.append(user_profile)
    return render(request,'groups/members.html',context={'group':group,'profile':user[0],'members':member_data})
    
def all_lessons(request,group_id):
    group=get_object_or_404(Group,id=group_id)
    user=UserProfile.objects.filter(user__username=request.user.username)
    lessons=Lesson.objects.filter(group=group)
    return render(request,'groups/lessons.html',context={'group':group,'profile':user[0],'lessons':lessons})

def lesson_detail(request,group_id,lesson_id):
    group=get_object_or_404(Group,id=group_id)
    user=UserProfile.objects.filter(user__username=request.user.username)
    lesson=get_object_or_404(Lesson,id=lesson_id)
    return render(request,'groups/lesson_detail.html',context={'group':group,'profile':user[0],'lesson':lesson})


def lesson_tasks(request,group_id,lesson_id):
    group=get_object_or_404(Group,id=group_id)
    user=UserProfile.objects.filter(user__username=request.user.username)
    lesson=get_object_or_404(Lesson,id=lesson_id)
    tasks=lesson.group_lesson.all()
    return render(request,'groups/lesson_tasks.html',context={'group':group,'profile':user[0],'lesson':lesson,'tasks':tasks})


def task_detail(request,task_id,group_id,lesson_id):
    group=get_object_or_404(Group,id=group_id)
    user=UserProfile.objects.filter(user__username=request.user.username)
    lesson=get_object_or_404(Lesson,id=lesson_id)
    tasks=lesson.group_lesson.filter(id=task_id)
    
    return render(request,'groups/lesson_task_detail.html',context={'task':tasks[0],'lesson':lesson,'group':group,'profile':user[0]})

def task_submit_solution(request,task_id,group_id,lesson_id):
    
    form = SolutionForm(request.POST or None)
    profile=UserProfile.objects.get(user=request.user)
    group=get_object_or_404(Group,id=group_id)
    lesson=get_object_or_404(Lesson,id=lesson_id)
    tasks=lesson.group_lesson.filter(id=task_id)
    task=tasks[0]

    if request.method == "POST":
        code = request.POST.get("code")
        language = request.POST.get("language")
        test_cases = task.problem.test_cases.all()

        # Çözüm kaydı oluştur
        solution = GroupLessonSolution.objects.create(
            problem=task,
            user=request.user,
            code=code,
            language=language,
            group=group,
            lesson=lesson,
        )

        results = []
        for test_case in test_cases:
            output, error, status_code = run_code_in_piston(
                language=language,
                code=code,
                input_data=test_case.input_data.strip()
            )

            if status_code != 200 or error:
                solution.feedback = f"Error: {error}"
                break

            is_correct = output.split() == test_case.expected_output.split()
            results.append(is_correct)
            print((test_case.expected_output.split()))
            print((output.split()))

            if not is_correct:
                solution.feedback = f"Yanlis cevap"
                #break

        # Sonuçları değerlendir
        solution.is_correct = all(results)
        '''status, created = LessonUserProblemStatus.objects.get_or_create(user=request.user, problem=task)
        if is_correct and not status.is_solved:
           status.percent_of_success=str(round((results.count(True)/len(results))*100,2))
           status.group=group
           status.lesson=lesson
           status.is_solved = True
           status.save()'''
        print(results)
        solution.all_results=results
        solution.result_value=str(round((results.count(True)/len(results))*100,2))
        print(str(round(results.count(True)/len(results)*100,2)))
        solution.save()

        # Yönlendirme - Sonuçları problem detay sayfasında gösteriyoruz
        return HttpResponseRedirect(reverse('groups:task_solution_result', kwargs={'solution_id': solution.id,'group_id':group.id,'lesson_id':lesson.id}))

    return render(request, 'groups/lesson_submit_solution.html', {'form': form, 'problem': task.problem,'profile':profile,'group':group,'lesson':lesson})


def task_solution_result(request, solution_id,group_id,lesson_id):
    solution = get_object_or_404(GroupLessonSolution, id=solution_id)
    group=get_object_or_404(Group,id=group_id)
    lesson=get_object_or_404(Lesson,id=lesson_id)
    results=solution.all_results
    user=UserProfile.objects.filter(user__username=request.user.username)
    return render(request, 'groups/lesson_task_solution.html', {'solution': solution,'results':results,'profile':user[0],'group':group,'lesson':lesson})


from django.db.models import F, Sum,Max

def leaderboard(request,group_id,lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    group=get_object_or_404(Group,id=group_id)
    solutions=GroupLessonSolution.objects.filter(group=group,lesson=lesson)
    problems=lesson.group_lesson.all()
    user=UserProfile.objects.filter(user__username=request.user.username)

    
    # Belirli bir grup ve derse ait kullanıcı puanları
    user_scores = (
        GroupLessonSolution.objects.filter(group_id=group_id, lesson_id=lesson_id)
        .values('user__username', 'problem__problem__title', 'problem__id')
        .annotate(highest_score=Max('result_value'))  # En yüksek puanı alıyoruz
        .values('user__username', 'problem__id', 'highest_score')
        
    )

    total_scores = {}
    for score in user_scores:
        username = score['user__username']
        if username not in total_scores:
            total_scores[username] = {'username': username, 'total': 0, 'problems': {}}
        total_scores[username]['problems'][score['problem__id']] = score['highest_score']
        total_scores[username]['total'] += float(score['highest_score'])

    # Template için kullanıcı skorlarını liste olarak hazırla
    leaderboard = list(total_scores.values())
    leaderboard = sorted(leaderboard, key=lambda x: x['total'], reverse=True)
    
    return render(request, 'groups/lesson_leaderboard.html', {'user_scores': user_scores,'group':group,'lesson':lesson,'problems':problems,'leaderboard':leaderboard,'profile':user[0]})
    

from django.http import JsonResponse
from django.contrib.auth.models import User

def search_users(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(username__icontains=query).values('id', 'username')
        return JsonResponse(list(users), safe=False)
    return JsonResponse([], safe=False)


def search_problems(request,group_id,lesson_id):
    query = request.GET.get('q', '')
    #group_id=request.GET.get('group_id','')
    #lesson_id=request.GET.get('lesson_id','')
    group=get_object_or_404(Group,id=group_id)
    lesson=get_object_or_404(Lesson,id=lesson_id)
    #existing_problems=lesson.group_lesson.all()
    existing_problem_ids = lesson.group_lesson.values_list('problem__id', flat=True)

    if query:
        problems = Problem.objects.filter(title__icontains=query ).exclude(id__in=existing_problem_ids).values('id', 'title')  
        return JsonResponse(list(problems), safe=False) 
    return JsonResponse([], safe=False)

from django.views.decorators.csrf import csrf_exempt

def search_users_while_group(request):
    query = request.GET.get('q', '')
    group_id=request.GET.get('group_id','')
    group=get_object_or_404(Group,id=group_id)
    print(group_id)
    #group=Group.objects.get(id=group_id)
    existing_members = group.members.all()
    if query:
        users = User.objects.filter(username__icontains=query).exclude(id__in=existing_members).values('id', 'username')
        return JsonResponse(list(users), safe=False)
    return JsonResponse([], safe=False)


def create_group_step1(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        group_description = request.POST.get('group_description')

        # Yeni grup oluştur ve kaydet
        group = Group.objects.create(name=group_name, description=group_description,admin=request.user)
        return HttpResponseRedirect(reverse('groups:create_group_step2', kwargs={'group_id':group.id}))

    return render(request, 'groups/create_group_step1.html')


def create_group_step2(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        # Üyeleri ekle
        user_ids_raw = request.POST.get('members', '')
        user_ids = [int(uid.strip()) for uid in user_ids_raw.split(',') if uid.strip().isdigit()]
        
        if user_ids:
            users = User.objects.filter(id__in=user_ids)
            group.members.add(*users)  # Kullanıcıları gruba ekle
        return HttpResponseRedirect(reverse('groups:group_detail', kwargs={'pk':group.pk}))

    # Kullanıcıları ara
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query) if query else User.objects.none()

    return render(request, 'groups/create_group_step2.html', {'group': group, 'users': users})


def group_setting_main(request,group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.user != group.admin:  # 'admin' alanı grup yöneticisini temsil etmeli
        return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok.")

    if request.method == 'POST':
        group.name = request.POST.get('name', group.name)
        group.description = request.POST.get('description', group.description)
        group.save()
        return HttpResponseRedirect(reverse('groups:settings',kwargs={'group_id':group.id}))

    return render(request, 'groups/group_settings.html',{'group': group})


def group_setting_members(request,group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.user != group.admin:  # 'admin' alanı grup yöneticisini temsil etmeli
        return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok.")
    
    members=group.members.all()
    
    if request.method=="POST":
        member_id = request.POST.get('member_id')
        member_to_remove = get_object_or_404(group.members, id=member_id)
        group.members.remove(member_to_remove)
        return HttpResponseRedirect(reverse('groups:member_management',kwargs={'group_id':group.id}))

    return render(request,'groups/group_user_settings.html',{'group':group,'members':members})

def group_add_members(request,group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        # Üyeleri ekle
        user_ids_raw = request.POST.get('members', '')
        user_ids = [int(uid.strip()) for uid in user_ids_raw.split(',') if uid.strip().isdigit()]
        
        if user_ids:
            users = User.objects.filter(id__in=user_ids)
            group.members.add(*users)  # Kullanıcıları gruba ekle
        return HttpResponseRedirect(reverse('groups:group_detail', kwargs={'pk':group.pk}))

    # Kullanıcıları ara
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query) if query else User.objects.none()

    return render(request, 'groups/group_add.html', {'group': group, 'users': users})

def create_lesson(request,group_id):
    group=get_object_or_404(Group,id=group_id)
    if request.method == 'POST':
        lesson_name = request.POST.get('lesson_name')
        lesson_description = request.POST.get('lesson_description')
        pdf=request.FILES.get('pdf')
        #if pdf:
        lesson=Lesson.objects.create(title=lesson_name,description=lesson_description,group=group,pdf=pdf)
        '''else:
            lesson=Lesson.objects.create(title=lesson_name,description=lesson_description,group=group)
        '''
        return HttpResponseRedirect(reverse('groups:add_problems', kwargs={'group_id': group.id, 'lesson_id': lesson.id}))
    
    return render(request, 'groups/create_lesson.html')


def add_problems_to_lesson(request, group_id, lesson_id):
    group = get_object_or_404(Group, id=group_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, group=group)

    if request.method == 'POST':
        # Problem ID'lerini al ve derse ekle
        problem_ids_raw = request.POST.getlist('problems')  # 'getlist' kullanarak tüm değerleri alın
        problem_ids = [int(pid.strip()) for pid in problem_ids_raw if pid.strip().isdigit()]
        
        if problem_ids:
            problems = Problem.objects.filter(id__in=problem_ids)
            for problem in problems:
                GroupLessonProblem.objects.create(group=group, lesson=lesson, problem=problem)
        
        return HttpResponseRedirect(reverse('groups:lesson_detail', kwargs={'group_id': group.id, 'lesson_id': lesson.id}))

    # Arama işlemi
    existing_problem_ids = lesson.group_lesson.values_list('problem__id', flat=True)
    query = request.GET.get('q', '')
    
    problems = Problem.objects.filter(title__icontains=query).exclude(id__in=existing_problem_ids) if query else Problem.objects.none()

    return render(request, 'groups/lesson_add_problems.html', {
        'group': group,
        'lesson': lesson,
        'selected_problems': problems,
    })


def lesson_settings(request,lesson_id,group_id):
    group=get_object_or_404(Group,id=group_id)
    lesson=get_object_or_404(Lesson,id=lesson_id)
    if request.user != group.admin:  # 'admin' alanı grup yöneticisini temsil etmeli
        return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok.")
    
    if request.method == 'POST':
        lesson.title = request.POST.get('title', lesson.title)
        lesson.description = request.POST.get('description', lesson.description)
        pdf=request.FILES.get('pdf')
        lesson.pdf=pdf
        lesson.save()
        return HttpResponseRedirect(reverse('groups:lesson_detail', kwargs={'group_id': group.id, 'lesson_id': lesson.id}))


    return render(request, 'groups/lesson_settings.html',context={'lesson':lesson,'group':group})


def lesson_task_settings(request,lesson_id,group_id):
    group = get_object_or_404(Group, id=group_id)
    lesson=get_object_or_404(Lesson,id=lesson_id)

    if request.user != group.admin:  # 'admin' alanı grup yöneticisini temsil etmeli
        return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok.")
    
    problems=lesson.group_lesson.all()
    if request.method == 'POST':
        problem_id = request.POST.get('problem_id')
        problem = get_object_or_404(GroupLessonProblem, id=problem_id)
        problem.delete()
        return HttpResponseRedirect(reverse("groups:lesson_task_settings",kwargs={'group_id':group.id,'lesson_id':lesson.id}))
    return render(request,'groups/lesson_task_settings.html',{'group':group,'problems':problems,'lesson':lesson})



#========================================  MOBILE VERSIONS  ================================================



def all_geoups_mobile(request):
    admin_groups = Group.objects.filter(admin=request.user)
    member_groups = Group.objects.filter(members=request.user)
    groups = (admin_groups | member_groups).distinct()
    print(len(groups))
    user=UserProfile.objects.filter(user__username=request.user.username)
    return render(request,'groups/all_mobile.html',context={'groups':groups,'profile':user[0]})
        
@login_required
def group_detail_mobile(request,pk):
    group=get_object_or_404(Group,pk=pk)
    user=UserProfile.objects.filter(user__username=request.user.username)
    return render(request,'groups/detail_mobile.html',context={'group':group,'profile':user[0]})

def members_mobile(request,group_id):
    group=get_object_or_404(Group,id=group_id)
    user=UserProfile.objects.filter(user__username=request.user.username)
    members=group.members.all()
    member_data = []
    for member in members:
        # Her üye için UserProfile alınır
        user_profile = UserProfile.objects.filter(user=member).first()
        member_data.append(user_profile)
    return render(request,'groups/members_mobile.html',context={'group':group,'profile':user[0],'members':member_data})
    
def all_lessons_mobile(request,group_id):
    group=get_object_or_404(Group,id=group_id)
    user=UserProfile.objects.filter(user__username=request.user.username)
    lessons=Lesson.objects.filter(group=group)
    return render(request,'groups/lessons_mobile.html',context={'group':group,'profile':user[0],'lessons':lessons})


def lesson_detail_mobile(request,group_id,lesson_id):
    group=get_object_or_404(Group,id=group_id)
    user=UserProfile.objects.filter(user__username=request.user.username)
    lesson=get_object_or_404(Lesson,id=lesson_id)
    return render(request,'groups/lesson_detail_mobile.html',context={'group':group,'profile':user[0],'lesson':lesson})



def lesson_tasks_mobile(request,group_id,lesson_id):
    group=get_object_or_404(Group,id=group_id)
    user=UserProfile.objects.filter(user__username=request.user.username)
    lesson=get_object_or_404(Lesson,id=lesson_id)
    tasks=lesson.group_lesson.all()
    return render(request,'groups/lesson_tasks_mobile.html',context={'group':group,'profile':user[0],'lesson':lesson,'tasks':tasks})


def leaderboard_mobile(request,group_id,lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    group=get_object_or_404(Group,id=group_id)
    solutions=GroupLessonSolution.objects.filter(group=group,lesson=lesson)
    problems=lesson.group_lesson.all()
    user=UserProfile.objects.filter(user__username=request.user.username)

    
    # Belirli bir grup ve derse ait kullanıcı puanları
    user_scores = (
        GroupLessonSolution.objects.filter(group_id=group_id, lesson_id=lesson_id)
        .values('user__username', 'problem__problem__title', 'problem__id')
        .annotate(highest_score=Max('result_value'))  # En yüksek puanı alıyoruz
        .values('user__username', 'problem__id', 'highest_score')
        
    )

    total_scores = {}
    for score in user_scores:
        username = score['user__username']
        if username not in total_scores:
            total_scores[username] = {'username': username, 'total': 0, 'problems': {}}
        total_scores[username]['problems'][score['problem__id']] = score['highest_score']
        total_scores[username]['total'] += float(score['highest_score'])

    # Template için kullanıcı skorlarını liste olarak hazırla
    leaderboard = list(total_scores.values())
    leaderboard = sorted(leaderboard, key=lambda x: x['total'], reverse=True)
    
    return render(request, 'groups/lesson_leaderboard_mobile.html', {'user_scores': user_scores,'group':group,'lesson':lesson,'problems':problems,'leaderboard':leaderboard,'profile':user[0]})



def task_detail_mobile(request,task_id,group_id,lesson_id):
    group=get_object_or_404(Group,id=group_id)
    user=UserProfile.objects.filter(user__username=request.user.username)
    lesson=get_object_or_404(Lesson,id=lesson_id)
    tasks=lesson.group_lesson.filter(id=task_id)
    task=tasks[0]
    
    return render(request,'groups/lesson_task_detail_mobile.html',context={'task':task,'lesson':lesson,'group':group,'profile':user[0]})



def task_submit_solution_mobile(request,task_id,group_id,lesson_id):
    
    form = SolutionForm(request.POST or None)
    profile=UserProfile.objects.get(user=request.user)
    group=get_object_or_404(Group,id=group_id)
    lesson=get_object_or_404(Lesson,id=lesson_id)
    tasks=lesson.group_lesson.filter(id=task_id)
    task=tasks[0]
    print(task.id)

    if request.method == "POST":
        code = request.POST.get("code")
        language = request.POST.get("language")
        test_cases = task.problem.test_cases.all()

        # Çözüm kaydı oluştur
        solution = GroupLessonSolution.objects.create(
            problem=task,
            user=request.user,
            code=code,
            language=language,
            group=group,
            lesson=lesson,
        )

        results = []
        for test_case in test_cases:
            output, error, status_code = run_code_in_piston(
                language=language,
                code=code,
                input_data=test_case.input_data.strip()
            )

            if status_code != 200 or error:
                solution.feedback = f"Error: {error}"
                break

            is_correct = output.split() == test_case.expected_output.split()
            results.append(is_correct)
            print((test_case.expected_output.split()))
            print((output.split()))

            if not is_correct:
                solution.feedback = f"Yanlis cevap"
                #break

        # Sonuçları değerlendir
        solution.is_correct = all(results)
        '''status, created = LessonUserProblemStatus.objects.get_or_create(user=request.user, problem=task)
        if is_correct and not status.is_solved:
           status.percent_of_success=str(round((results.count(True)/len(results))*100,2))
           status.group=group
           status.lesson=lesson
           status.is_solved = True
           status.save()'''
        print(results)
        solution.all_results=results
        solution.result_value=str(round((results.count(True)/len(results))*100,2))
        print(str(round(results.count(True)/len(results)*100,2)))
        solution.save()

        # Yönlendirme - Sonuçları problem detay sayfasında gösteriyoruz
        return HttpResponseRedirect(reverse('groups:task_solution_result', kwargs={'solution_id': solution.id,'group_id':group.id,'lesson_id':lesson.id}))

    return render(request, 'groups/lesson_submit_solution_mobile.html', {'form': form, 'problem': task.problem,'profile':profile,'group':group,'lesson':lesson,'task':task})


def task_solution_result_mobile(request, solution_id,group_id,lesson_id):
    solution = get_object_or_404(GroupLessonSolution, id=solution_id)
    group=get_object_or_404(Group,id=group_id)
    lesson=get_object_or_404(Lesson,id=lesson_id)
    results=solution.all_results
    user=UserProfile.objects.filter(user__username=request.user.username)
    return render(request, 'groups/lesson_task_solution_mobile.html', {'solution': solution,'results':results,'profile':user[0],'group':group,'lesson':lesson})


def create_group_step1_mobile(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        group_description = request.POST.get('group_description')

        # Yeni grup oluştur ve kaydet
        group = Group.objects.create(name=group_name, description=group_description,admin=request.user)
        return HttpResponseRedirect(reverse('groups:create_group_step2_mobile', kwargs={'group_id':group.id}))

    return render(request, 'groups/create_group_step1_mobile.html')


def create_group_step2_mobile(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        # Üyeleri ekle
        user_ids_raw = request.POST.get('members', '')
        user_ids = [int(uid.strip()) for uid in user_ids_raw.split(',') if uid.strip().isdigit()]
        
        if user_ids:
            users = User.objects.filter(id__in=user_ids)
            group.members.add(*users)  # Kullanıcıları gruba ekle
        return HttpResponseRedirect(reverse('groups:group_detail_mobile', kwargs={'pk':group.pk}))

    # Kullanıcıları ara
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query) if query else User.objects.none()

    return render(request, 'groups/create_group_step2_mobile.html', {'group': group, 'users': users})


def group_setting_main_mobile(request,group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.user != group.admin:  # 'admin' alanı grup yöneticisini temsil etmeli
        return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok.")

    if request.method == 'POST':
        group.name = request.POST.get('name', group.name)
        group.description = request.POST.get('description', group.description)
        group.save()
        return HttpResponseRedirect(reverse('groups:settings',kwargs={'group_id':group.id}))

    return render(request, 'groups/group_settings_mobile.html',{'group': group})


def group_setting_members_mobile(request,group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.user != group.admin:  # 'admin' alanı grup yöneticisini temsil etmeli
        return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok.")
    
    members=group.members.all()
    
    if request.method=="POST":
        member_id = request.POST.get('member_id')
        member_to_remove = get_object_or_404(group.members, id=member_id)
        group.members.remove(member_to_remove)
        return HttpResponseRedirect(reverse('groups:member_management_mobile',kwargs={'group_id':group.id}))

    return render(request,'groups/group_user_settings_mobile.html',{'group':group,'members':members})


def group_add_members_mobile(request,group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        # Üyeleri ekle
        user_ids_raw = request.POST.get('members', '')
        user_ids = [int(uid.strip()) for uid in user_ids_raw.split(',') if uid.strip().isdigit()]
        
        if user_ids:
            users = User.objects.filter(id__in=user_ids)
            group.members.add(*users)  # Kullanıcıları gruba ekle
        return HttpResponseRedirect(reverse('groups:group_detail_mobile', kwargs={'pk':group.pk}))

    # Kullanıcıları ara
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query) if query else User.objects.none()

    return render(request, 'groups/group_add_mobile.html', {'group': group, 'users': users})


def create_lesson_mobile(request,group_id):
    group=get_object_or_404(Group,id=group_id)
    if request.method == 'POST':
        lesson_name = request.POST.get('lesson_name')
        lesson_description = request.POST.get('lesson_description')
        pdf=request.FILES.get('pdf')
        #if pdf:
        lesson=Lesson.objects.create(title=lesson_name,description=lesson_description,group=group,pdf=pdf)
        '''else:
            lesson=Lesson.objects.create(title=lesson_name,description=lesson_description,group=group)
        '''
        return HttpResponseRedirect(reverse('groups:add_problems_mobile', kwargs={'group_id': group.id, 'lesson_id': lesson.id}))
    
    return render(request, 'groups/create_lesson_mobile.html',{'group':group})


def add_problems_to_lesson_mobile(request, group_id, lesson_id):
    group = get_object_or_404(Group, id=group_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, group=group)

    if request.method == 'POST':
        # Problem ID'lerini al ve derse ekle
        problem_ids_raw = request.POST.getlist('problems')  # 'getlist' kullanarak tüm değerleri alın
        problem_ids = [int(pid.strip()) for pid in problem_ids_raw if pid.strip().isdigit()]
        
        if problem_ids:
            problems = Problem.objects.filter(id__in=problem_ids)
            for problem in problems:
                GroupLessonProblem.objects.create(group=group, lesson=lesson, problem=problem)
        
        return HttpResponseRedirect(reverse('groups:lesson_detail_mobile', kwargs={'group_id': group.id, 'lesson_id': lesson.id}))

    # Arama işlemi
    existing_problem_ids = lesson.group_lesson.values_list('problem__id', flat=True)
    query = request.GET.get('q', '')
    
    problems = Problem.objects.filter(title__icontains=query).exclude(id__in=existing_problem_ids) if query else Problem.objects.none()

    return render(request, 'groups/lesson_add_problems_mobile.html', {
        'group': group,
        'lesson': lesson,
        'selected_problems': problems,
    })


def lesson_settings_mobile(request,lesson_id,group_id):
    group=get_object_or_404(Group,id=group_id)
    lesson=get_object_or_404(Lesson,id=lesson_id)
    if request.user != group.admin:  # 'admin' alanı grup yöneticisini temsil etmeli
        return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok.")
    
    if request.method == 'POST':
        lesson.title = request.POST.get('title', lesson.title)
        lesson.description = request.POST.get('description', lesson.description)
        pdf=request.FILES.get('pdf')
        lesson.pdf=pdf
        lesson.save()
        return HttpResponseRedirect(reverse('groups:lesson_detail_mobile', kwargs={'group_id': group.id, 'lesson_id': lesson.id}))


    return render(request, 'groups/lesson_settings_mobile.html',context={'lesson':lesson,'group':group})


def lesson_task_settings_mobile(request,lesson_id,group_id):
    group = get_object_or_404(Group, id=group_id)
    lesson=get_object_or_404(Lesson,id=lesson_id)

    if request.user != group.admin:  # 'admin' alanı grup yöneticisini temsil etmeli
        return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok.")
    
    problems=lesson.group_lesson.all()
    if request.method == 'POST':
        problem_id = request.POST.get('problem_id')
        problem = get_object_or_404(GroupLessonProblem, id=problem_id)
        problem.delete()
        return HttpResponseRedirect(reverse("groups:lesson_task_settings_mobile",kwargs={'group_id':group.id,'lesson_id':lesson.id}))
    return render(request,'groups/lesson_task_settings_mobile.html',{'group':group,'problems':problems,'lesson':lesson})

