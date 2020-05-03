# Generated by Django 3.0 on 2020-05-03 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz', '0001_initial'),
        ('announcements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcements',
            name='year_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Year_Level'),
        ),
    ]
