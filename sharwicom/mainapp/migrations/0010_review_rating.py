# Generated by Django 4.2.11 on 2025-02-12 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_remove_content_review_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.SmallIntegerField(default=1),
        ),
    ]
