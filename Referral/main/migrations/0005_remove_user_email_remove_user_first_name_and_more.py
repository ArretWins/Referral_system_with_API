# Generated by Django 4.2.4 on 2023-08-26 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_user_invite_code_activated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
    ]
