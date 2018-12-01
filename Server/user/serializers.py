from rest_framework import serializers
from .models import DirFile
from django.contrib.auth.models import User


class DirFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirFile
        fields = ('pk',
                  'owners',
                  'name',
                  'file_type',
                  'modified_time',
                  'encryption_scheme',
                  'file_path',
                  'b2code',
                  'last_update_by',
                  'parent_id', )


class DirFileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirFile
        fields = ('pk',
                  'owners',
                  'name',
                  'file_type',
                  'parent_id',
                  'modified_time',
                  'encryption_scheme',
                  'file_path',
                  'b2code',
                  'last_update_by',
                  'file_contents', )


class UserSerializer(serializers.ModelSerializer):
    dirfiles = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'dirfiles', )


class DirStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirFile
        fields = ('file_path', 'b2code', 'modified_time', 'file_type', 'name', )
