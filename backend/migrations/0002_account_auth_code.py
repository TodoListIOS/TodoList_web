# Generated by Django 2.2.5 on 2020-01-06 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='Auth_code',
            field=models.CharField(default='Bust_is_small', max_length=128),
        ),
    ]
