# Generated by Django 4.2.1 on 2023-06-24 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_user_is_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
