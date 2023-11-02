from config.scripts import auth_code_generator, editing_phone
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from frontend.models import CustomUser
from phonenumber_field.validators import validate_international_phonenumber
from rest_framework import decorators, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import UserSerializer


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    """Информация о пользователях."""

    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=('GET',), detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status.HTTP_200_OK)


@decorators.api_view(['POST', 'DELETE'])
@decorators.permission_classes([IsAuthenticated])
def invitation(request):
    """Отправка/удаление инвайт-кода."""

    data = request.data
    code = data.get('invite_code')

    if code is None:
        return Response(
            {'message': 'Введите инвайт-код'},
            status=status.HTTP_400_BAD_REQUEST
        )

    pattern = get_object_or_404(CustomUser.objects.all(), invite_code=code)
    validate_pattern = request.user.invitations.filter(
        invite_code=code).exists()
    serializer = UserSerializer(
        pattern, context={'request': request}
    )

    if request.method == 'POST' and request.user.invitations.all():
        return Response({'message': 'Вы уже активировали один инвайт-код'},
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST' and not validate_pattern:
        request.user.invitations.add(pattern)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE' and validate_pattern:
        request.user.invitations.remove(pattern)
        return Response({'message': 'Приглашение удалено'},
                        status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(['POST'])
def authorization(request):
    """Ввод номера телефона и получение СМС-кода."""

    data = request.data
    phone = data.get('phone_number')

    if phone is None:
        return Response(
            {'message': 'Введите номер телефона'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        validate_international_phonenumber(phone)
    except ValidationError:
        return Response(
            {'message':
             'Введите корректный номер телефона например, 83011234567, или '
             'номер с префиксом международной связи.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    phone = editing_phone(phone) if phone[0] == '8' else phone
    code = auth_code_generator()
    request.session['phone'] = phone
    request.session['code'] = code
    request.session.set_expiry(300)
    return Response(
        {'message': f'СМС код - {code}'},
        status=status.HTTP_200_OK
    )


@decorators.api_view(['POST'])
def verification(request):
    """СМС-верификация и получение JWT-токена.

    Если пользователь ранее не авторизовывался, он будет добавлен в БД.
    """

    data = request.data
    code = data.get('auth_code')

    if (
        not request.session.get('code') or
        not request.session.get('phone')
    ):
        return Response(
            {'message': ('Сначала вам нужно ввести номер телефона '
                         'по адресу /api/auth/')
             },
            status=status.HTTP_400_BAD_REQUEST
        )

    elif code is None:
        return Response(
            {'message': 'Введите код из СМС'},
            status=status.HTTP_400_BAD_REQUEST
        )

    elif code != request.session.get('code'):
        return Response(
            {'message': 'Вы ввели неверный смс-код.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    phone = str(request.session.get('phone'))
    user = CustomUser.objects.filter(phonenumber=phone)

    if not user:
        user = CustomUser.objects.create_user(phone)
    else:
        user = user.get(phonenumber=phone)

    request.session.flush()
    token = AccessToken.for_user(user)
    return Response({'Авторизация прошла успешно, ваш токен': str(token)},
                    status=status.HTTP_200_OK)
