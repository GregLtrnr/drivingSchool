# Generated by Django 4.1.7 on 2023-04-27 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_account_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='paid_hours',
            field=models.IntegerField(default=0),
        ),
    ]
