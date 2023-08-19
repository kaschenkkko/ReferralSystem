from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .constants import (AUTH_CODE_LENGTH, INVITE_CODE_LENGTH,
                        MAX_LENGTH_PHONE_NUMBER)
from .scripts import auth_code_generator, invite_code_generator


class CustomUserManager(BaseUserManager):
    def _create_user(self, phonenumber, password=None, **extra_fields):
        """
        Создание пользователя с указанным телефоном.
        При регистрации пользователю присваивается инвайт-код.
        """
        if not phonenumber:
            raise ValueError('Номер телефона должен быть указан')
        invite_code = invite_code_generator()
        auth_code = auth_code_generator()
        user = self.model(phonenumber=phonenumber, invite_code=invite_code,
                          auth_code=auth_code, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phonenumber, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(phonenumber, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель юзеров, которая основана на модели «AbstractBaseUser».

    Поля модели:
      - phonenumber: номер телефона.
      - invite_code: инвайт-код
      - invitation: активация инвайт-кода
      - auth_code: СМС код для авторизации
    """
    phonenumber = PhoneNumberField(
        validators=[RegexValidator(
            r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')
        ],
        max_length=MAX_LENGTH_PHONE_NUMBER, unique=True,
        verbose_name='Номер телефона'
    )
    invite_code = models.CharField(
        validators=[MinLengthValidator(INVITE_CODE_LENGTH)],
        max_length=INVITE_CODE_LENGTH, verbose_name='Инвайт-код'
    )
    invitation = models.ManyToManyField(
        to='self', symmetrical=False,
        related_name='invitations', verbose_name='Активация инвайт-кода'
    )
    auth_code = models.CharField(
        validators=[MinLengthValidator(AUTH_CODE_LENGTH)],
        max_length=AUTH_CODE_LENGTH, null=True, blank=True,
        verbose_name='СМС код для авторизации'
    )
    is_staff = models.BooleanField(
        default=False, verbose_name='Статус администратора'
    )
    is_superuser = models.BooleanField(
        default=False, verbose_name='Статус суперпользователя'
    )

    USERNAME_FIELD = 'phonenumber'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.phonenumber)
