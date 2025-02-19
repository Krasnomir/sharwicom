# Generated by Django 4.2.11 on 2025-02-11 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0008_content_review_delete_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='review',
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('summary', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.content')),
            ],
        ),
    ]
