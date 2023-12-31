# Generated by Django 4.1.2 on 2023-08-03 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elearning', '0006_achievements_courseenroll_timedelta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='img',
            field=models.ImageField(default='defualt.png', upload_to='elerning_course_img/'),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='img',
            field=models.ImageField(default='defualt.png', upload_to='elerning_subjects/'),
        ),
        migrations.CreateModel(
            name='QuestionsTaken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('courses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearning.courses')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
