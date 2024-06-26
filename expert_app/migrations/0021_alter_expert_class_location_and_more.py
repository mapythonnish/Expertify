# Generated by Django 5.0.3 on 2024-04-02 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert_app', '0020_remove_expert_area_remove_expert_areas_covered_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expert',
            name='class_location',
            field=models.CharField(blank=True, choices=[('OFFLINE_AT_STUDENT_HOME', 'Offline at Student Home'), ('OFFLINE_AT_OWN_HOME', 'Offline at Own Home'), ('ONLINE', 'Online')], max_length=100),
        ),
        migrations.AlterField(
            model_name='expert',
            name='languages_spoken',
            field=models.CharField(blank=True, choices=[('hindi', 'Hindi'), ('english', 'English'), ('marathi', 'Marathi'), ('kannada', 'Kannada')], max_length=100),
        ),
    ]
