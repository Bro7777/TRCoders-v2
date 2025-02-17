# Generated by Django 5.1.2 on 2025-01-30 22:22

import django.db.models.deletion
import groups.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0011_lessonscore_delete_lessonuserproblemstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to=groups.models.lesson_pdf_upload_path),
        ),
        migrations.AlterField(
            model_name='lessonscore',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.grouplessonproblem'),
        ),
    ]
