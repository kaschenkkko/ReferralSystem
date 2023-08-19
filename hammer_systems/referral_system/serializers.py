from rest_framework import serializers

from .models import CustomUser


class ListInviteSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей активировавших инвайт-код."""
    class Meta:
        model = CustomUser
        fields = ('id', 'phonenumber')


class UserSerializer(serializers.ModelSerializer):
    invitation = ListInviteSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'phonenumber', 'invite_code', 'invitation')
