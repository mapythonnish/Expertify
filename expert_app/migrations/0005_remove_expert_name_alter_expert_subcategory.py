# Generated by Django 5.0.3 on 2024-03-13 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert_app', '0004_alter_expert_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expert',
            name='name',
        ),
        migrations.AlterField(
            model_name='expert',
            name='subcategory',
            field=models.CharField(max_length=100),
        ),
    ]
