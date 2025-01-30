from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=120,blank=False,verbose_name="Baslik")
    icerik=RichTextField()
    draft=models.BooleanField(default=False,verbose_name="Taslak olussunmu?")
    image=models.ImageField(upload_to='images/',blank=True, null=True,verbose_name="Fotgraf ekle")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True) #Ilk duzeldilende 
    updated_date=models.DateTimeField(auto_now=True) #Sonra dan edit edilende


    def __str__(self):
        return "{}".format(self.title)
    
    class Meta :
        verbose_name="Gonderilerim"
        verbose_name_plural="Gonderilerim"
        ordering=["id"]

class Comment(models.Model):
    post=models.ForeignKey(Post,verbose_name='Post',related_name='comment',on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    comment_icerik=models.TextField(max_length=200,verbose_name='icerik')
    created_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='Yorum'
        verbose_name_plural='Yorumlar'
    
    def __str__(self):
        return "{}".format(self.post,self.user)
    

    



        
    

    


