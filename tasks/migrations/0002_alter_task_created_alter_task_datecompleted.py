# Generated by Django 5.0.2 on 2024-08-22 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='datecompleted',
            field=models.DateTimeField(),
        ),
    ]
