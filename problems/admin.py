from django.contrib import admin
from.models import *
from users.models import UserProblemStatus

class TestCasesInline(admin.TabularInline):
    model = TestCases
    extra = 1  # Number of empty forms to display

class ExamplesInline(admin.TabularInline):
    model = Examples
    extra = 1  # Number of empty forms to display
class ProblemAdmin(admin.ModelAdmin):
    inlines = [ExamplesInline,TestCasesInline]

# Register your models here.
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Solution)

@admin.register(UserProblemStatus)
class UserProblemStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'is_solved')
    list_filter = ('is_solved',)

#admin.site.register(Problem)
#admin.site.register(TestCases)
#admin.site.register(Solution)