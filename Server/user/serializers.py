from rest_framework import serializers
from .models import DirFile
from django.contrib.auth.models import User


class DirFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirFile
        fields = ('pk', 'owners', 'name', 'file_type', 'modified_time', 'encryption_scheme', 'file_path', 'md5code', )


class UserSerializer(serializers.ModelSerializer):
    dirfiles = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'dirfiles')
