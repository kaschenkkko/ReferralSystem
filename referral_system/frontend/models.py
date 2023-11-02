from config.constants import INVITE_CODE_LENGTH, MAX_LENGTH_PHONE_NUMBER
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель юзеров, которая основана на модели «AbstractBaseUser».

    Поля модели:
      - phonenumber: номер телефона.
      - invite_code: инвайт-код
      - invitation: активация инвайт-кода
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
        max_length=INVITE_CODE_LENGTH, verbose_name='Инвайт-код',
        unique=True, blank=True
    )
    invitation = models.ManyToManyField(
        to='self', symmetrical=False,
        related_name='invitations', verbose_name='Активация инвайт-кода'
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
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.phonenumber)
