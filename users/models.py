from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.utils.timezone import now
from datetime import timedelta

from django.db.models import Count

from problems.models import Solution
from problems.models import Problem

from django.db.models import Count




def one_minute_ago():
    return now() - timedelta(minutes=1)





def user_directory_path(instance, filename):
    # Dosya uzantısını al
    ext = filename.split('.')[-1]
    # Yeni dosya adını 'profile_pic.ext' olarak belirle
    filename = f"profile_pic.{ext}"
    # Kullanıcıya özel yol: user_pfps/<username>/profile_pic.ext
    return f'user_pfps/{instance.user.username}/{filename}'


class UserProfile(models.Model):
    TAG_CHOICES = [
        ('newbie', 'Newbie'),
        ('skilled', 'Skilled'),
        ('admin', 'Admin'),
        ('professional', 'Professional'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="profiles")
    profile_photo=models.ImageField(upload_to=user_directory_path,default='default/default_pfp.jpg')
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, default='newbie')
    first_join_date=models.DateTimeField(auto_now=True)

    solved_problem_count = models.PositiveIntegerField(default=0)

    def update_solved_problem_count(self):
        self.solved_problem_count = Solution.objects.filter(
            user=self.user,
            is_correct=True
        ).values('problem').distinct().count()
        self.save()
    
    class Meta:
        verbose_name_plural="Kullanici bilgileri"

    def __str__(self):
        return f"{self.user.get_full_name()} Profile"
    
    
    

def create_user_profile(instance,created,**kwargs):
    if(created==True):
        UserProfile.objects.create(user=instance)

post_save.connect(receiver=create_user_profile,sender=User)


class UserProblemStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problem_statuses')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='problem_statuses')
    is_solved = models.BooleanField(default=False)  # Çözüm durumu

    class Meta:
        unique_together = ('user', 'problem')  # Her kullanıcı-problem çifti benzersiz olmalı.

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}: {'Solved' if self.is_solved else 'Not Solved'}"


# Create your models here.
