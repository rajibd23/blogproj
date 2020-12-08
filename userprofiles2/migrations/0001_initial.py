# Generated by Django 3.1.3 on 2020-12-06 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.PositiveIntegerField(blank=True, null=True, verbose_name='Phone')),
                ('gender', models.CharField(blank=True, choices=[('man', 'Man'), ('woman', 'Woman')], max_length=40, verbose_name='Gender')),
                ('avatar', models.ImageField(blank=True, upload_to='userprofiles2/avatars', verbose_name='Avatar')),
                ('completion_level', models.PositiveSmallIntegerField(default=0, verbose_name='Profile completion percentage')),
                ('email_is_verified', models.BooleanField(default=False, verbose_name='Email is verified')),
                ('personal_info_is_completed', models.BooleanField(default=False, verbose_name='Personal info completed')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User profile',
                'verbose_name_plural': 'User profiles',
            },
        ),
    ]
