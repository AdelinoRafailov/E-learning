# Generated by Django 4.0.3 on 2022-03-27 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appdetails',
            name='logo',
            field=models.ImageField(upload_to='static/system'),
        ),
    ]
