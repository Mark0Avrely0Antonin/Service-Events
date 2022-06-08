from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Select

from service.models import CustomUser, Event, Vote


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'is_public', 'data_passage', 'data_placing', 'data_created',)
    list_filter = ('is_public', )
    search_fields = ('title', 'id', 'is_public', 'data_created',)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'event')
    list_filter = ('event__is_public',)
    search_fields = ('voter', 'event')


class CustomUserAdmin(UserAdmin):
    search_fields = ('username', 'email', 'id')
    list_display = ('username', 'email', 'id', 'is_staff', 'is_active')
    fieldsets = (
        ('Главное', {'fields': ('username', 'email')}),
        ('Доступ', {'fields': ('is_staff', 'is_active')}),
        ('Персональные данные', {'fields': ('role', )})
    )
    formfield_overrides = {
        CustomUser.role: {'widget': Select(attrs={'class': 'form-control'})}
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role')
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)