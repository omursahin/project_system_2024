# Generated by Django 5.0.3 on 2024-05-22 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectreport',
            name='description',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]