# Generated by Django 5.1.2 on 2024-10-26 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TRCodersTrying', '0007_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='icerik',
            new_name='comment_icerik',
        ),
    ]
