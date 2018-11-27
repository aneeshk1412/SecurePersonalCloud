from rest_framework import serializers
from .models import DirFile
from django.contrib.auth.models import User


class DirFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirFile
        fields = ('pk', 'owners', 'name', 'file_type', 'modified_time', 'encryption_scheme', 'file_path', )


class UserSerializer(serializers.ModelSerializer):
    dirfiles = serializers.PrimaryKeyRelatedField(many=True, queryset=DirFile.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'dirfiles')
