# Generated by Django 5.0.3 on 2024-04-03 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert_app', '0023_expert_certifications_upload_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expert',
            name='certifications_upload',
            field=models.FileField(upload_to='certificates/'),
        ),
    ]
