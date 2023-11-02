from config.scripts import invite_code_generator
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    """
    Добавлен дополнительный виджет для формы редактирования пользователей.
    """

    class Meta:
        widgets = {'phonenumber': PhoneNumberPrefixWidget()}


class CustomUserCreationForm(ModelForm):
    """Форма для создания пользователей."""

    class Meta:
        model = CustomUser
        fields = ('phonenumber',)
        widgets = {'phonenumber': PhoneNumberPrefixWidget()}

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.invite_code = invite_code_generator()
        if commit:
            user.save()
        return user


def get_user_by_phonenumber(phonenumber):
    """Оптимизация поиска(идею взял с habr.com)

    Метод возвращает объект, у которого номер телефона равен переданному
    значению из поля для поиска.
    """

    try:
        return CustomUser.objects.get(phonenumber__exact=phonenumber)
    except ObjectDoesNotExist:
        return None


class UserPhonenSearchAdmin(admin.ModelAdmin):
    """Оптимизация поиска(идею взял с habr.com)

    Когда таблица пользователей и таблица с данными разростается,
    замечаем что любая попытка найти что-то приводит к Time out error.
    Поэтому лучше преобразовать номер телефона в id и уже по нему делать поиск.
    """

    def get_search_results(self, request, queryset, search_term):
        user = get_user_by_phonenumber(search_term)
        if user is not None:
            queryset = queryset.filter(id=user.id)
            use_distinct = False
        else:
            queryset, use_distinct = super().get_search_results(request,
                                                                queryset,
                                                                search_term)
        return queryset, use_distinct


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, UserPhonenSearchAdmin):
    list_display = ('phonenumber',)
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    add_fieldsets = (
        ('Регистрация',
            {'fields': ('phonenumber',)}
         ),
    )

    fieldsets = (
        ('Регистрация',
            {'fields': ('phonenumber',)}
         ),
        ('Данные пользователя',
            {'fields': (
                'invite_code', 'is_staff', 'is_superuser', 'last_login'
            )}
         )
    )

    ordering = ('-id',)
    list_filter = ('is_superuser',)
    search_fields = ('phonenumber',)
