from django.contrib import admin
from.models import *
class ProblemsInline(admin.TabularInline):
    model=GroupLessonProblem
    fields = ('lesson', 'problem', 'max_score')
    extra=1
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1  # Boş ders ekleme alanı sayısı
    
    fields = ('title', 'description', 'pdf')  # Görünen alanlar
    
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'created_at')
    search_fields = ('name',)
    inlines = [LessonInline,ProblemsInline]

#admin.site.register(GroupLessonProblem)
admin.site.register(GroupLessonSolution)


admin.site.register(LessonScore)
#admin.register(LessonUserProblemStatus)
#admin.site.register(Lesson)

# Register your models here.
