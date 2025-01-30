from django.db import models
from django.contrib.auth.models import User
from problems.models import Problem  # TRCoders problem seti
from ckeditor.fields import RichTextField
from problems.models import *
import os


    
class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_groups")
    members = models.ManyToManyField(User, related_name="member_groups", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

def lesson_pdf_upload_path(instance, filename):
    # Grup ismini ve ders başlığını al
    group_name = instance.group.name.replace(' ', '_')  # Boşlukları "_" ile değiştir
    lesson_title = instance.title.replace(' ', '_')  # Boşlukları "_" ile değiştir

    # Dosyanın kaydedileceği yolu oluştur
    return os.path.join('lesson_pdfs', group_name, lesson_title, filename)

class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = RichTextField()
    pdf = models.FileField(upload_to=lesson_pdf_upload_path, blank=True, null=True)
    #problems = models.ManyToManyField(Problem, related_name='lesson_problems')

    def __str__(self):
        return f"{self.title} ({self.group.name})"



class GroupLessonProblem(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name="group_of_lesson")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='group_lesson')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='group_lesson_problems')
    max_score = models.IntegerField(default=100)



class GroupLessonSolution(models.Model):
    PROGRAMMING_LAGUAGE=[
        ('python','Python3'),
        ('cpp','C++20')
    ]
    lesson=models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name="pol",default=1)
    group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name="problem_of_lesson",default=1)
    problem=models.ForeignKey(GroupLessonProblem,on_delete=models.CASCADE,related_name='group_lesson_solutions')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.TextField(help_text="Kullanıcının kodu")
    language=models.CharField(max_length=20,choices=PROGRAMMING_LAGUAGE,default='python')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    feedback = models.TextField(blank=True, null=True)
    result_value=models.CharField(blank=True,max_length=15)
    all_results = models.JSONField(
        default=list,  # Varsayılan olarak boş bir liste
        help_text="Test sonuçlarının doğru/yanlış bilgisi",
        blank=True
    )
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s solution for {self.problem.problem.title} in {self.group.name}-{self.problem.lesson.title}"



class LessonScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='scores')
    problem = models.ForeignKey(GroupLessonProblem, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)


