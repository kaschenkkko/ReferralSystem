from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    """Добавлен дополнительный виджет для формы редактирования пользователей"""
    class Meta:
        widgets = {
            'phonenumber': PhoneNumberPrefixWidget(),
        }


class CustomUserCreationForm(UserCreationForm):
    """Добавлен дополнительный виджет для формы создания пользователей"""
    class Meta:
        widgets = {
            'phonenumber': PhoneNumberPrefixWidget(),
        }


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('phonenumber',)
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    add_fieldsets = (
        ('Регистрация',
            {'fields': (
                'phonenumber', 'password1', 'password2'
            )}
         ),
        ('Данные пользователя',
            {'fields': (
                'invite_code', 'auth_code',
                'is_staff', 'is_superuser'
            )}
         )
    )
    fieldsets = (
        ('Регистрация',
            {'fields': (
                'phonenumber',
            )}
         ),
        ('Данные пользователя',
            {'fields': (
                'invite_code', 'auth_code',
                'is_staff', 'is_superuser', 'last_login'
            )}
         )
    )
    ordering = ('id',)
    list_filter = ('phonenumber',)
    search_fields = ('phonenumber',)
