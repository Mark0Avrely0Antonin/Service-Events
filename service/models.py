from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext_lazy


class CustomManager(BaseUserManager):
    def create_user(self, username, email, password, **other_fields):
        if not email:
            raise ValueError(gettext_lazy('Вы забыли написать свою почту'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **other_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(username=username, email=email, password=password, **other_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ORGANIZER = 'OR'
    VOTER = 'VO'
    ROLE_CHOICES = [
        (ORGANIZER, 'Organizer'),
        (VOTER, 'Voter'),
    ]

    username = models.CharField(max_length=25, verbose_name='Имя пользователя')
    email = models.EmailField(max_length=30, verbose_name='Почта пользователя', unique=True)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=VOTER, verbose_name='Роль пользователя')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.username)


class Event(models.Model):
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Организатор')
    title = models.CharField(max_length=255, verbose_name='Название события')
    description = models.TextField(verbose_name='Описание события')
    data_placing = models.DateTimeField(verbose_name='Дата размещение', null=True)
    data_passage = models.DateTimeField(verbose_name='Дата проведение', null=True)
    data_created = models.DateTimeField(auto_now_add=True, verbose_name='Создание события')

    is_public = models.BooleanField(default=True, verbose_name='Публичное события')
    votes = models.ManyToManyField('Vote', verbose_name='Откликнувшиеся', related_name='votes', blank=True, null=True)

    class Meta:
        verbose_name = 'События'
        verbose_name_plural = 'Событий'

    def __str__(self):
        return self.title


class Vote(models.Model):
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Доброволец')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='События')
    file = models.FileField(upload_to='media/%Y/%m/%d', verbose_name='Резюме добровольца', blank=True, null=True)
    data_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата отклика')

    class Meta:
        verbose_name = 'Доброволец'
        verbose_name_plural = 'Добровольцы'

    def __str__(self):
        return str(self.voter)