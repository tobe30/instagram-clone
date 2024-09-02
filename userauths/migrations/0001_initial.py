# Generated by Django 4.2.3 on 2024-08-30 22:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import userauths.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0002_alter_post_pid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, max_length=200, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, default='default-pp.png', null=True, upload_to=userauths.models.user_directory_path, verbose_name='picture')),
                ('favourite', models.ManyToManyField(to='post.post')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
