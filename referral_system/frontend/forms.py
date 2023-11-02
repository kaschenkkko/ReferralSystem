from config.scripts import editing_phone, form_html
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import CharField, Form, TextInput
from phonenumber_field.formfields import PhoneNumberField

from .models import CustomUser

User = get_user_model()


class InviteForm(Form):
    """Форма для отправки инвайт-кода."""

    def __init__(self, *args, **kwargs):
        """
        Переопределил конструктор, что-бы можно было передать
        в форму информацию о запросе(request).
        """

        self.request = kwargs.pop('request')
        super(InviteForm, self).__init__(*args, **kwargs)

    invite_code = CharField(
        widget=TextInput(attrs={
            'placeholder': 'Введите инвайт-код',
            'class': 'form-control me-sm-2 me-2'}
        ),
        required=True,
        help_text='Вы можете отправить только один инвайт-код.')

    def clean_invite_code(self):
        """Валидация инвайт-кода.

        Проверка на существование инвайт-кода.
        Запрет на отправку инвайт-кода самому себе.
        Проверка на количество отправленных приглашений(не больше одного).
        """

        data = self.cleaned_data.get('invite_code')
        user = CustomUser.objects.filter(invite_code=data)

        if not user:
            raise ValidationError('Вы ввели неверный инвайт-код')

        elif user.get(invite_code=data) == self.request.user:
            raise ValidationError('Вы не можете отправить приглашение себе.')

        elif self.request.user.invitations.all():
            raise ValidationError('Вы уже отправили одно приглашение.')

        return data


class VerifyForm(Form):
    """Форма для sms-верификации/регистрации.

    Если пользователь входит на сайт первый раз, он
    будет добавлен в БД, после подтверждения sms.
    """

    def __init__(self, *args, **kwargs):
        """
        Переопределил конструктор, что-бы можно было передать
        в форму информацию о запросе(request).
        """

        self.request = kwargs.pop("request")
        super(VerifyForm, self).__init__(*args, **kwargs)

    code = CharField(
        widget=TextInput(attrs={
            'placeholder': 'Введите смс-код',
            'class': 'form-control',
            'id': 'floatingInput'}
        ),
        required=True,
        label='Введите смс-код')

    def as_custom(self):
        return form_html(self)

    def clean_code(self):
        """Валидация смс-кода. Проверка, что пользователь введёт верный код."""

        data = self.cleaned_data.get('code')
        if data != self.request.session.get('code'):
            raise ValidationError('Вы ввели неверный смс-код.')
        return data

    def save(self):
        """Метод для сохранения пользователей в БД."""

        phone = str(self.request.session.get('phone'))
        user = CustomUser.objects.filter(phonenumber=phone)

        if not user:
            user = CustomUser.objects.create_user(phone)
            return user

        phone = editing_phone(phone) if phone[0] == '8' else phone
        user = user.get(phonenumber=phone)
        user.save()
        return user


class PhoneForm(Form):
    """Форма для ввода номера телефона."""

    phonenumber = PhoneNumberField(
        widget=TextInput(attrs={
            'placeholder': 'Введите номер телефона',
            'class': 'form-control',
            'id': 'floatingInput'}
        ),
        required=True,
        label='Номер телефона')

    phonenumber.error_messages['invalid'] = (
        'Введите корректный номер телефона например, 83011234567, или '
        'номер с префиксом международной связи.')

    def as_custom(self):
        return form_html(self)
