# Generated by Django 5.0.3 on 2024-04-03 06:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert_app', '0026_alter_expert_class_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='certifications/')),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications_set', to='expert_app.expert')),
            ],
        ),
    ]