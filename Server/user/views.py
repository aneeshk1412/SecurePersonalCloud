from django.shortcuts import render
from .models import DirFile
from .serializers import DirFileDetailSerializer
from rest_framework import generics
# Create your views here.


class DirFileList(generics.ListCreateAPIView):
    queryset = DirFile.objects.all()
    serializer_class = DirFileDetailSerializer


class DirFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DirFile.objects.all()
    serializer_class = DirFileDetailSerializer
    lookup_field = 'file_path'
    lookup_url_kwarg = 'file_path'
