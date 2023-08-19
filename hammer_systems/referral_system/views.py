from django.shortcuts import get_object_or_404
from rest_framework import decorators, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import CustomUser
from .scripts import auth_code_generator
from .serializers import UserSerializer


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    """GET-запросы для вывода информации о пользователях."""
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
def invitation(request, code):
    """Активация/удаление инвайт-кода."""
    pattern = get_object_or_404(CustomUser.objects.all(), invite_code=code)
    validate_pattern = request.user.invitations.filter(
        invite_code=code).exists()
    serializer = UserSerializer(
        pattern, context={'request': request}
    )

    if request.method == 'POST' and request.user.invitations.all():
        return Response({'message': 'Вы уже активировали инвайт-код'},
                        status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST' and not validate_pattern:
        request.user.invitations.add(pattern)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE' and validate_pattern:
        request.user.invitations.remove(pattern)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(['POST'])
def authorization(request):
    """Авторизация по номеру телефона.

    Если пользователь ранее не авторизовывался, он будет добавлен в БД.
    """
    data = request.data
    phone = data.get('phone_number')
    if phone is None:
        return Response(
            {'message': 'Введите номер телефона'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = CustomUser.objects.filter(phonenumber=phone)
    if not user:
        user = CustomUser.objects._create_user(phone)
        return Response(
            {'message': f'СМС код - {user.auth_code}'},
            status=status.HTTP_201_CREATED
            )
    user = CustomUser.objects.get(phonenumber=phone)
    user.auth_code = auth_code_generator()
    user.save()
    user.confirmation_code = user.auth_code
    return Response(
        {'message': f'СМС код - {user.auth_code}'},
        status=status.HTTP_200_OK
    )


@decorators.api_view(['POST'])
def verification(request):
    """СМС-верификация и получение JWT-токена."""
    data = request.data
    phone = data.get('phone_number')
    code = data.get('auth_code')
    if phone is None:
        return Response(
            {'message': 'Введите номер телефона'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if code is None:
        return Response(
            {'message': 'Введите код из СМС'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user = get_object_or_404(CustomUser, phonenumber=phone)
    if user.auth_code == code:
        user.save()
        token = AccessToken.for_user(user)
        return Response({'Авторизация прошла успешно, ваш токен': str(token)},
                        status=status.HTTP_200_OK)
    return Response(
        {'message': 'Неправильный код'},
        status=status.HTTP_400_BAD_REQUEST
    )
