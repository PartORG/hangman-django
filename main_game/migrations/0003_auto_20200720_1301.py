# Generated by Django 3.0.7 on 2020-07-20 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_game', '0002_auto_20200720_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='name',
        ),
        migrations.AddField(
            model_name='game',
            name='word_letters',
            field=models.CharField(default='', max_length=50),
        ),
    ]
