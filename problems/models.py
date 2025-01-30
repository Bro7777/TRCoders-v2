from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from datetime import datetime

class Problem(models.Model):
    choices=[
        ('-','Belirlenmemis'),
        ('kolay','Kolay'),
        ('orta','Orta'),
        ('zor','Zor'),
    ]
    title=models.CharField(max_length=60)
    title_en=models.CharField(max_length=60,help_text="Title in Engish",blank=True)
    title_az=models.CharField(max_length=60,help_text="Azerbaycan dilinde basliq",blank=True)
    statement=RichTextField(max_length=1000)
    statement_en = RichTextField(max_length=1000, help_text="Statement in English",blank=True)
    statement_az = RichTextField(max_length=1000, help_text="Statement in Azerbaijani",blank=True)
    #statement_fr = RichTextField(max_length=400, help_text="Statement in French")
    difficulty=models.CharField(max_length=20,choices=choices,default='-')
    
    def __str__(self):
        return self.title
    

class TestCases(models.Model):
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE,related_name='test_cases')
    input_data = models.TextField(help_text="Testin giriş verisi")
    expected_output = models.TextField(help_text="Beklenen çıktı")


    def __str__(self):
        return f"Test Case for {self.problem.title}"
    
class Examples(models.Model):
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE,related_name="ornekler")
    input_data=RichTextField(help_text="Ornegin giris verisi")
    output_data=RichTextField(help_text="Ornegin cikis verisi")
    


class Solution(models.Model):
    PROGRAMMING_LAGUAGE=[
        ('python','Python3'),
        ('cpp','C++20')
    ]
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE,related_name='solutions')
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
        return f"{self.user.username}'s solution for {self.problem.title}"







# Create your models here.
