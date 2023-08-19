import random
import string
import time
from random import randrange

from .constants import AUTH_CODE_LENGTH, INVITE_CODE_LENGTH


def invite_code_generator(size=INVITE_CODE_LENGTH,
                          chars=string.digits + string.ascii_letters):
    """Генерирует 6-значный код из цифр и букв."""
    return ''.join(random.choice(chars) for _ in range(size))


def auth_code_generator(size=AUTH_CODE_LENGTH, chars=string.digits):
    """Генерирует 4-значный код из цифр."""
    time.sleep(randrange(1, 2))
    return ''.join(random.choice(chars) for _ in range(size))
