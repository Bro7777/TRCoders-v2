
from django.urls import path

from.views import *

urlpatterns = [
    
    path('detail/<int:pk>/',problem_detail,name='problem_detail'),
    path('detail/<int:problem_id>/submit_solution',submit_solution,name='submit_solution'),
    path('solution/<int:solution_id>/result/',solution_result,name='solution'),
    path('detail/<int:problem_id>/attempts',problem_attempts,name='problem_attempts'),
    path('detail/<int:problem_id>/statistics',problem_stats,name='problem_stats'),
    path('all',all_problems,name='all_problems'),
    path('all/mobile',all_problems_mobile,name='all_problems_mobile'),
    path('detail/<int:pk>/mobile',problem_detail_mobile,name='problem_detail_mobile'),
    path('detail/<int:problem_id>/submit_solution/mobile',submit_solution_mobile,name='submit_solution_mobile'),
    path('solution/<int:solution_id>/result/mobile',solution_result_mobile,name='solution_mobile'),
    path('detail/<int:problem_id>/statistics/mobile',problem_stat_mobile,name='problem_stats_mobile'),
    path('detail/<int:problem_id>/attempts/mobile',problem_attempts_mobile,name='problem_attempts_mobile'),
]