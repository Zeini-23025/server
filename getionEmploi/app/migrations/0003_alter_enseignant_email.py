# Generated by Django 5.1.7 on 2025-03-08 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_enseignant_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enseignant',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]
