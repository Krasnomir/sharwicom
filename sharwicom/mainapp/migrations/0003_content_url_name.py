# Generated by Django 4.2.11 on 2025-02-09 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_content_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='url_name',
            field=models.TextField(default=''),
        ),
    ]
