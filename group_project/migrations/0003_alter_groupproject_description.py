# Generated by Django 5.0.3 on 2024-05-22 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_project', '0002_rename_group_project_groupproject_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupproject',
            name='description',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
