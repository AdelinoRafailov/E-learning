# Generated by Django 4.1.2 on 2023-07-18 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0004_rename_des_courses_longdes_courses_shortdes'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='feature',
            field=models.TextField(default='', max_length=1000),
        ),
    ]
