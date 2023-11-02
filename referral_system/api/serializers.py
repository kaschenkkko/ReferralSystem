from frontend.models import CustomUser
from rest_framework import serializers


class ListInviteSerializer(serializers.ModelSerializer):
    """Сериализатор для подписчиков/подписок."""

    class Meta:
        model = CustomUser
        fields = ('id', 'phonenumber')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для информации о пользователях."""

    followers = ListInviteSerializer(many=True, read_only=True,
                                     source='invitation')
    following = ListInviteSerializer(many=True, read_only=True,
                                     source='invitations')

    class Meta:
        model = CustomUser
        fields = ('id', 'phonenumber', 'invite_code', 'followers',
                  'following')
