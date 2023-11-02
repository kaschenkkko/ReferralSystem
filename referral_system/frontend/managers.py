from config.scripts import editing_phone, invite_code_generator
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        """Создание пользователя по номеру телефона.

        При регистрации пользователю присваивается инвайт-код.
        """

        if not phone:
            raise ValueError('Номер телефона должен быть указан')
        phonenumber = editing_phone(phone) if phone[0] == '8' else phone
        invite_code = invite_code_generator()
        user = self.model(phonenumber=phonenumber, invite_code=invite_code,
                          **extra_fields)
        if user.is_staff and user.is_superuser:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, phonenumber, password=None, **extra_fields):
        """Создание суперпользователя."""

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        elif extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phonenumber, password, **extra_fields)
