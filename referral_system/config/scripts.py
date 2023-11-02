import logging
import random
import string
import time
from random import randrange

from django.contrib.auth import get_user_model

from .constants import AUTH_CODE_LENGTH, INVITE_CODE_LENGTH

logger = logging.getLogger(__name__)


def invite_code_generator(size=INVITE_CODE_LENGTH,
                          chars=string.digits + string.ascii_letters) -> str:
    """Генерирует 6-значный инвайт-код из цифр и букв.

    Если пользователь с таким инвайт-кодом уже существует, то
    запускается рекурсия.
    """

    CustomUser = get_user_model()
    invite_code = ''.join(random.choice(chars) for _ in range(size))
    user = CustomUser.objects.filter(invite_code=invite_code)
    if user:
        logger.warning('Инвайт-код дублируется.')
        return invite_code_generator()
    return invite_code


def auth_code_generator(size=AUTH_CODE_LENGTH, chars=string.digits) -> str:
    """Генерирует 4-значный код из цифр."""

    time.sleep(randrange(1, 2))
    return ''.join(random.choice(chars) for _ in range(size))


def editing_phone(phone) -> str:
    """Изменение номера телефона, если он начинается с восьмёрки.

    Метод создан, что-бы в БД не сохранялись одинаковые номера.
    Пример: 8xxx --> +7xxx
    """

    str_number = bytearray(phone, 'utf-8')
    str_number[0] = bytes('7', 'utf-8')[0]
    new_phone = str(str_number, 'utf-8').split()
    new_phone.insert(0, '+')
    new_phone = ''.join(new_phone)
    return new_phone


def form_html(obj):
    """Кастомный метод для отображения форм.

    Поменял местоположение label для работы эффекта от bootstrap.
    """

    return obj._html_output(
        normal_row=('%(html_class_attr)s%(field)s'
                    '%(help_text)s%(label)s%(errors)s'),
        error_row='<li>%s</li>',
        row_ender='</li>',
        help_text_html='<span class="helptext">%s</span>',
        errors_on_separate_row=False)
