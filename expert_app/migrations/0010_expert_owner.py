# Generated by Django 5.0.3 on 2024-03-16 05:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert_app', '0009_remove_expert_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='expert_app.owner'),
        ),
    ]
