# Generated by Django 4.0.5 on 2022-06-08 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=25, verbose_name='Имя пользователя')),
                ('email', models.EmailField(max_length=30, unique=True, verbose_name='Почта пользователя')),
                ('role', models.CharField(choices=[('OR', 'Organizer'), ('VO', 'Voter')], default='VO', max_length=2, verbose_name='Роль пользователя')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название события')),
                ('description', models.TextField(verbose_name='Описание события')),
                ('data_placing', models.DateTimeField(null=True, verbose_name='Дата размещение')),
                ('data_passage', models.DateTimeField(null=True, verbose_name='Дата проведение')),
                ('data_created', models.DateTimeField(auto_now_add=True, verbose_name='Создание события')),
                ('is_public', models.BooleanField(default=True, verbose_name='Публичное события')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Организатор')),
            ],
            options={
                'verbose_name': 'События',
                'verbose_name_plural': 'Событий',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='media/%Y/%m/%d', verbose_name='Резюме добровольца')),
                ('data_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата отклика')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.event', verbose_name='События')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Доброволец')),
            ],
            options={
                'verbose_name': 'Доброволец',
                'verbose_name_plural': 'Добровольцы',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='votes',
            field=models.ManyToManyField(blank=True, null=True, related_name='votes', to='service.vote', verbose_name='Откликнувшиеся'),
        ),
    ]