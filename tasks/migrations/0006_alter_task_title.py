# Generated by Django 4.1.1 on 2022-10-04 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_remove_task_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.TextField(max_length=1000),
        ),
    ]