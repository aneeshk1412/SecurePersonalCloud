from rest_framework import serializers
from .models import DirFile


class DirFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirFile
        fields = ('name', 'file_type', 'modified_time', 'encryption_scheme', 'file_path', )
