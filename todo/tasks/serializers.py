from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', ]


class TaskSerializer(serializers.Serializer):

    owner = UserSerializer(read_only=True)
    body = serializers.CharField()
    estimated_finish_time = serializers.DateTimeField(format='%d:%m:%Y %H:%M', input_formats=['%d:%m:%Y %H:%M', ])
    is_finished = serializers.BooleanField(read_only=True)
