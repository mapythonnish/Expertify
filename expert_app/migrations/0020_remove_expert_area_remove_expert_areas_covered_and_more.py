# Generated by Django 5.0.3 on 2024-04-02 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert_app', '0019_remove_expert_english_remove_expert_hindi_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expert',
            name='area',
        ),
        migrations.RemoveField(
            model_name='expert',
            name='areas_covered',
        ),
        migrations.RemoveField(
            model_name='expert',
            name='emergency_contact_name',
        ),
        migrations.RemoveField(
            model_name='expert',
            name='emergency_phone_number',
        ),
        migrations.AlterField(
            model_name='expert',
            name='class_location',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='expert',
            name='languages_spoken',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
