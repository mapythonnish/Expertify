# Generated by Django 5.0.3 on 2024-03-21 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert_app', '0017_notification_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='message',
            field=models.TextField(default='Default message'),
        ),
    ]
