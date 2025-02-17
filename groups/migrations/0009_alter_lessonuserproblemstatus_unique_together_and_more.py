# Generated by Django 5.1.2 on 2024-12-10 21:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0008_alter_grouplessonproblem_group_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='lessonuserproblemstatus',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='lessonuserproblemstatus',
            name='percent_of_success',
            field=models.IntegerField(default=100, help_text='Yuzde'),
        ),
        migrations.AlterField(
            model_name='lessonuserproblemstatus',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_problem_statuses', to='groups.grouplessonproblem'),
        ),
        migrations.AlterUniqueTogether(
            name='lessonuserproblemstatus',
            unique_together={('user', 'problem', 'percent_of_success')},
        ),
    ]
